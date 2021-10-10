import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, LabelFrame
from db_connections.mysqldb import SQLDatabase
from PIL import Image, ImageTk
db = SQLDatabase()

LARGEFONT = ("Verdana", 35)


class AdminApproveRequestsPage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller

        results = db.retrieveRequestsForApproval()

        wrapper1 = LabelFrame(self, text="")
        wrapper2 = LabelFrame(self, text="Requests Waiting for Approval")
        wrapper1.pack(fill=tk.X)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)

        # set style to classic so that background can be changed, error on macbooks
        # tk.Frame.__init__(self, parent)
        # style = ttk.Style(self)
        # style.theme_use('classic')
        label = ttk.Label(wrapper1, text="Approve Requests", font=LARGEFONT, background='white')
        label.grid(row=0, column=1, padx=10, pady=10)

        # treeview to show requests that need approval (submitted/in progress)
        global cols 
        cols = ('Request ID', 'Service ID', 'Item ID', 'Request Date', 'Payment for Service', 'Request Status', 'Service Status')

        global tree
        tree = ttk.Treeview(wrapper2, columns=cols, show='headings', height="20")

        self.selectedRequests = []
        self.selectedServices = []

        for col in cols:
            tree.column(col, anchor="center", width=150)
            tree.heading(col, text=col)

        for r in results:
            result = self.polishData(r)
            tree.insert("", "end", values=result)

        tree.grid(row=2, column=1, columnspan=1)

        # Attach scrollbar to treeview
        scrollbar = ttk.Scrollbar(wrapper2, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=2, sticky="ns")

        # approve button removes requests from the list and change the request & service statuses to approved and in progress
        self.approveButton = tk.Button(self, text="Approve", command=self.approveRequests)
        self.approveButton.pack()

    def polishData(self, r):
        paymentStatus = ""
        if r[4] == 0:
            paymentStatus = "Waived"
        else:
            paymentStatus = "Paid"

        result = (r[0], r[1], r[2], r[3], paymentStatus, r[5], r[6])
        return result

    def approveRequests(self):

        values = tree.selection()

        for v in values:
            self.selectedRequests.append(tree.item(v)['values'][0])
            self.selectedServices.append(tree.item(v)['values'][1])     

        res = db.approveRequests(self.selectedRequests, self.selectedServices, self.domain.get())

        if res:
            messagebox.showinfo(title="Requests Approval", message="Selected record(s) have been approved successfully!")
            for v in values:
                tree.delete(v)
        else:
            messagebox.showinfo(title="Requests Approval", message="An error has occurred while request(s) were processed.")
        
        self.selectedRequests.clear()
        self.selectedServices.clear()

    def setUserType(self, userID):
        self.domain = userID
        # Log
        print("gui.py>AdminApproveRequestsPage> Domain Set:",self.domain.get())