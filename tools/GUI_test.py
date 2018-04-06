import tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        b = tk.Button(self, text="Done!", command=self.upload_cor)
        b.pack()
        table = tk.Frame(self)
        table.pack(side="top", fill="both", expand=True)

        data = (
            (45417, "rodringof", "CSP L2 Review", 0.000394, "2014-12-19 10:08:12", "2014-12-19 10:08:12"),
            (45418, "rodringof", "CSP L2 Review", 0.000394, "2014-12-19 10:08:12", "2014-12-19 10:08:12"),
            (45419, "rodringof", "CSP L2 Review", 0.000394, "2014-12-19 10:08:12", "2014-12-19 10:08:12"),
            (45420, "rodringof", "CSP L2 Review", 0.000394, "2014-12-19 10:08:12", "2014-12-19 10:08:12"),
            (45421, "rodringof", "CSP L2 Review", 0.000394, "2014-12-19 10:08:12", "2014-12-19 10:08:12"),
            (45422, "rodringof", "CSP L2 Review", 0.000394, "2014-12-19 10:08:12", "2014-12-19 10:08:12"),
            (45423, "rodringof", "CSP L2 Review", 0.000394, "2014-12-19 10:08:12", "2014-12-19 10:08:12"),
        )
        
        self.widgets = {}
        row = 0
        for rowid, reviewer, task, num_seconds, start_time, end_time in (data):
            row += 1
            self.widgets[rowid] = {
                "rowid": tk.Label(table, text=rowid),
                "reviewer": tk.Label(table, text=reviewer),
                "task": tk.Label(table, text=task),
                "num_seconds_correction": tk.Entry(table),
                "num_seconds": tk.Label(table, text=num_seconds),
                "start_time": tk.Label(table, text=start_time),
                "end_time": tk.Label(table, text=start_time)
            }

            self.widgets[rowid]["rowid"].grid(row=row, column=0, sticky="nsew")
            self.widgets[rowid]["reviewer"].grid(row=row, column=1, sticky="nsew")
            self.widgets[rowid]["task"].grid(row=row, column=2, sticky="nsew")
            self.widgets[rowid]["num_seconds_correction"].grid(row=row, column=3, sticky="nsew")
            self.widgets[rowid]["num_seconds"].grid(row=row, column=4, sticky="nsew")
            self.widgets[rowid]["start_time"].grid(row=row, column=5, sticky="nsew")
            self.widgets[rowid]["end_time"].grid(row=row, column=6, sticky="nsew")

        table.grid_columnconfigure(1, weight=1)
        table.grid_columnconfigure(2, weight=1)
        # invisible row after last row gets all extra space
        table.grid_rowconfigure(row+1, weight=1)

    def upload_cor(self):
        for rowid in sorted(self.widgets.keys()):
            entry_widget = self.widgets[rowid]["num_seconds_correction"]
            new_value = entry_widget.get()
            print("%s: %s" % (rowid, new_value))

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()