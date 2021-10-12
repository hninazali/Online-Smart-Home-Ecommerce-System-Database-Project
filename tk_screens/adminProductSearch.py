import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from db_connections.mongodb import MongoDB
from PIL import Image, ImageTk
# from tk_screens.adminPortal import AdminPortal

mongo = MongoDB()
# mongo.dropCollection("items")
# mongo.dropCollection("products")
# mongo.resetMongoState()

LARGEFONT = ("Verdana", 35)

class AdminProductSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.category = tk.StringVar(self)
        self.model = tk.StringVar(self)
        
        self['background']='#F6F4F1'

        # button1 = ttk.Button(self, text="Back to Admin Home",
        #                      command=lambda: controller.show_frame(AdminPortal))
        # button1.grid(row=1, column=3, padx=5, pady=5)

        self.label = ttk.Label(self, text="Products List", font=LARGEFONT)
        self.label.grid(row=0, column=3, padx=10, pady=10)

        # Dropdown menu options
        optionsCategory = ("All", "Lights", "Locks")
        optionsModel = ("All", "Light1", "Light2", "SmartHome1", "Safe1", "Safe2", "Safe3")

        vModel=[]
        self.modelLabel = ttk.Label(self, text="Model:")
        self.modelLabel.grid(row=2, column=1, padx=5, pady=5)
        self.modelBox = ttk.Combobox(self, values = vModel)
        self.modelBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.modelBox.grid(row=2, column=2, sticky=tk.E, padx=10, pady=10)

        def categoryAndModel(event):
            if self.categoryBox.get()=="Lights":
                vModel = ["Light1", "Light2", "SmartHome1",""]
            elif self.categoryBox.get()=="Locks":
                vModel = ["Safe1", "Safe2", "Safe3", "SmartHome1",""]
            else:

                vModel = []
            self.modelBox.configure(values = vModel)

        self.catLabel = ttk.Label(self, text="Model:")
        self.catLabel.grid(row=1, column=1, padx=5, pady=5)
        self.categoryBox = ttk.Combobox(self, values = ["Lights", "Locks",""])
        self.categoryBox.bind('<<ComboboxSelected>>', categoryAndModel)
        self.categoryBox.configure(state='readonly')
        self.categoryBox.grid(row=1, column=2, sticky=tk.E, padx=10, pady=10)

        button2 = ttk.Button(self, text="Filter",
                             command=self.renderProductsList)
        button2.grid(row=2, column=3, padx=10, pady=10)

        self.treeFrame= ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='300')
        self.treeFrame.grid(column='1', columnspan='6', row='10', rowspan='1')

        self.cols = ('Product ID', 'Category', 'Model', 'Price', 'Cost', 'Warranty (months)', 'Inventory Level', 'Number sold')

        self.tree = ttk.Treeview(self.treeFrame, columns = self.cols,show='headings')
        self.tree.pack(side='left')
        scroll_y = Scrollbar(self.treeFrame, orient = 'vertical', command = self.tree.yview)
        scroll_y.pack(side = RIGHT, fill = Y)
        self.tree.configure(yscrollcommand = scroll_y.set)

        res = mongo.adminProductSearch(self.category.get(), self.model.get())
        for col in self.cols:
            self.tree.column(col, anchor="center", width=150)
            self.tree.heading(col, text=col)
        for r in  res:
            result = self.mongoToTree(r)
            self.tree.insert("", "end", values=result)

    def renderProductsList(self):
        for r in self.tree.get_children():
            self.tree.delete(r)

        res = mongo.adminProductSearch(self.categoryBox.get(), self.modelBox.get())

        for col in self.cols:
            self.tree.heading(col, text=col)
        for r in res:
            result = self.mongoToTree(r)
            self.tree.insert("", "end", values=result)

        # self.tree.grid(row=6, column=1, columnspan=1)

    def mongoToTree(self, r):
        resSold = mongo.soldLevel()
        resUnsold = mongo.unsoldLevel()

        re = (r["ProductID"], r["Category"], r["Model"], r["Price ($)"], r["Cost ($)"], r["Warranty (months)"], resSold[r["ProductID"]-1]["total"], resUnsold[r["ProductID"]-1]["total"])
        return re

 
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
        

       

