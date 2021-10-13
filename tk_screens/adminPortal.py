import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import *
from tkinter import ttk, messagebox, PhotoImage, Label, Entry, Menu
from db_connections.mysqldb import SQLDatabase
from tk_screens.adminApproveRequestsPage import AdminApproveRequestsPage
from tk_screens.adminCompleteServicesPage import AdminCompleteServicesPage
# from tk_screens.adminProductSearch import AdminProductSearch 
# from tk_screens.adminItemSearch import AdminItemSearch
# from tk_screens.adminAdvancedSearch import AdminAdvancedSearch
from tk_screens.viewProfileWindow import ViewProfileWindow
from db_connections.mongodb import MongoDB
from tk_screens.changePasswordWindow import ChangePasswordWindow
from PIL import Image, ImageTk

mongo = MongoDB()
# mongo.dropCollection("items")
# mongo.dropCollection("products")
# mongo.resetMongoState()
db = SQLDatabase()

LARGEFONT = ("Calibri", 35, "bold")

class AdminPortal(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.domain = controller.getDomain()
        self.adminFunc = tk.StringVar(self)
        self.controller = controller
        self.userID = None
        self.domain = None

        self.label = ttk.Label(self, text="Admin Home", font=LARGEFONT)
        self.label.grid(row=0, column=3, padx=10, pady=10)

        # Reset Button
        self.resetButton = ttk.Button(self, text="Reset Database",
                             command=self.resetDB)
        self.resetButton.grid(row=1, column=6,padx=10, pady=10)
        # self.resetButton.grid(column='6', padx='5', pady='5', row='1')
        # self.resetButton.bind('<1>', self.resetDB, add='')

        createAdminButton = ttk.Button(self, text="Create New Admin",
                             command=lambda: controller.show_frame(CreateAdminPage, self.domain))
        createAdminButton.grid(row=2, column=6, padx=10, pady=10)

        options = ("Inventory Level", "Items Under Service", "Customers with Unpaid Service Fees")

        dropdownlist = ttk.OptionMenu(self, self.adminFunc, options[0], *options)

        dropdownlist.grid(row=1, column=1, padx=10, pady=10)

        button1 = ttk.Button(self, text="Display",
                             command=self.display)
        button1.grid(row=1, column=2, padx=10, pady=10)

        button2 = ttk.Button(self, text="Search Product",
                             command=lambda: controller.show_frame(AdminProductSearch))
        button2.grid(row=3, column=6, padx=10, pady=10)

        button3 = ttk.Button(self, text="Search Item",
                             command=lambda: controller.show_frame(AdminItemSearch))
        button3.grid(row=4, column=6, padx=10, pady=10)

        button4 = ttk.Button(self, text="Advanced Search",
                             command=lambda: controller.show_frame(AdminAdvancedSearch))
        button4.grid(row=5, column=6, padx=10, pady=10)

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

        # Approve requests button
        self.approveButton = ttk.Button(self, text="Approve Requests", command= lambda: controller.show_frame(AdminApproveRequestsPage, self.domain, self.userID))
        self.approveButton.grid(column=2, pady=5, padx=10, row=2)

        # Complete services button
        self.completeButton = ttk.Button(self, text="Complete Services", command= lambda: controller.show_frame(AdminCompleteServicesPage, self.domain, self.userID))
        self.completeButton.grid(column=2, pady=5, padx=10, row=3)
        

        self['background']='#F6F4F1'

    def hello(self):
        print("hello")
        print(self.userID)
        print(self.domain)
        

    def handleLogout(self):
        self.controller.logout()
    
    def menuBar(self,root):
        menubar = tk.Menu(root)
        # self.controller = controller
        # nestedProductMenu = tk.Menu(self)
        # nestedItemMenu = tk.Menu(self)
        # nestedRequestMenu = tk.Menu(self)
        # nestedServiceMenu = tk.Menu(self)
        # nestedProfileMenu = tk.Menu(self)

        #back to admin main portal
        
        #product
        productMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Products", menu=productMenu)
        productMenu.add_command(label="Simple Search", command=lambda: self.controller.show_frame(AdminProductSearch))
        productMenu.add_command(label="Advanced Search", command=lambda: self.controller.show_frame(AdminAdvancedSearch))
        # productMenu.add_cascade(label="hehehe", menu=nestedProductMenu) #only for adding more nested menus to menus


        #items
        itemMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Items", menu=itemMenu)
        itemMenu.add_command(label="View Items", command=lambda: self.controller.show_frame(AdminItemSearch))
        # itemMenu.add_cascade(label="wowooow",menu=nestedItemMenu)
        
        #service requests
        requestMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Service Requests", menu=requestMenu)
        requestMenu.add_command(label="View Service Requests", command=lambda: self.controller.show_frame(AdminApproveRequestsPage, self.domain, self.userID))
    #     requestMenu.add_cascade(label="heloooo", menu=nestedRequestMenu)

        #service 
        serviceMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Services", menu=serviceMenu)
        serviceMenu.add_command(label="View Services", command=lambda: self.controller.show_frame(AdminCompleteServicesPage, self.domain, self.userID))
        # serviceMenu.add_cascade(label="yayy", menu=nestedServiceMenu)

        #profile
        profileMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="My Profile", menu=profileMenu)
        profileMenu.add_command(label="View Profile", command=lambda: ViewProfileWindow(master=self.controller))
        profileMenu.add_command(label="Change Password", command= lambda: ChangePasswordWindow(master=self.controller))
        profileMenu.add_separator()
        profileMenu.add_command(label="Logout", command=self.handleLogout)      
        
        return menubar

    def display(self):
        if self.adminFunc.get() == "Items Under Service":
            self.renderItemService()
        elif self.adminFunc.get() == "Customers with Unpaid Service Fees":
            self.renderCustWithFee()
        elif self.adminFunc.get() == "Inventory Level":
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
        cols = ('Item ID', 'Category', 'Model', 'Service Status', 'Admin Assigned')
        
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
            print("inventoryTable:",resSold)
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
        print("normalTable:",res)
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
        print("Reloading databases")
        db.resetMySQLState()
        items, products = mongo.convertMongotoSQL()
        db.loadMongo(items, products)
        messagebox.showinfo(title="Reset Database Success", message= "Success! The database is reset!")

    def setUserType(self, userID):
        self.domain = userID
        # Log
        print("gui.py>AdminPortalPage> Domain Set:",self.domain.get())
        

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

class AdminItemSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.itemID = tk.StringVar()
        self['background']='#F6F4F1'

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(AdminPortal))
        button1.grid(row=0, column=1, padx=5, pady=5)

        label = ttk.Label(self, text="Items List", font=LARGEFONT)
        label.grid(row=0, column=3, padx=10, pady=10)

        itemIDLabel = ttk.Label(self, text="Item ID:")
        itemIDLabel.grid(row=1, column=1, padx=10, pady=10)

        itemIDInput = ttk.Entry(self, textvariable=self.itemID)
        itemIDInput.grid(row=1, column=2, padx=10, pady=10)

        button1 = ttk.Button(self, text="Filter",
                             command=self.renderItemsList)
        button1.grid(row=1, column=3, padx=10, pady=10)

        self.treeFrame= ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='300')
        self.treeFrame.grid(column='2', columnspan='6', row='6', rowspan='1')

        self.cols = ('Item ID', 'Model', 'Category', 'Color', 'Factory', 'Power Supply', 'Production Year', 'Purchase Status', 'Service Status')

        self.tree = ttk.Treeview(self.treeFrame, columns = self.cols,show='headings')
        self.tree.pack(side='left')
        scroll_y = Scrollbar(self.treeFrame, orient = 'vertical', command = self.tree.yview)
        scroll_y.pack(side = RIGHT, fill = Y)
        self.tree.configure(yscrollcommand = scroll_y.set)
        
        res = mongo.findItemByID(self.itemID.get())
        for col in self.cols:
            self.tree.column(col, anchor="center", width=80)
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
    
class AdminProductSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.category = tk.StringVar(self)
        self.model = tk.StringVar(self)
        
        self['background']='#F6F4F1'

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(AdminPortal))
        button1.grid(row=0, column=1, padx=5, pady=5)

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
        self.treeFrame.grid(column='2', columnspan='6', row='6', rowspan='1')

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

class AdminAdvancedSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Products List", font=LARGEFONT)
        label.grid(row=0, column=3, padx=10, pady=10)

        self['background']='#F6F4F1'

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(AdminPortal))
        button1.grid(row=0, column=1, padx=5, pady=5)

        self.priceBox = ttk.Combobox(self ,values = ["50", "60",
        "70","100","120","125","200",""])
        self.priceBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.priceBox.grid(column='2', padx='5', pady='5', row='2')
        
        self.colorBox = ttk.Combobox(self, values = ["White", "Blue",
        "Yellow", "Green", "Black",""])
        self.colorBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.colorBox.grid(column='2', padx='5', pady='5', row='3')

        self.factoryBox = ttk.Combobox(self, values = ["Malaysia", "China", "Philippines",""])
        self.factoryBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.factoryBox.grid(column='2', padx='5', pady='5', row='4')

        self.productionYearBox = ttk.Combobox(self, values = ["2014", "2015",
        "2016", "2017", "2018", "2019", "2020",""])
        self.productionYearBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.productionYearBox.grid(column='2', padx='5', pady='5', row='5')

        self.powerSupplyBox = ttk.Combobox(self, values = ["Battery", "USB",""])
        self.powerSupplyBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.powerSupplyBox.grid(column='2', padx='5', pady='5', row='6')

        self.advancedSearchButton = ttk.Button(self, text="Filter", command=self.search)
        self.advancedSearchButton.grid(column='3', padx='5', pady='5', row='6')

        self.priceLabel = ttk.Label(self)
        self.priceLabel.configure(text='Price')
        self.priceLabel.grid(column='1', padx='5', pady='5', row='2')

        self.colorLabel = ttk.Label(self)
        self.colorLabel.configure(text='Color')
        self.colorLabel.grid(column='1', padx='5', pady='5', row='3')

        self.factoryLabel = ttk.Label(self)
        self.factoryLabel.configure(text='Factory')
        self.factoryLabel.grid(column='1', padx='5', pady='5', row='4')

        self.productionYearLabel = ttk.Label(self)
        self.productionYearLabel.configure(text='Production Year')
        self.productionYearLabel.grid(column='1', padx='5', pady='5', row='5')

        self.powerSupplyLabel = ttk.Label(self)
        self.powerSupplyLabel.configure(text='Power Supply')
        self.powerSupplyLabel.grid(column='1', padx='5', pady='5', row='6')

        self.treeFrame= ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='300')
        self.treeFrame.grid(column='2', columnspan='6', row='7', rowspan='1')

        self.cols = ("Item ID", "Category", "Model", "Price", "Cost", "Color", "Factory", "Warranty", "Production Year", "Power Supply", "Purchase Status", "Service Status")

        self.tree = ttk.Treeview(self.treeFrame, columns = self.cols,show='headings')
        self.tree.pack(side='left')
        scroll_y = Scrollbar(self.treeFrame, orient = 'vertical', command = self.tree.yview)
        scroll_y.pack(side = RIGHT, fill = Y)
        self.tree.configure(yscrollcommand = scroll_y.set)
        
        for col in self.cols:
            self.tree.column(col, anchor="center", width=100)
            self.tree.heading(col, text=col)

        res = mongo.adminAdvancedSearch(self.mongoSearch())
        for r in  res:
            result = self.mongoToTree(r)
            self.tree.insert("", "end", values=result)
    
    def search(self):
        for r in self.tree.get_children():
            self.tree.delete(r)

        for col in self.cols:
            self.tree.heading(col, text=col)

        stringsearch = self.mongoSearch()
        allrecordsList = mongo.adminAdvancedSearch(stringsearch)
        messagebox.showinfo(title="Search Results", message= "{} items available based on your search!".format(len(allrecordsList)))

        if len(allrecordsList) == 0:
            pass
        else:
            for record in allrecordsList:
                result = self.mongoToTree(record)
                self.tree.insert("", "end", values=result)

    def mongoSearch(self):
        mongoSearch = ""

        price =  self.priceBox.get()
        color = self.colorBox.get()
        factory = self.factoryBox.get()
        productionYear = self.productionYearBox.get()
        powerSupply = self.powerSupplyBox.get()
        category = ""
        model = ""

        if price:
            catandmod = self.findModelfromPrice(price)
            if category and category != catandmod[0]:
                category = "no output"
            if model and model != catandmod[1]:
                model = "no output"
            else:
                category = catandmod[0]
                model = catandmod[1]   
        dictSearch = {}   

        if category:
             dictSearch["Category"] = category
        if model:
            dictSearch["Model"] = model
        if color:
             dictSearch["Color"] = color
        if factory:
            dictSearch["Factory"] = factory
        if productionYear:
            dictSearch["ProductionYear"] = productionYear
        if powerSupply:
            dictSearch["PowerSupply"] = powerSupply
        return dictSearch

    def findModelfromPrice(self, price):
        product = mongo.findModelfromPrice(price)
        Category = product["Category"]
        Model = product["Model"]
        return (Category, Model)

    def mongoToTree(self, r):
        # To get price, cost, warranty from product (not avail in item)
        pcw = mongo.findPriceCostWarranty(r["Category"], r["Model"])
        re = (r["ItemID"], r["Category"], r["Model"], pcw["Price"], pcw["Cost"], r["Color"], r["Factory"], pcw["Warranty"], r["ProductionYear"], r["PowerSupply"], r["PurchaseStatus"], r["ServiceStatus"])
        return re

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


