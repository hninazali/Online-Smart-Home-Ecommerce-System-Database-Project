import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from db_connections.mongodb import MongoDB
from PIL import Image, ImageTk
# from tk_screens.adminPortal import AdminPortal
mongo = MongoDB()
mongo.dropCollection("items")
mongo.dropCollection("products")
mongo.resetMongoState()

LARGEFONT = ("Verdana", 35)

class AdminItemSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.itemID = tk.StringVar()
        self['background']='#F6F4F1'

        # button1 = ttk.Button(self, text="Back to Admin Home",
        #                      command=lambda: controller.show_frame(AdminPortal))
        # button1.grid(row=1, column=3, padx=5, pady=5)

        label = ttk.Label(self, text="Items List", font=LARGEFONT)
        label.grid(row=0, column=2, padx=10, pady=10)

        itemIDLabel = ttk.Label(self, text="Item ID:")
        itemIDLabel.grid(row=1, column=1, padx=10, pady=10)

        itemIDInput = ttk.Entry(self, textvariable=self.itemID)
        itemIDInput.grid(row=1, column=2, padx=10, pady=10)

        button1 = ttk.Button(self, text="Filter",
                             command=self.renderItemsList)
        button1.grid(row=1, column=3, padx=10, pady=10)

        self.treeFrame= ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='300')
        self.treeFrame.grid(column='1', columnspan='6', row='10', rowspan='1')

        self.cols = ('Item ID', 'Model', 'Category', 'Color', 'Factory', 'Power Supply', 'Production Year', 'Purchase Status', 'Service Status')

        self.tree = ttk.Treeview(self.treeFrame, columns = self.cols,show='headings')
        self.tree.pack(side='left')
        scroll_y = Scrollbar(self.treeFrame, orient = 'vertical', command = self.tree.yview)
        scroll_y.pack(side = RIGHT, fill = Y)
        self.tree.configure(yscrollcommand = scroll_y.set)
        
        res = mongo.findItemByID(self.itemID.get())
        for col in self.cols:
            self.tree.column(col, anchor="center", width=150)
            self.tree.heading(col, text=col)
        for r in  res:
            result = self.mongoToTree(r)
            self.tree.insert("", "end", values=result)

    def renderItemsList(self):
        for r in self.tree.get_children():
            self.tree.delete(r)

        res = mongo.findItemByID(self.itemID.get())

        for col in self.cols:
            self.tree.heading(col, text=col)
        for r in res:
            result = self.mongoToTree(r)
            self.tree.insert("", "end", values=result)

    def mongoToTree(self, r):
        serviceStatus = ""
        if r["PurchaseStatus"] == "Sold" and r["ServiceStatus"] == "":
            serviceStatus = "N/A"
        else:
            serviceStatus =  r["ServiceStatus"]
        re = (r["ItemID"], r["Model"], r["Category"], r["Color"], r["Factory"], r["PowerSupply"], r["ProductionYear"], r["PurchaseStatus"], serviceStatus)
        return re
        

