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



class MyFrame(wx.Frame):  # this is the parent frame
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenu.Append(1, "Open File", "", wx.ITEM_NORMAL)
        self.menubar.Append(fileMenu, "&File")
        self.SetMenuBar(self.menubar)
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.open_fileDialog, id=1)
        self.Centre()


    def __set_properties(self):
        self.SetTitle("Throughput Test")
        self.SetSize((300, 300))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer_1)
        self.Layout()

    ############
    def open_fileDialog(self, event):
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
                MyDialog1(self).Show()

                # testSet = csv.DictReader(open(dataPath))

                bulkData = []
                for row in csv.DictReader(open(dataPath)):
                    bulkData.append({"index":{"_index": INDEX, "_type": TYPE}})
                    bulkData.append(row)

            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)


class MyDialog1(wx.Dialog):  # this is the PhoneBook dialog box...
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.lbl_filename = wx.StaticText(self, -1, "File name : ")
        self.lbl_rows = wx.StaticText(self, -1, "Total rows : ")
        self.txt_filename = wx.TextCtrl(self, -1, dataPath)
        self.txt_rows = wx.TextCtrl(self, -1, "{:,} Rows".format(rowLen))
        self.lbl_dataGrid = wx.StaticText(self, -1, "Data Grid (Only 1,000 rows of all dataset is shown")

        self.btn_save = wx.Button(self, -1, "SAVE")
        self.dataGrid = wx.grid.Grid(self, -1, size=(1000, 400))
        self.lbl_result = wx.StaticText(self, -1, "Result :")
        self.txt_result = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE, size=(-1, 120))

        self.dataGrid.SetFocus()
        # self.txt_filename.SetFocus()
        # self.txt_rows.Enabled = False
        # self.txt_filename.Enabled = False

        self.__set_properties()
        self.__do_layout()
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.clk_save, self.btn_save)


    def __set_properties(self):
        self.SetTitle("Throughput Test")
        self.SetSize((1020, 750))
        # self.txtID.SetMinSize((150, 27))

        i = 0
        self.dataGrid.CreateGrid(1000, colLen)  # this is to create the grid with same rows as database

        for col in dataSet.columns:
            self.dataGrid.SetColLabelValue(i, col)
            i += 1

        self.drawData()


    def drawData(self):
        for i in range(0, 1000):
            for j in range(0,colLen):
                cell = dataSet.iloc[i,j]
                self.dataGrid.SetCellValue(i,j,str(cell))

        self.dataGrid.AutoSizeColumns(setAsMin=True)


    def __do_layout(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.lbl_filename, flag=wx.RIGHT, border=8)
        hbox1.Add(self.txt_filename, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        vbox.Add((-1, 7))  # 구분 공간 추가
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.lbl_rows, flag=wx.RIGHT, border=8)
        hbox2.Add(self.txt_rows, flag=wx.RIGHT, border=200, proportion=1)

        hbox2.Add(self.btn_save, flag=wx.RIGHT, border=400)
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


    def clk_save(self, event):
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

        event.Skip()

if __name__ == "__main__":
    app = wx.App(False)
    frame_1 = MyFrame(None)
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()