import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, Entry, LabelFrame, IntVar
from db_connections.mysqldb import SQLDatabase
from tk_screens.adminProductSearch import AdminProductSearch 
from tk_screens.adminItemSearch import AdminItemSearch
from tk_screens.adminAdvancedSearch import AdminAdvancedSearch
from db_connections.mongodb import MongoDB
from PIL import Image, ImageTk
mongo = MongoDB()
mongo.dropCollection("items")
mongo.dropCollection("products")
mongo.resetMongoState()
db = SQLDatabase()


class AdminPortal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.domain = tk.StringVar(self)
        self.controller = controller

        self.wrapper1 = LabelFrame(self, text="Header")
        self.wrapper2 = LabelFrame(self, text="Display List")

        self.wrapper1.pack(fill=tk.X)
        self.wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)

        # Reset Button
        resetButton = ttk.Button(self, text="Reset SQLDB", command=self.resetDB)
        resetButton.grid(row=3, column=6, padx=10, pady=10)


        createAdminButton = ttk.Button(self, text="Create New Admin",
                             command=lambda: controller.show_frame(CreateAdminPage, self.domain))

        createAdminButton.grid(row=3, column=7, padx=10, pady=10)


    def hello(self):
        print("hello")
    
    def menuBar(self,root):
        menubar = tk.Menu(root)
        # nestedProductMenu = tk.Menu(self)
        # nestedItemMenu = tk.Menu(self)
        # nestedRequestMenu = tk.Menu(self)
        # nestedServiceMenu = tk.Menu(self)
        # nestedProfileMenu = tk.Menu(self)

        #product
        productMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Products", menu=productMenu)
        productMenu.add_command(label="View Products", command=self.hello)
        # productMenu.add_cascade(label="hehehe", menu=nestedProductMenu) #only for adding more nested menus to menus


        #items
        itemMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Items", menu=itemMenu)
        itemMenu.add_command(label="View Items", command=self.hello)
        # itemMenu.add_cascade(label="wowooow",menu=nestedItemMenu)
        
        #service requests
        requestMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Service Requests", menu=requestMenu)
        requestMenu.add_command(label="View Service Requests", command=self.hello)
    #     requestMenu.add_cascade(label="heloooo", menu=nestedRequestMenu)

        #service 
        serviceMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Services", menu=requestMenu)
        serviceMenu.add_command(label="View Services", command=self.hello)
        # serviceMenu.add_cascade(label="yayy", menu=nestedServiceMenu)

        #profile
        profileMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="My Profile", menu=profileMenu)
        profileMenu.add_command(label="View Profile", command=self.hello)
        profileMenu.add_separator()
        profileMenu.add_command(label="Logout", command=self.hello)      
        
        return menubar


        # button1 = ttk.Button(self.wrapper1, text="Display",
        #                      command=self.display)
        # button1.grid(row=1, column=2, padx=10, pady=10)

        # self.renderInventoryList()

        # button2 = ttk.Button(self.wrapper1, text="Search Product",
        #                      command=lambda: controller.show_frame(AdminProductSearch))
        # button2.grid(row=0, column=2, padx=10, pady=10)

        # button3 = ttk.Button(self.wrapper1, text="Search Item",
        #                      command=lambda: controller.show_frame(AdminItemSearch))
        # button3.grid(row=0, column=3, padx=10, pady=10)

        # button4 = ttk.Button(self.wrapper1, text="Advanced Search",
        #                      command=lambda: controller.show_frame(AdminAdvancedSearch))
        # button4.grid(row=0, column=4, padx=10, pady=10)

    def display(self):
        if self.domain.get() == "Items Under Service":
            self.renderItemService()
        elif self.domain.get() == "Customers with Unpaid Service Fees":
            self.renderCustWithFee()
        elif self.domain.get() == "Inventory Level":
            self.renderInventoryList()

    def renderInventoryList(self):
        cols = ('Item ID', 'Sold', 'Unsold')
        tree = ttk.Treeview(self.wrapper2, columns=cols, show='headings', height="6")
        self.produceTree(cols, "inventory",tree)

    def renderItemService(self):
        cols = ('Item ID', 'Category', 'Model', 'Service Status', 'Admin Assigned')
        tree = ttk.Treeview(self.wrapper2, columns=cols, show='headings', height="6")
        self.produceTree(cols, "service", tree)

    def renderCustWithFee(self):
        cols = ('Customer ID', 'Name', 'Email', 'Request ID', 'Amount ($)', 'Days left for Payment')
        tree = ttk.Treeview(self.wrapper2, columns=cols, show='headings', height="6")
        self.produceTree(cols, "fee", tree)

    def produceTree(self, cols, func, tree):
        w = tk.IntVar(self)
        res = []
        if func == "inventory":
            w = 240
            resSold = mongo.soldLevel()
            resUnsold = mongo.unsoldLevel()
            self.inventoryTable(w, cols, tree, resSold, resUnsold)
        elif func == "service":
            w = 144
            res = db.itemUnderService()
            self.normalTable(w, cols, tree, res)
        else:
            w = 120
            res = db.custWithUnpaidFees()
            self.normalTable(w, cols, tree, res)

    def inventoryTable(self, w, cols, tree, resSold, resUnsold):
        for index, unsold in enumerate(resUnsold):
            resSold[index]["unsold"] = unsold["total"]
            print(resSold)
        for col in cols:
            tree.column(col, anchor="center", width=w)
            tree.heading(col, text=col)
        for r in resSold:
            r = self.mongoToTree(r)
            tree.insert("", "end", values=r)

        tree.grid(row=6, column=1, columnspan=1)
        self.setScrollbar(tree)

    def normalTable(self, w, cols, tree, res):
        for col in cols:
            tree.column(col, anchor="center", width=w)
            tree.heading(col, text=col)
        for r in res:
            tree.insert("", "end", values=r)

        tree.grid(row=6, column=1, columnspan=1)
        self.setScrollbar(tree)

    def setScrollbar(self,tree):
        scrollbar = ttk.Scrollbar(self.wrapper2, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=2, sticky="ns")
    
    def mongoToTree(self, r):
        re = (r["_id"], r["total"], r["unsold"])
        return re

    def resetDB(self):
        db.resetMySQLState()
        db.dataInit()
