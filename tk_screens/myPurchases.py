import tkinter as tk
from tkinter import *
# import tkinter.ttk as ttk
from tkinter import ttk, messagebox
from db_connections.mongodb import MongoDB
from PIL import Image, ImageTk
from db_connections.mysqldb import SQLDatabase
import datetime

mongo = MongoDB()
mongo.dropCollection("items")
mongo.dropCollection("products")
mongo.resetMongoState()

LARGEFONT = ("Calibri", 35, "bold")

class MyPurchases(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = SQLDatabase()
        self.domain = controller.getDomain()
        self.userID = controller.getUserID()
        print("User ID:")
        print(self.userID)

        self['background']='#F6F4F1'

        # button1 = ttk.Button(self, text="Back to Customer Home",
        #                      command=lambda: controller.show_frame(CustomerPortal))
        # button1.grid(row=1, column=3, padx=5, pady=5)

        self.label = ttk.Label(self, text="My Purchases", font=LARGEFONT)
        self.label.grid(row=0, column=3, padx=10, pady=10)  

        self.loadButton = ttk.Button(self, text="Load Purchases", command=self.showTree)
        self.loadButton.grid(column='1', padx='10', pady='10', row='9')

        self.treeFrame= ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='300')
        self.treeFrame.grid(column='2', columnspan='7', row='6', rowspan='1')

        self.cols = ("Item ID", "Category", "Model", "Price ($)", "Date of Purchase", "Warranty Expiry Date", "Warranty Status", "Service Fee ($)")

        self.tree = ttk.Treeview(self.treeFrame, columns = self.cols, show='headings')
        self.tree.pack(side='left')
        scroll_y = Scrollbar(self.treeFrame, orient = 'vertical', command = self.tree.yview)
        scroll_y.pack(side = RIGHT, fill = Y)
        self.tree.configure(yscrollcommand = scroll_y.set)

        self.requestButton = ttk.Button(self, text="Request to Service", command=self.createRequest)
        self.requestButton.grid(column='6', pady='20', row='11', sticky='e')

    def showTree(self):
        self.tree.delete(*self.tree.get_children())

        # load the purchased items for the currently logged in user
        results = self.db.loadPurchases(self.controller.getUserID())
        # print("Purchases:")
        # for r in results:
        #     print(r)

        for col in self.cols:
            self.tree.column(col, anchor="center", width=150)
            self.tree.heading(col, text=col)

        for r in results:
            # for field in r:
            #     print(field)
            #     print(type(field))
            #     print("-----------")
            self.tree.insert("", "end", values=self.polishData(r))       

    def polishData(self, r):
        dateOfPurchase = r[5]
        warranty = r[6]
        expiryDay = dateOfPurchase.day
        expiryYear = dateOfPurchase.year

        expiryMonth = dateOfPurchase.month + warranty
        if expiryMonth > 12:
            expiryMonth = expiryMonth - 12
            expiryYear = expiryYear + 1

        warrantyExpiry = datetime.date(expiryYear, expiryMonth, expiryDay)
        print(warrantyExpiry)

        today = datetime.date.today()
        validity = ""
        serviceFee = 0.0

        if today < warrantyExpiry:
            validity = "valid"
        else:
            validity = "expired"
            cost = r[3]
            serviceFee = 40 + (cost/5)

        result = (r[0], r[1], r[2], r[4], r[5], warrantyExpiry, validity, serviceFee)
        return result

    def createRequest(self):
        curItem = self.tree.focus()
        serviceFee = self.tree.item(curItem)['values'][7]
        itemID = self.tree.item(curItem)['values'][0]
        dateOfRequest = datetime.date.today()
        # print(serviceFee)
        # print(itemID)
        # print(dateOfRequest)

        res = self.db.createServiceRequest([serviceFee, dateOfRequest, itemID])
        if res: 
            messagebox.showerror(title="Request Service Failed", message=res)
        else : 
            messagebox.showinfo(title="Request Service Success", message= "Succesfully requested for service!")

        requestID = self.db.retrieveRequestID([dateOfRequest, itemID])
        print("Request ID")
        print(requestID[0])

        service = self.db.createService([itemID, requestID])
        if service: 
            messagebox.showerror(title="Service Creation Failed", message=res)
        else : 
            messagebox.showinfo(title="Service Creation Success", message= "Succesfully created service!")

        # refresh table
        self.showTree()