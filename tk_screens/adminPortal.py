import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, Entry, LabelFrame
from db_connections.mysqldb import SQLDatabase
from tk_screens.adminProductSearch import AdminProductSearch 
from tk_screens.adminItemSearch import AdminItemSearch

db = SQLDatabase()

class AdminPortal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.domain = tk.StringVar(self)

        self.wrapper1 = LabelFrame(self, text="Header")
        self.wrapper2 = LabelFrame(self, text="Display List")

        self.wrapper1.pack(fill=tk.X)
        self.wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)

        # Reset Button
        resetButton = ttk.Button(self.wrapper1, text="Reset SQLDB", command=self.resetDB)
        resetButton.grid(row=0, column=1, padx=10, pady=10)
        #  Dummy Display 
        options = ("Inventory Level", "Items Under Service", "Customers with Unpaid Service Fees")

        dropdownlist = ttk.OptionMenu(self.wrapper1, self.domain, options[0], *options)
        
        dropdownlist.grid(row=1, column=1, padx=10, pady=10)

        button1 = ttk.Button(self.wrapper1, text="Display",
                             command=self.display)
        button1.grid(row=1, column=2, padx=10, pady=10)

        self.renderInventoryList()

        button2 = ttk.Button(self.wrapper1, text="Search Product",
                             command=lambda: controller.show_frame(AdminProductSearch))
        button2.grid(row=0, column=2, padx=10, pady=10)

        button3 = ttk.Button(self.wrapper1, text="Search Item",
                             command=lambda: controller.show_frame(AdminItemSearch))
        button3.grid(row=0, column=3, padx=10, pady=10)

        button4 = ttk.Button(self.wrapper1, text="Advanced Search",
                             command=lambda: controller.show_frame(AdvancedSearch))
        button4.grid(row=0, column=3, padx=10, pady=10)

    def display(self):
        if self.domain.get() == "Items Under Service":
            self.renderItemService()
        elif self.domain.get() == "Customers with Unpaid Service Fees":
            self.renderCustWithFee()
        elif self.domain.get() == "Inventory Level":
            self.renderInventoryList()

    def renderInventoryList(self):
        # Get data from mongo
        # res = mongo.inventoryList()
        cols = ('Item ID', 'Sold', 'Unsold')
        tree = ttk.Treeview(self.wrapper2, columns=cols, show='headings', height="6")
        for col in cols:
            tree.column(col, anchor="center", width=240)
            tree.heading(col, text=col)
        tree.grid(row=6, column=1, columnspan=1)

        scrollbar = ttk.Scrollbar(self.wrapper2, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=2, sticky="ns")

    def renderItemService(self):
        # Get data from db
        res = db.itemUnderService()

        # Set heading and load new data results
        cols = ('Item ID', 'Category', 'Model', 'Service Status', 'Admin Assigned')
        tree = ttk.Treeview(self.wrapper2, columns=cols, show='headings', height="6")
        for col in cols:
            tree.column(col, anchor="center", width=144)
            tree.heading(col, text=col)
        for r in res:
            tree.insert("", "end", values=r)

        tree.grid(row=6, column=1, columnspan=1)

    def renderCustWithFee(self):
        
        # Get data from db
        cols = ('Customer ID', 'Name', 'Email', 'Request ID', 'Amount ($)', 'Days left for Payment')
        tree = ttk.Treeview(self.wrapper2, columns=cols, show='headings', height="6")
        res = db.custWithUnpaidFees()

        # Set heading and load new data results
        for col in cols:
            tree.column(col, anchor="center", width=120)
            tree.heading(col, text=col)
        for r in res:
            tree.insert("", "end", values=r)

        tree.grid(row=6, column=1, columnspan=1)

    def resetDB(self):
        db.resetMySQLState()
        db.dataInit()
# In addition, provide a MYSQL database initialization function under the Administrator login. 
# At the beginning of your  presentation, you are required to apply this function to reinitialize the MYSQL database. 
# When the MYSQL database is initialized,  provide a function to allow the Administrator to display the following information (Purchase status= “SOLD” and  Purchase status=“UNSOLD”) on the items in the MySQL tables:


# Winy can try with her table code too

 # table = Table(parent= parent,columns=("FName", "LName", "Roll No"))
        # table.insertRow(('Amit', 'Kumar', '17701'))
        # table.insertRow(('Ankush', 'Mathur', '17702'))
        # tree = table.getTree()
        # tree.grid(row=4, column=1, padx=10, pady=10)

# class Table:
#     def __init__(self, parent, columns, num_visible_rows=5):
#         self.tree = ttk.Treeview(parent, column=columns, show='headings', height=num_visible_rows)
#         self.tree.column("# 1", anchor="center")
#         self.tree.heading("# 1", text="FName")
#         self.tree.column("# 2", anchor="center")
#         self.tree.heading("# 2", text="LName")
#         self.tree.column("# 3", anchor="center")
#         self.tree.heading("# 3", text="Roll No")


#     def insertRow(self, values):
#         self.tree.insert('', 'end', text="1", values=values)

#     def getTree(self):
#         return self.tree