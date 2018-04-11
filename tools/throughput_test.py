import wx
import wx.grid
import pandas as pd
from datetime import datetime
import time
import csv
import elasticsearch

dataSet = None
dataPath = None
colLen = None
rowLen = None
bulkData = None
INDEX = 'efsl_throughput_test'
TYPE = 'throughput'
host = 'http://localhost:9200'
es = elasticsearch.Elasticsearch(host)

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, style=wx.DEFAULT_FRAME_STYLE)

        self.lbl_filename = wx.StaticText(self, -1, "File name : ")
        self.btn_openFile = wx.Button(self, -1, "...", size=(50,-1))
        self.lbl_rows = wx.StaticText(self, -1, "Total rows : ")
        self.txt_filename = wx.TextCtrl(self, -1, "")
        self.txt_rows = wx.TextCtrl(self, -1, "", size=(150,-1))
        self.lbl_dataGrid = wx.StaticText(self, -1, "Data Grid ( Only shows maximum 1,000 rows" )

        self.btn_save = wx.Button(self, -1, "SAVE")
        self.dataGrid = wx.grid.Grid(self, -1, size=(1000, 400))
        self.lbl_result = wx.StaticText(self, -1, "Result :")
        self.txt_result = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=(-1, 120))

        self.dataGrid.SetFocus()

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.openFileDialog, self.btn_openFile)
        self.Bind(wx.EVT_BUTTON, self.clk_save, self.btn_save)
        self.Bind(wx.EVT_CLOSE, self.onCloseFrame)

        self.Centre()

    def onCloseFrame(self, event):
        print("closed Frame")
        self.Destroy()


    def __set_properties(self):
        self.SetTitle("Throughput Test")
        self.SetSize((1020, 750))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.dataGrid.CreateGrid(5, 10) #init


    def __set_dataGridTable(self, row, col):
        self.dataGrid.ClearGrid()
        cols = self.dataGrid.GetNumberCols()
        rows = self.dataGrid.GetNumberRows()
        if cols is not 0:
            self.dataGrid.DeleteCols(0, cols, True)
        if rows is not 0:
            self.dataGrid.DeleteRows(0, rows, True)

        if row > 1000 :
            row = 1000

        self.dataGrid.AppendCols(col, True)
        self.dataGrid.AppendRows(row, True)

        i = 0
        for col_name in dataSet.columns:
            self.dataGrid.SetColLabelValue(i, col_name)
            i += 1

        self.drawData(row, col)


    def __do_layout(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.lbl_filename, flag=wx.RIGHT, border=8)
        hbox1.Add(self.txt_filename, flag=wx.RIGHT, border=8, proportion=1)
        hbox1.Add(self.btn_openFile, flag=wx.RIGHT, border=400)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 7))  # 구분 공간 추가

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.lbl_rows, flag=wx.RIGHT, border=8)
        hbox2.Add(self.txt_rows, flag=wx.RIGHT, border=20)
        hbox2.Add(self.btn_save)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 7))  # 구분 공간 추가

        hbox3 = wx.BoxSizer(wx.VERTICAL)
        hbox3.Add(self.lbl_dataGrid, flag=wx.BOTTOM, border=8)
        hbox3.Add(-1, 7)
        hbox3.Add(self.dataGrid, flag=wx.EXPAND)
        vbox.Add(hbox3, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add((-1, 10))  # 구분 공간 추가
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(self.lbl_result, flag=wx.RIGHT, border=8)
        hbox4.Add(self.txt_result, proportion=1)
        vbox.Add(hbox4, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.SetSizer(vbox)
        # self.Layout()


    def openFileDialog(self, event):
        global dataSet, dataPath, colLen, rowLen, bulkData
        wildcard = "CSV (쉼표로 분리) (*.csv)|*.csv| All files (*.*)|*.*"

        with wx.FileDialog(self, "Open Testdata file", wildcard=wildcard,
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            dataPath = fileDialog.GetPath()
            try:
                dataSet = pd.read_csv(dataPath, sep=',', encoding='utf-8', skiprows=0)
                rowLen = len(dataSet.index)
                colLen = len(dataSet.columns)

                self.txt_filename.SetValue(dataPath)
                self.txt_rows.SetValue("{:,} Rows".format(rowLen))
                self.__set_dataGridTable(rowLen, colLen)

                bulkData = []
                for row in dataSet.to_dict('records'):
                    bulkData.append({"index":{"_index": INDEX, "_type": TYPE}})
                    bulkData.append(row)

            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)

    def drawData(self, row, col):
        for i in range(0, row):
            for j in range(0, col):
                cell = dataSet.iloc[i,j]
                self.dataGrid.SetCellValue(i,j,str(cell))

        self.dataGrid.AutoSizeColumns(setAsMin=True)

    def clk_save(self, event):
        if bulkData == None:
            wx.MessageBox("No data loaded, Please select the .csv file from fileDialog")
        else:
            dlg = wx.MessageDialog(self, "{:,} 건의 데이터를 Elasticsearch에 저장하시겠습니까?".format(rowLen),
                                   "Confirm Save", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()

            if result == wx.ID_OK:
                saveID = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                startTimestamp = time.time() * 1000

                es.bulk(bulkData)

                endTimestamp = time.time() * 1000
                self.txt_result.AppendText("Start timestamp : {} \n  - Processing time ~ {} ms \n".format(saveID, int(round(endTimestamp - startTimestamp))))
                print(" Processing time ~ {} ms".format(int(round(endTimestamp - startTimestamp))))

            elif result == wx.ID_CANCEL:
                print("cancel")


if __name__ == "__main__":
    app = wx.App()
    MyFrame().Show()
    app.MainLoop()
