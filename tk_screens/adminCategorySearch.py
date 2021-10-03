import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label
from db_connections.mysqldb import SQLDatabase
from PIL import Image, ImageTk
db = SQLDatabase()

LARGEFONT = ("Verdana", 35)

class AdminCategorySearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.category = tk.StringVar(self)
        # self.model = tk.StringVar(self)

        # Dropdown menu options
        # Will have to be dynamic
        optionsCategory = ("Lights", "Locks")
        # optionsModel = ("Light1", "Light2", "SmartHome1", "Safe1", "Safe2", "Safe3")

        categoryListLabel = ttk.Label(self, text="Filter by category:")
        categoryListLabel.grid(row=3, column=1, padx=10, pady=10)
        categoryList = ttk.OptionMenu(self, self.category, optionsCategory[0], *optionsCategory)
        categoryList.grid(row=3, column=2, sticky=tk.E, padx=10, pady=10)
        button2 = ttk.Button(self, text="Filter",
                             command=self.renderProductsList)
        button2.grid(row=3, column=3, padx=10, pady=10)

        label = tk.Label(self, text="Products List").grid(row=5, columnspan=3)
        
        # Treeview to show product result based on filter
        global cols
        cols = ('Product ID', 'Category', 'Model', 'Price', 'Cost', 'Warranty (months)', 'Inventory Level', 'Number sold')

        global tree
        tree = ttk.Treeview(self, columns=cols, show='headings')

        res = db.adminCategorySearch(self.category.get())
        for col in cols:
            tree.column(col, anchor="center", width=150)
            tree.heading(col, text=col)
        for r in  res:
            tree.insert("", "end", values=r)
        tree.grid(row=6, column=1, columnspan=2)
        tree.bind("<ButtonRelease-1>", self.clicker)

        # Attach scrollbar to treeview
        # Scrollbar only works if there are many items (can duplicate line 48-49 to try it out if amount of data is not sufficient)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=3, sticky="ns")

    def renderProductsList(self):
        # Delete existing data from table
        for r in tree.get_children():
            tree.delete(r)

        # Get data from db
        res = db.adminCategorySearch(self.category.get())

        # Set heading and load new data results
        for col in cols:
            tree.heading(col, text=col)
        for r in res:
            tree.insert("", "end", values=r)

        tree.grid(row=6, column=1, columnspan=2)

    # When a row is  clicked, this method will get the item from the selected row
    def clicker(self, event):
        # Grab record number
        selected = tree.focus()
        # Grab record values
        values = tree.item(selected, 'values')
        # Can use the return value to query data eg values[0] returns itemID
        print(values)

        

