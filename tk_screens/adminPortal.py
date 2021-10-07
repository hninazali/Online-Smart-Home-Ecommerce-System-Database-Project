import tkinter as tk
from tkinter import *
from tkinter import ttk
from db_connections.mysqldb import SQLDatabase

db = SQLDatabase()

class AdminPortal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # self.domain = tk.StringVar(self)

    def menuBar(self,root):
        menubar = tk.Menu(self)
        productMenu = tk.Menu(self)
        itemMenu = tk.Menu(self)
        requestMenu = tk.Menu(self)
        serviceMenu = tk.Menu(self)
        profileMenu = tk.Menu(self)
        nestedProductMenu = tk.Menu(self)
        nestedItemMenu = tk.Menu(self)
        nestedRequestMenu = tk.Menu(self)
        nestedServiceMenu = tk.Menu(self)
        nestedProfileMenu = tk.Menu(self)


        menubar.add_cascade(label="Products", menu=productMenu)
        productMenu.add_cascade(label="hehehe", menu=nestedProductMenu)
            # menubar.add_separator()
        menubar.add_cascade(label="Items", menu=itemMenu)
        itemMenu.add_cascade(label="wowooow",menu=nestedItemMenu)

        menubar.add_cascade(label="Service Requests", menu=requestMenu)
        requestMenu.add_cascade(label="heloooo", menu=nestedRequestMenu)

        menubar.add_cascade(label="Services", menu=serviceMenu)
        serviceMenu.add_cascade(label="yayy", menu=nestedServiceMenu)

        menubar.add_cascade(label="My Profile", menu=profileMenu)
        profileMenu.add_cascade(label="View Profile", menu=nestedProfileMenu)
        return menubar


        # Reset Button
        resetButton = ttk.Button(self, text="Reset SQLDB", command=self.resetDB)
        resetButton.grid(row=0, column=1, padx=10, pady=10)
        
        #  Dummy Display 
        # options = ("Customer", "Administrator")

        # dropdownlist = ttk.OptionMenu(self, self.domain, options[0], *options)
        
        # dropdownlist.grid(row=1, column=1, padx=10, pady=10)

    def resetDB(self):
        db.resetMySQLState()
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