import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, LabelFrame
from db_connections.mysqldb import SQLDatabase
from PIL import Image, ImageTk
db = SQLDatabase()

LARGEFONT = ("Verdana", 35)


class AdminCompleteServicesPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.domain = tk.StringVar(self)
        self.controller = controller

        results = db.retrieveServicesToComplete()

        wrapper1 = LabelFrame(self, text="")
        wrapper2 = LabelFrame(self, text="Services under you")
        wrapper1.pack(fill=tk.X)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)

        # set style to classic so that background can be changed, error on macbooks
        # tk.Frame.__init__(self, parent)
        # style = ttk.Style(self)
        # style.theme_use('classic')
        label = ttk.Label(wrapper1, text="Complete Services", font=LARGEFONT, background='white')
        label.grid(row=0, column=1, padx=10, pady=10)

        # treeview to show requests that need approval (submitted/in progress)
        global cols 
        cols = ('Request ID', 'Service ID', 'Item ID', 'Request Date', 'Request Status', 'Service Status')

        global tree
        tree = ttk.Treeview(wrapper2, columns=cols, show='headings', height="20")

        self.selectedRequests = []
        self.selectedServices = []

        for col in cols:
            tree.column(col, anchor="center", width=150)
            tree.heading(col, text=col)

        for r in results:
            tree.insert("", "end", values=r)

        tree.grid(row=2, column=1, columnspan=1)

        # Attach scrollbar to treeview
        scrollbar = ttk.Scrollbar(wrapper2, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=2, sticky="ns")

        self.approveButton = tk.Button(self, text="Completed", command=self.completeServices)
        self.approveButton.pack()

    def completeServices(self):

        values = tree.selection()

        for v in values:
            self.selectedRequests.append(tree.item(v)['values'][0])
            self.selectedServices.append(tree.item(v)['values'][1])

        print(self.selectedRequests)
        print(self.selectedServices)

        res = db.completeService(self.selectedRequests, self.selectedServices)

        if res:
            messagebox.showinfo(title="Services Completion", message="Selected record(s) have been updated successfully!")
            for v in values:
                tree.delete(v)
        else:
            messagebox.showinfo(title="Services Completion", message="An error has occurred while records(s) were processed.")
        
        self.selectedRequests.clear()
        self.selectedServices.clear()
