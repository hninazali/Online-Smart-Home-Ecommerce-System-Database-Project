import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, LabelFrame
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
        
        wrapper1 = LabelFrame(self, text="Header")
        wrapper2 = LabelFrame(self, text="Products List")

        wrapper1.pack(fill=tk.X)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)

        label = ttk.Label(wrapper1, text="Products List", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        # Dropdown menu options
        optionsCategory = ("All", "Lights", "Locks")
        optionsModel = ("All", "Light1", "Light2", "SmartHome1", "Safe1", "Safe2", "Safe3")

        vModel=[]
        self.modelBox = ttk.Combobox(wrapper1, values = vModel)
        self.modelBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.modelBox.grid(row=2, column=1, sticky=tk.E, padx=10, pady=10)

        def categoryAndModel(event):
            if self.categoryBox.get()=="Lights":
                vModel = ["Light1", "Light2", "SmartHome1",""]
            elif self.categoryBox.get()=="Locks":
                vModel = ["Safe1", "Safe2", "Safe3", "SmartHome1",""]
            else:
                vModel = []
            self.modelBox.configure(values = vModel)

        self.categoryBox = ttk.Combobox(wrapper1, values = ["Lights", "Locks",""])
        self.categoryBox.bind('<<ComboboxSelected>>', categoryAndModel)
        self.categoryBox.configure(state='readonly')
        self.categoryBox.grid(row=1, column=1, sticky=tk.E, padx=10, pady=10)

        button2 = ttk.Button(wrapper1, text="Filter",
                             command=self.renderProductsList)
        button2.grid(row=3, column=1, padx=10, pady=10)

        global cols
        cols = ('Product ID', 'Category', 'Model', 'Price', 'Cost', 'Warranty (months)', 'Inventory Level', 'Number sold')

        global tree
        tree = ttk.Treeview(wrapper2, columns=cols, show='headings', height="6")

        res = mongo.adminProductSearch(self.category.get(), self.model.get())
        for col in cols:
            tree.column(col, anchor="center", width=150)
            tree.heading(col, text=col)
        for r in  res:
            result = self.mongoToTree(r)
            tree.insert("", "end", values=result)
        tree.grid(row=6, column=1, columnspan=2)

        scrollbar = ttk.Scrollbar(wrapper2, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=2, sticky="ns")

    def renderProductsList(self):
        for r in tree.get_children():
            tree.delete(r)

        res = mongo.adminProductSearch(self.categoryBox.get(), self.modelBox.get())
        # resSold = mongo.soldLevel()
        # resUnsold = mongo.unsoldLevel()

        # for index, r in enumerate(res):
        #     res[index]["Unsold"] = resSold[r["ProductID"]]["total"]
        #     res[index]["Sold"] = resUnsold[r["ProductID"]]["total"]
        #     print("index")
        #     print(resSold[r["ProductID"]]["total"])
        #     print(resUnsold[r["ProductID"]]["total"])
        #     print(r)

        for col in cols:
            tree.heading(col, text=col)
        for r in res:
            result = self.mongoToTree(r)
            tree.insert("", "end", values=result)

        tree.grid(row=6, column=1, columnspan=1)

    def mongoToTree(self, r):
        resSold = mongo.soldLevel()
        resUnsold = mongo.unsoldLevel()

        re = (r["ProductID"], r["Category"], r["Model"], r["Price ($)"], r["Cost ($)"], r["Warranty (months)"], resSold[r["ProductID"]-1]["total"], resUnsold[r["ProductID"]-1]["total"])
        return re

        

