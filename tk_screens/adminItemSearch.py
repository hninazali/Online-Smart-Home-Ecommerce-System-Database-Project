import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, LabelFrame
from db_connections.mongodb import MongoDB
from PIL import Image, ImageTk
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

        wrapper1 = LabelFrame(self, text="Header")
        wrapper2 = LabelFrame(self, text="Items List")

        wrapper1.pack(fill=tk.X)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)

        label = ttk.Label(wrapper1, text="Items List", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        itemIDLabel = ttk.Label(wrapper1, text="Item ID:")
        itemIDLabel.grid(row=1, column=0, padx=10, pady=10)

        itemIDInput = ttk.Entry(wrapper1, textvariable=self.itemID)
        itemIDInput.grid(row=1, column=1, padx=10, pady=10)

        button1 = ttk.Button(wrapper1, text="Filter",
                             command=self.renderItemsList)
        button1.grid(row=1, column=2, padx=10, pady=10)

        global cols
        cols = ('Item ID', 'Model', 'Category', 'Color', 'Factory', 'Power Supply', 'Production Year', 'Purchase Status', 'Service Status')

        global tree
        tree = ttk.Treeview(wrapper2, columns=cols, show='headings', height="6")

        res = mongo.findItemByID(self.itemID.get())
        for col in cols:
            tree.column(col, anchor="center", width=150)
            tree.heading(col, text=col)
        for r in  res:
            result = self.mongoToTree(r)
            tree.insert("", "end", values=result)
        tree.grid(row=6, column=1, columnspan=1)
        # tree.bind("<ButtonRelease-1>", self.clicker)

        scrollbar = ttk.Scrollbar(wrapper2, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=2, sticky="ns")

    def renderItemsList(self):
        for r in tree.get_children():
            tree.delete(r)

        res = mongo.findItemByID(self.itemID.get())

        for col in cols:
            tree.heading(col, text=col)
        for r in res:
            result = self.mongoToTree(r)
            tree.insert("", "end", values=result)

        tree.grid(row=6, column=1, columnspan=1)

    def mongoToTree(self, r):
        serviceStatus = ""
        if r["PurchaseStatus"] == "Sold" and r["ServiceStatus"] == "":
            serviceStatus = "N/A"
        else:
            serviceStatus =  r["ServiceStatus"]
        re = (r["ItemID"], r["Model"], r["Category"], r["Color"], r["Factory"], r["PowerSupply"], r["ProductionYear"], r["PurchaseStatus"], serviceStatus)
        return re
        

