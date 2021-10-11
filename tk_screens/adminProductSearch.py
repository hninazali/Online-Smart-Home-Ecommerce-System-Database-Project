import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from db_connections.mongodb import MongoDB
from PIL import Image, ImageTk
mongo = MongoDB()
mongo.dropCollection("items")
mongo.dropCollection("products")
mongo.resetMongoState()

LARGEFONT = ("Verdana", 35)

class AdminProductSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.category = tk.StringVar(self)
        self.model = tk.StringVar(self)
        
        self['background']='#F6F4F1'
        
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

        

