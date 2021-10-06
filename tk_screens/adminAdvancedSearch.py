import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, LabelFrame
from db_connections.mongodb import MongoDB
from PIL import Image, ImageTk
mongo = MongoDB()
mongo.dropCollection("items")
mongo.dropCollection("products")
mongo.resetMongoState()

LARGEFONT = ("Verdana", 35)

class AdminAdvancedSearch(tk.Frame):
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

        categoryListLabel = ttk.Label(wrapper1, text="Category:")
        categoryListLabel.grid(row=1, column=0, padx=10, pady=10)
        categoryList = ttk.OptionMenu(wrapper1, self.category, optionsCategory[0], *optionsCategory)
        categoryList.grid(row=1, column=1, sticky=tk.E, padx=10, pady=10)

        modelListLabel = ttk.Label(wrapper1, text="Model:")
        modelListLabel.grid(row=2, column=0, padx=10, pady=10)
        modelList = ttk.OptionMenu(wrapper1, self.model, optionsModel[0], *optionsModel)
        modelList.grid(row=2, column=1, sticky=tk.E, padx=10, pady=10)

        button2 = ttk.Button(wrapper1, text="Filter",
                             command=self.renderProductsList)
        button2.grid(row=3, column=1, padx=10, pady=10)

        
        # Treeview to show product result based on filter
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
        tree.bind("<ButtonRelease-1>", self.clicker)

        # Attach scrollbar to treeview
        # Scrollbar only works if there are many items (can duplicate line 48-49 to try it out if amount of data is not sufficient)
        scrollbar = ttk.Scrollbar(wrapper2, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=2, sticky="ns")

    def renderProductsList(self):
        # Delete existing data from table
        for r in tree.get_children():
            tree.delete(r)

        # Get data from db
        res = mongo.adminProductSearch(self.category.get(), self.model.get())

        # Set heading and load new data results
        for col in cols:
            tree.heading(col, text=col)
        for r in res:
            result = self.mongoToTree(r)
            tree.insert("", "end", values=result)

        tree.grid(row=6, column=1, columnspan=1)


    def mongoToTree(self, r):
        re = (r["ProductID"], r["Category"], r["Model"], r["Price ($)"], r["Cost ($)"], r["Warranty (months)"])
        return re