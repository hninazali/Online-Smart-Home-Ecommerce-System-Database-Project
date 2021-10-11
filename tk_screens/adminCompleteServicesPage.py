import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, LabelFrame
from db_connections.mysqldb import SQLDatabase
from PIL import Image, ImageTk
db = SQLDatabase()

LARGEFONT = ("Verdana", 35)


class AdminCompleteServicesPage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.selectedRequests = []
        self.selectedServices = []
        self['background']='#F6F4F1'

        # set style to classic so that background can be changed, error on macbooks
        # tk.Frame.__init__(self, parent)
        # style = ttk.Style(self)
        # style.theme_use('classic')
        label = ttk.Label(self, text="Services pending Completion", font=LARGEFONT)
        label.grid(row=0, column=4, padx=350, pady=10)

    def showTree(self):

        self.treeFrame = ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='400')
        self.treeFrame.grid(column='2', columnspan='6', row='2', rowspan='1', pady='20', padx='245')

        self.cols = ('Request ID', 'Service ID', 'Item ID', 'Request Date', 'Request Status', 'Service Status')

        results = db.retrieveServicesToComplete(self.domain.get())

        self.tree = ttk.Treeview(self.treeFrame, columns=self.cols, show='headings', height='10')
        self.tree.pack(side='left')
        scrollbar = ttk.Scrollbar(self.treeFrame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side = 'right', fill = 'y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        for col in self.cols:
            self.tree.column(col, anchor="center", width=150)
            self.tree.heading(col, text=col)

        for r in results:
            self.tree.insert("", "end", values=r)

        # approve button removes requests from the list and change the request & service statuses to approved and in progress
        self.cButton = ttk.Button(self, text="Completed", command= lambda: self.completeServices(), width=15)
        self.cButton.grid(row='5', column='4', padx='35', pady='5')

    def completeServices(self):

        values = self.tree.selection()

        for v in values:
            self.selectedRequests.append(self.tree.item(v)['values'][0])
            self.selectedServices.append(self.tree.item(v)['values'][1])

        res = db.completeService(self.selectedRequests, self.selectedServices)

        if res is None:
            messagebox.showwarning(title="Services Completion", message="Please select record(s) to proceed.")
        elif res == len(self.selectedRequests):
            messagebox.showinfo(title="Services Completion", message="Selected record(s) have been updated successfully!")
            for v in values:
                self.tree.delete(v)
        else:
            messagebox.showerror(title="Services Completion", message="An error has occurred while records(s) were processed.")
        
        self.selectedRequests.clear()
        self.selectedServices.clear()
    
    def setUserType(self, userID):
        self.domain = userID
        # Log
        print("gui.py>AdminCompleteServicesPage> Domain Set:", self.domain.get())

        self.showTree()