# In addition, provide a MYSQL database initialization function under the Administrator login. 
# At the beginning of your  presentation, you are required to apply this function to reinitialize the MYSQL database. 
# When the MYSQL database is initialized,  provide a function to allow the Administrator to display the following information (Purchase status= “SOLD” and  Purchase status=“UNSOLD”) on the items in the MySQL tables:
    
    # def logout(self):
    #     self.domain = tk.StringVar(self)
    #     self.controller.show_frame(StartPage)

class CreateAdminPage(tk.Frame):
    def __init__(self, parent, controller):
        self.domain = controller.getDomain()

        self.adminID = tk.StringVar()
        self.name = tk.StringVar()
        self.password = tk.StringVar()
        self.gender = tk.StringVar()   
        self.phoneNumber = tk.StringVar()
        

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Create new Admin", font=LARGEFONT)
        label.grid(row=2, column=3, padx=5, pady=5, columnspan=11)

        adminIDlabel = ttk.Label(self, text="Admin ID:")
        adminIDlabel.grid(row=3, column=3, padx=5, pady=5)

        adminIDInput = ttk.Entry(self, textvariable=self.adminID)
        adminIDInput.grid(row=3, column=4,  padx=5, pady=5)

        namelabel = ttk.Label(self, text="Name:")
        namelabel.grid(row=4, column=3, padx=5, pady=5)

        nameInput = ttk.Entry(self, textvariable=self.name)
        nameInput.grid(row=4, column=4,  padx=5, pady=5)

        passwordLabel = ttk.Label(self, text="Password:")
        passwordLabel.grid(row=6, column=3,  padx=5, pady=5)

        passwordInput = ttk.Entry(self,show="*", textvariable=self.password)
        passwordInput.grid(row=6, column=4,  padx=5, pady=5)

        genderLabel = ttk.Label(self, text="Gender:")
        genderLabel.grid(row=9, column=3,  padx=5, pady=5)

        genderOptions = ttk.OptionMenu(self, self.gender, 'M', *("M","F"))
        genderOptions.grid(row=9, column=4,  padx=5, pady=5)


        phoneNumberLabel = ttk.Label(self, text="Phone:")
        phoneNumberLabel.grid(row=8, column=3,  padx=5, pady=5)

        phoneNumberInput = ttk.Entry(self, textvariable=self.phoneNumber)
        phoneNumberInput.grid(row=8, column=4,  padx=5, pady=5)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Register",
                             command=self.handleRegister)

        # putting the button in its place by
        # using grid
        button1.grid(row=10, column=3,  padx=5, pady=5)

        # button to show frame 3 with text
        # layout3
        backToAdminPortalButton = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(AdminPortal))

        # putting the button in its place by
        # using grid
        backToAdminPortalButton.grid(row=10, column=4,  padx=5, pady=5)


    def setUserType(self,usertype):
        self.domain = usertype

    '''
    Returns True if any of the fields are empty.
    '''
    def checkEmptyField(self):
        for element in [self.adminID.get(), self.name.get(), self.password.get(), self.gender.get(), self.phoneNumber.get()]:
            if element=='' or element==' ':
                return True
        return False

    def handleRegister(self):        
        print("Register button clicked")
        # if self.domain.get()=="Administrator":
        if self.checkEmptyField():
            print("Incomeplete fields")
            messagebox.showerror(title="Registration Failed", message="Please fill in all fields")
        else:
            res = db.createAdmin([self.adminID.get(), self.name.get(), self.password.get(), self.gender.get(), self.phoneNumber.get()])
            if res : 
                messagebox.showerror(title="Registration Failed", message=res)
            else : 
                print("Register success")
                messagebox.showinfo(title="Registration Success", message= "Succesfully created an admin account!")



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


