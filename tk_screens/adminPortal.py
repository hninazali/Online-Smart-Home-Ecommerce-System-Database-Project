import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
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
LARGEFONT = ("Verdana", 35)

class AdminPortal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.domain = tk.StringVar(self)
        self.controller = controller

        # Reset Button
        self.resetButton = ttk.Button(self)
        self.resetButton.configure(text='Reset SQLDB')
        self.resetButton.grid(column='4', padx='5', pady='5', row='1')
        self.resetButton.bind('<1>', self.resetDB, add='')

        createAdminButton = ttk.Button(self, text="Create New Admin",
                             command=lambda: controller.show_frame(CreateAdminPage, self.domain))
        createAdminButton.grid(row=6, column=4, padx=10, pady=10)

        options = ("Inventory Level", "Items Under Service", "Customers with Unpaid Service Fees")

        dropdownlist = ttk.OptionMenu(self, self.domain, options[0], *options)

        dropdownlist.grid(row=1, column=1, padx=10, pady=10)

        button1 = ttk.Button(self, text="Display",
                             command=self.display)
        button1.grid(row=1, column=2, padx=10, pady=10)

        button2 = ttk.Button(self, text="Search Product",
                             command=lambda: controller.show_frame(AdminProductSearch))
        button2.grid(row=2, column=4, padx=10, pady=10)

        button3 = ttk.Button(self, text="Search Item",
                             command=lambda: controller.show_frame(AdminItemSearch))
        button3.grid(row=3, column=4, padx=10, pady=10)

        button4 = ttk.Button(self, text="Advanced Search",
                             command=lambda: controller.show_frame(AdminAdvancedSearch))
        button4.grid(row=4, column=4, padx=10, pady=10)

        self['background']='#F6F4F1'

        self.treeFrame= ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='300')
        self.treeFrame.grid(column='2', columnspan='6', row='6', rowspan='1')

        cols = ('Product ID', 'Sold', 'Unsold')
        
        self.tree = ttk.Treeview(self.treeFrame, columns = cols,show='headings')

        self.tree.pack(side='left')
        self.scroll_y = Scrollbar(self.treeFrame, orient = 'vertical', command = self.tree.yview)
        self.scroll_y.pack(side = RIGHT, fill = Y)
        self.tree.configure(yscrollcommand = self.scroll_y.set)

        self.renderInventoryList()
        

        self['background']='#F6F4F1'

    def hello(self):
        print("hello")

    def menuBar(self,root):
        menubar = tk.Menu(root)
        # self.controller = controller
        # nestedProductMenu = tk.Menu(self)
        # nestedItemMenu = tk.Menu(self)
        # nestedRequestMenu = tk.Menu(self)
        # nestedServiceMenu = tk.Menu(self)
        # nestedProfileMenu = tk.Menu(self)

        #product
        productMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Products", menu=productMenu)
        productMenu.add_command(label="Simple Search", command=lambda: controller.show_frame(AdminProductSearch))
        productMenu.add_command(label="Advanced Search", command=lambda: controller.show_frame(AdminAdvancedSearch))
        # productMenu.add_cascade(label="hehehe", menu=nestedProductMenu) #only for adding more nested menus to menus


        #items
        itemMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Items", menu=itemMenu)
        itemMenu.add_command(label="View Items", command=lambda: controller.show_frame(AdminItemSearch))
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

    def display(self):
        if self.domain.get() == "Items Under Service":
            self.renderItemService()
        elif self.domain.get() == "Customers with Unpaid Service Fees":
            self.renderCustWithFee()
        elif self.domain.get() == "Inventory Level":
            self.renderInventoryList()

    def renderInventoryList(self):
        self.tree.destroy()
        self.scroll_y.destroy()
        cols = ('Product ID', 'Sold', 'Unsold')
        
        self.tree = ttk.Treeview(self.treeFrame, columns = cols,show='headings')
        self.produceTree(cols, "inventory")

    def renderItemService(self):
        self.tree.destroy()
        self.scroll_y.destroy()
        cols = ('Product ID', 'Category', 'Model', 'Service Status', 'Admin Assigned')
        
        self.tree = ttk.Treeview(self.treeFrame, columns = cols,show='headings')
        self.produceTree(cols, "service")

    def renderCustWithFee(self):
        self.tree.destroy()
        self.scroll_y.destroy()
        cols = ('Customer ID', 'Name', 'Email', 'Request ID', 'Amount ($)', 'Days left for Payment')
        self.tree = ttk.Treeview(self.treeFrame, columns = cols, show='headings')
        self.produceTree(cols, "fee")

    def produceTree(self, cols, func):
        w = tk.IntVar(self)
        res = []
        if func == "inventory":
            w = 240
            resSold = mongo.soldLevel()
            resUnsold = mongo.unsoldLevel()
            self.inventoryTable(w, cols, resSold, resUnsold)
        elif func == "service":
            w = 144
            res = db.itemUnderService()
            self.normalTable(w, cols, res)
        else:
            w = 120
            res = db.custWithUnpaidFees()
            self.normalTable(w, cols, res)

    def inventoryTable(self, w, cols, resSold, resUnsold):
        for index, unsold in enumerate(resUnsold):
            resSold[index]["unsold"] = unsold["total"]
            print(resSold)
        for col in cols:
            self.tree.column(col, anchor="center", width=w)
            self.tree.heading(col, text=col)
        for r in resSold:
            r = self.mongoToTree(r)
            self.tree.insert("", "end", values=r)
        self.tree.pack(side='left')
        self.scroll_y = Scrollbar(self.treeFrame, orient = 'vertical', command = self.tree.yview)
        self.scroll_y.pack(side = RIGHT, fill = Y)
        self.tree.configure(yscrollcommand = self.scroll_y.set)

    def normalTable(self, w, cols, res):
        print(res)
        for col in cols:
            self.tree.column(col, anchor="center", width=w)
            self.tree.heading(col, text=col)
        for r in res:
            self.tree.insert("", "end", values=r)
        self.tree.pack(side='left')
        self.scroll_y = Scrollbar(self.treeFrame, orient = 'vertical', command = self.tree.yview)
        self.scroll_y.pack(side = RIGHT, fill = Y)
        self.tree.configure(yscrollcommand = self.scroll_y.set)
        
        # self.setScrollbar()

    # def setScrollbar(self):
    #     self.tree.pack(side='left')
    #     scroll_y = Scrollbar(self.treeFrame, orient = 'vertical', command = self.tree.yview)
    #     scroll_y.pack(side = RIGHT, fill = Y)
    #     self.tree.configure(yscrollcommand = scroll_y.set)
    
    def mongoToTree(self, r):
        re = (r["_id"], r["total"], r["unsold"])
        return re

    def resetDB(self):
        db.resetMySQLState()
        db.dataInit()

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


