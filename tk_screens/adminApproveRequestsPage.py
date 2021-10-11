import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from db_connections.mysqldb import SQLDatabase
db = SQLDatabase()

LARGEFONT = ("Verdana", 35)


class AdminApproveRequestsPage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.selectedRequests = []
        self.selectedServices = []

        self['background']='#F6F4F1'

        label = ttk.Label(self, text="Requests pending Approval", font=LARGEFONT)
        label.grid(row='0', column='4', padx='220', pady='10')

    def showTree(self):

        self.treeFrame = ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='400')
        self.treeFrame.grid(column='2', columnspan='6', row='2', rowspan='1', pady='20', padx='170')

        self.cols = ('Request ID', 'Service ID', 'Item ID', 'Request Date', 'Payment for Service', 'Request Status', 'Service Status')

        self.tree = ttk.Treeview(self.treeFrame, columns=self.cols, show='headings', height='10')
        self.tree.pack(side='left')
        scrollbar = ttk.Scrollbar(self.treeFrame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side = 'right', fill = 'y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        results = db.retrieveRequestsForApproval()

        for col in self.cols:
            self.tree.column(col, anchor="center", width=150)
            self.tree.heading(col, text=col)

        for r in results:
            self.tree.insert("", "end", values=self.polishData(r))

        # approve button removes requests from the list and change the request & service statuses to approved and in progress
        self.aButton = ttk.Button(self, text="Approve", command= lambda: self.approveRequests(), width=15)
        self.aButton.grid(row='5', column='4', padx='45', pady='5')

    def polishData(self, r):
        paymentStatus = ""
        if r[4] == 0:
            paymentStatus = "Waived"
        else:
            paymentStatus = "Paid"

        result = (r[0], r[1], r[2], r[3], paymentStatus, r[5], r[6])
        return result

    def approveRequests(self):

        values = self.tree.selection()

        for v in values:
            self.selectedRequests.append(self.tree.item(v)['values'][0])
            self.selectedServices.append(self.tree.item(v)['values'][1])     

        res = db.approveRequests(self.selectedRequests, self.selectedServices, self.domain.get())

        if res is None:
            messagebox.showwarning(title="Request Approval", message="Please select record(s) to proceed.")
        elif res == len(self.selectedRequests):
            messagebox.showinfo(title="Requests Approval", message="Selected record(s) have been approved successfully!")
            for v in values:
                self.tree.delete(v)
        else:
            messagebox.showerror(title="Requests Approval", message="An error has occurred while request(s) were processed.")
        
        self.selectedRequests.clear()
        self.selectedServices.clear()

    def setUserType(self, userID):
        self.domain = userID
        # Log
        print("gui.py>AdminApproveRequestsPage> Domain Set:",self.domain.get())

        self.showTree()