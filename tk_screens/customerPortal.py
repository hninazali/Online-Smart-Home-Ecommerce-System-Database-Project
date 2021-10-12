import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from datetime import date
from db_connections.mysqldb import SQLDatabase
from db_connections.mongodb import MongoDB
from tk_screens.viewProfileWindow import ViewProfileWindow
from tk_screens.changePasswordWindow import ChangePasswordWindow
#connect to mongoDB to search
global client
global db
global products
mymongodb = MongoDB()
client = mymongodb.getClient()
db = client["oshes"]
products = db["products"]

LARGEFONT = ("Calibri", 35, "bold")

#connect to mysql database to register purchases
global con
mysqlinit = SQLDatabase()
con = mysqlinit.getConnection()

class CustomerPortal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.userID = None
        self.domain = None
    
        self.label = ttk.Label(self, text="Customer Home", font=LARGEFONT)
        self.label.grid(row=0, column=4, padx=10, pady=10)
        
        ####Buttons####
        # self.homeButton = ttk.Button(self)
        # self.homeButton.configure(text='Home')
        # self.homeButton.grid(column='1', padx='3', pady='3', row='1')

        self.searchButton = ttk.Button(self)
        self.searchButton.configure(text='Search')
        self.searchButton.grid(column='7', padx='5', pady='5', row='9')

        self.searchButton.bind('<1>', self.search, add='')

        self.buyButton = ttk.Button(self)
        self.buyButton.configure(text='Buy')
        self.buyButton.grid(column='7', pady='20', row='11', sticky='e')
        self.buyButton.bind('<Button-1>', self.buyItem)

        self['background']='#F6F4F1'

        print("user id to req page")
        print("======================")
        print(self.controller.getUserID())
        reqButton = ttk.Button(self, text="Requests List",
                             command=lambda: controller.show_frame(RequestsPage, domain = "Customer", userID = self.controller.getUserID()))
        reqButton.grid(row=2, column=8, padx=10, pady=10)

        ####Comboboxes####
        vModel=[]
        self.modelBox = ttk.Combobox(self, values = vModel)
        self.modelBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.modelBox.grid(column='4', padx='5', pady='5', row='3')

        #ensure that only the right model shows when category selected
        def categoryAndModel(event):
            if self.categoryBox.get()=="Lights":
                vModel = ["Light1", "Light2", "SmartHome1",""]
            elif self.categoryBox.get()=="Locks":
                vModel = ["Safe1", "Safe2", "Safe3", "SmartHome1",""]
            else:
                vModel = []
            self.modelBox.configure(values = vModel)


        self.categoryBox = ttk.Combobox(self, values = ["Lights", "Locks",""])
        self.categoryBox.bind('<<ComboboxSelected>>', categoryAndModel)
        self.categoryBox.configure(state='readonly')
        self.categoryBox.grid(column='4', padx='5', pady='5', row='2')
        
        self.priceBox = ttk.Combobox(self,values = ["50", "60",
        "70","100","120","125","200",""])
        self.priceBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.priceBox.grid(column='7', padx='5', pady='5', row='2')
        
        self.colorBox = ttk.Combobox(self, values = ["White", "Blue",
        "Yellow", "Green", "Black",""])
        self.colorBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.colorBox.grid(column='7', padx='5', pady='5', row='3')

        self.factoryBox = ttk.Combobox(self, values = ["Malaysia", "China", "Philippines",""])
        self.factoryBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.factoryBox.grid(column='7', padx='5', pady='5', row='4')

        self.productionYearBox = ttk.Combobox(self, values = ["2014", "2015",
        "2016", "2017", "2018", "2019", "2020",""])
        self.productionYearBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.productionYearBox.grid(column='7', padx='5', pady='5', row='5')

        self.powerSupplyBox = ttk.Combobox(self, values = ["Battery", "USB",""])
        self.powerSupplyBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.powerSupplyBox.grid(column='7', padx='5', pady='5', row='6')

        ####Labels####
        self.simpleSearchLabel = ttk.Label(self)
        self.simpleSearchLabel.configure(background='#a6f991', text='Simple Search')
        self.simpleSearchLabel.grid(column='2', padx='5', pady='5', row='2')

        self.advancedSearchLabel = ttk.Label(self)
        self.advancedSearchLabel.configure(background='#b19bee', text='Advanced Search')
        self.advancedSearchLabel.grid(column='5', padx='5', pady='5', row='2')

        self.priceLabel = ttk.Label(self)
        self.priceLabel.configure(text='Price')
        self.priceLabel.grid(column='6', padx='5', pady='5', row='2')

        self.colorLabel = ttk.Label(self)
        self.colorLabel.configure(text='Color')
        self.colorLabel.grid(column='6', padx='5', pady='5', row='3')

        self.factoryLabel = ttk.Label(self)
        self.factoryLabel.configure(text='Factory')
        self.factoryLabel.grid(column='6', padx='5', pady='5', row='4')

        self.productionYearLabel = ttk.Label(self)
        self.productionYearLabel.configure(text='Production Year')
        self.productionYearLabel.grid(column='6', padx='5', pady='5', row='5')

        self.powerSupplyLabel = ttk.Label(self)
        self.powerSupplyLabel.configure(text='Power Supply')
        self.powerSupplyLabel.grid(column='6', padx='5', pady='5', row='6')

        self.categoryLabel = ttk.Label(self)
        self.categoryLabel.configure(text='Category')
        self.categoryLabel.grid(column='3', padx='5', pady='5', row='2')

        self.modelLabel = ttk.Label(self)
        self.modelLabel.configure(text='Model')
        self.modelLabel.grid(column='3', padx='5', pady='5', row='3')
        
        ####Item display####
        self.treeFrame= ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='300')
        self.treeFrame.grid(column='2', columnspan='6', row='10', rowspan='1', pady ='10')

        cols = ("itemID","Category","Model", "Price", "Color","Factory", "Production Year", "Power Supply")
        
        self.itemTree = ttk.Treeview(self.treeFrame, columns = cols,show='headings')
        self.itemTree.pack(side='left')
        scroll_y = Scrollbar(self.treeFrame, orient = 'vertical', command = self.itemTree.yview)
        scroll_y.pack(side = RIGHT, fill = Y)
        self.itemTree.configure(yscrollcommand = scroll_y.set)

        
        for col in cols:
            self.itemTree.column(col, anchor="center", width=110)
            self.itemTree.heading(col, text=col)


        self.availItems = ttk.Label(self, font=("Arial", 14))
        self.availItems.configure(text='Search Results')
        self.availItems.grid(column='2', columnspan='2', row='9')

         #take inputs from comboboxes and bring to searchResults frame
    def search(self, event):
        self.itemTree.delete(*self.itemTree.get_children())
        mongoSearch = ""
        
        category = self.categoryBox.get()
        model = self.modelBox.get()
        price =  self.priceBox.get()
        color = self.colorBox.get()
        factory = self.factoryBox.get()
        productionYear = self.productionYearBox.get()
        powerSupply = self.powerSupplyBox.get()

        ##special handeling for price
        if price:
            catandmod = self.findModelfromPrice(price)
            if category and category != catandmod[0]:
                category = "no output"
            if model and model != catandmod[1]:
                model = "no output"
            else:
                category = catandmod[0]
                model = catandmod[1]       

        if category:
            mongoSearch += "'Category': " + "'{}'".format(category) + ", "
        if model:
            mongoSearch += "'Model': " + "'{}'".format(model) + ", "
        if color:
            mongoSearch += "'Color': " + "'{}'".format(color) + ", "
        if factory:
            mongoSearch += "'Factory': " + "'{}'".format(factory) + ", "
        if productionYear:
            mongoSearch += "'ProductionYear': " + "'{}'".format(productionYear) + ", "
        if powerSupply:
            mongoSearch += "'PowerSupply': " + "'{}'".format(powerSupply) + ", "
        
        mongoSearch = "{" + mongoSearch + "'PurchaseStatus': 'Unsold'" + "}"

        #uncomment print statement to show output in terminal
        #print(mongoSearch)

        items = db["items"]
        allrecords = items.find(eval(mongoSearch))
        allrecordsList = list(allrecords)
        #uncomment to print records in terminal
        messagebox.showinfo(title="Search Results", message= "{} items available based on your search!".format(len(allrecordsList)))

        if len(allrecordsList) == 0:
            pass
        else:
            for record in allrecordsList:
                result = self.mongoToTree(record)
                self.itemTree.insert("", "end", values=result)
    
    def findModelfromPrice(self, price):
        product = products.find({'Price ($)': int(price)})[0]
        Category = product['Category']
        Model = product['Model']
        return (Category, Model)

    def findPrice(self, category, model):
        product = products.find({'Category': category, 'Model': model})[0]
        price = product['Price ($)']
        return (price)

    def buyItem(self, a):
        curItem = self.itemTree.focus()
        extractID = self.itemTree.item(curItem)['values'][0]
        
        #update mysql database, need to get current customer id
        updateStatement = "UPDATE items SET PurchaseStatus = 'Sold',dateOfPurchase = %s, customerID = %s  WHERE ItemID = %s"
        val = (date.today().isoformat(),self.controller.getUserID(), extractID)

        con.ping()  # reconnecting mysql
        with con.cursor() as cursor:         
            cursor.execute(updateStatement, val)
        con.commit()
        con.close()



        #delete item and show purchase success
        self.itemTree.delete(self.itemTree.focus())
        messagebox.showinfo(title="Purchase Successful", message= "Thank you for your purchase!")
        

    def mongoToTree(self, r):
        price = self.findPrice(r["Category"], r["Model"])
        re = (r["ItemID"], r["Category"], r["Model"], price, r["Color"], r["Factory"], r["ProductionYear"], r["PowerSupply"])
        return re
    
    # file new function
    # def file_new():
    #     file_new_frame.pack(fill="both", expand=1)

    def hello(self):
        print("hello")
    
    def handleLogout(self):
        self.controller.logout()
    
    def menuBar(self,root):
        menubar = tk.Menu(root)
        # nestedProductMenu = tk.Menu(self)
        # nestedItemMenu = tk.Menu(self)
        # nestedRequestMenu = tk.Menu(self)
        # nestedServiceMenu = tk.Menu(self)
        # nestedProfileMenu = tk.Menu(self)

        # #product
        # productMenu = tk.Menu(menubar, tearoff=0)   
        # menubar.add_cascade(label="Products", menu=productMenu)
        # productMenu.add_command(label="View Products", command=self.hello)
        # # productMenu.add_cascade(label="hehehe", menu=nestedProductMenu) #only for adding more nested menus to menus


        #purchases
        purchasesMenu = tk.Menu(menubar, tearoff=0) 
        menubar.add_cascade(label = "My Purchases", menu=purchasesMenu)  
        purchasesMenu.add_command(label="View My Purchases", command=self.hello)
        # itemMenu.add_cascade(label="wowooow",menu=nestedItemMenu)
        
        #service requests
        requestMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="My Service Requests", menu=requestMenu)
        requestMenu.add_command(label="View Service Requests", command=self.hello)
    #     requestMenu.add_cascade(label="heloooo", menu=nestedRequestMenu)

        # #service 
        # serviceMenu = tk.Menu(menubar, tearoff=0)   
        # menubar.add_cascade(label="Services", menu=requestMenu)
        # serviceMenu.add_command(label="View Services", command=self.hello)
        # # serviceMenu.add_cascade(label="yayy", menu=nestedServiceMenu)

        #profile
        profileMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="My Profile", menu=profileMenu)
        profileMenu.add_command(label="View Profile", command= lambda: ViewProfileWindow(master=self.controller))
        profileMenu.add_command(label="Change Password", command= lambda: ChangePasswordWindow(master=self.controller))
        profileMenu.add_separator()
        profileMenu.add_command(label="Logout", command=self.handleLogout)

        
        return menubar
    
class RequestsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.userID = None
        self.domain = None
    
        self.label = ttk.Label(self, text="Requests List", font=LARGEFONT)
        self.label.grid(row=0, column=4, padx=10, pady=10)

        self.payButton = ttk.Button(self)
        self.payButton.configure(text='Pay')
        self.payButton.grid(column='6', pady='20', row='11', sticky='e')
        self.payButton.bind('<Button-1>', self.payRequest)

        self.cancelButton = ttk.Button(self)
        self.cancelButton.configure(text='Cancel')
        self.cancelButton.grid(column='7', pady='20', row='11', sticky='e')
        self.cancelButton.bind('<Button-1>', self.cancelRequest)

        button1 = ttk.Button(self, text="Back to Admin Home",
                             command=lambda: controller.show_frame(CustomerPortal))
        button1.grid(row=0, column=1, padx=5, pady=5)

        self['background']='#F6F4F1'
        
    def showTree(self):
        ####Item display####
        self.treeFrame= ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='400')
        self.treeFrame.grid(column='2', columnspan='6', row='10', rowspan='1', pady ='10')

        cols = ("Request ID", "Item ID","Request Status","Request Date", "Payment Due Date", "Service Fee")
        
        self.itemTree = ttk.Treeview(self.treeFrame, columns = cols,show='headings')
        self.itemTree.pack(side='left')
        scroll_y = Scrollbar(self.treeFrame, orient = 'vertical', command = self.itemTree.yview)
        scroll_y.pack(side = RIGHT, fill = Y)
        self.itemTree.configure(yscrollcommand = scroll_y.set)

        for col in cols:
            if col ==  "Request Status":
                self.itemTree.column(col, anchor="center", width=230)
                self.itemTree.heading(col, text=col)
            else:
                self.itemTree.column(col, anchor="center", width=150)
                self.itemTree.heading(col, text=col)

        allRequestsList = mysqlinit.retrieveRequests(self.controller.getUserID())
        for r in allRequestsList:
            self.itemTree.insert("", "end", values=r)
 
    def payRequest(self, a):
        curItem = self.itemTree.focus()
        extractID = self.itemTree.item(curItem)['values'][0]
        requestStatus = self.itemTree.item(curItem)['values'][2]
        if requestStatus == "Submitted and Waiting for payment":

            payReq = mysqlinit.payRequest(extractID)

            # reload table
            messagebox.showinfo(title="Payment Successful", message= "Thank you for your payment!")
            for r in self.itemTree.get_children():
                self.itemTree.delete(r)

            allRequestsList = mysqlinit.retrieveRequests(self.controller.getUserID())

            for r in allRequestsList:
                self.itemTree.insert("", "end", values=r)
        else:
            messagebox.showinfo(title="Payment Unsuccessful", message= "Payment is not required for this request!")
    
    def cancelRequest(self, a):
        curItem = self.itemTree.focus()
        extractID = self.itemTree.item(curItem)['values'][0]
        requestStatus = self.itemTree.item(curItem)['values'][2]
        if requestStatus != "Canceled" and requestStatus != "Completed":

            payReq = mysqlinit.cancelRequest(extractID)

            # reload table
            messagebox.showinfo(title="Cancellation Successful", message= "Request {} has been successfully cancelled!".format(extractID))
            for r in self.itemTree.get_children():
                self.itemTree.delete(r)

            allRequestsList = mysqlinit.retrieveRequests(self.controller.getUserID())

            for r in allRequestsList:
                self.itemTree.insert("", "end", values=r)
        else:
            messagebox.showinfo(title="Cancellation Unsuccessful", message= "This request cannot be cancelled!")

    def menuBar(self,root):
        menubar = tk.Menu(root)
        #purchases
        purchasesMenu = tk.Menu(menubar, tearoff=0) 
        menubar.add_cascade(label = "My Purchases", menu=purchasesMenu)  
        purchasesMenu.add_command(label="View My Purchases", command=self.hello)
        # itemMenu.add_cascade(label="wowooow",menu=nestedItemMenu)
        
        #service requests
        requestMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="My Service Requests", menu=requestMenu)
        requestMenu.add_command(label="View Service Requests", command=self.hello)
    #     requestMenu.add_cascade(label="heloooo", menu=nestedRequestMenu)
        #profile
        profileMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="My Profile", menu=profileMenu)
        profileMenu.add_command(label="View Profile", command= lambda: ViewProfileWindow(master=self.controller))
        profileMenu.add_command(label="Change Password", command= lambda: ChangePasswordWindow(master=self.controller))
        profileMenu.add_separator()
        profileMenu.add_command(label="Logout", command=self.handleLogout)
        self.showTree()
        return menubar
    
    def hello(self):
        print("hello")
    
    def handleLogout(self):
        self.controller.logout()


    # def menuBar(self,root):
    #     menubar = tk.Menu(self)
    #     homeMenu = tk.Menu(self)
    #     purchaseMenu = tk.Menu(self)
    #     requestMenu = tk.Menu(self)
    #     profileMenu = tk.Menu(self)
    #     nestedHomeMenu = tk.Menu(self)
    #     nestedPurchaseMenu = tk.Menu(self)
    #     nestedRequestMenu = tk.Menu(self)
    #     nestedProfileMenu = tk.Menu(self)

    #     # pageMenu.add_command(label="PageOne")
    #     # menubar.add_cascade(label="PageOne", menu=pageMenu)

    #     menubar.add_cascade(label="Home", menu=homeMenu)
    #     homeMenu.add_cascade(label="hehehe", menu=nestedHomeMenu)
    #     # menubar.add_separator()
    #     menubar.add_cascade(label="Purchases", menu=purchaseMenu)
    #     purchaseMenu.add_cascade(label="wowooow",menu=nestedPurchaseMenu)

    #     menubar.add_cascade(label="Service Requests", menu=requestMenu)
    #     requestMenu.add_cascade(label="heloooo", menu=nestedRequestMenu)

    #     menubar.add_cascade(label="My Profile", menu=profileMenu)
    #     profileMenu.add_cascade(label="View Profile", menu=nestedProfileMenu)
    #     profileMenu.add_cascade(label="Change Password", menu=nestedProfileMenu)
    #     return menubar


        # root = tk.Frame(self)
        # root.tkraise()

        # my_menu = Menu(root)
        # my_menu = tk.Menu(self)

        # create a menu item
        # file_menu = tk.Menu(my_menu)
        # my_menu.add_cascade(label="File", menu=file_menu)
        # file_menu.add_command(label="New...", command=file_new)
        # file_menu.add_separator()
        # file_menu.add_command(label="Exit", command=root.destroy)

        # create some frames
        # file_new_frame = Frame(root,width=400, height=400, bg="red")


        # self.config(menu=my_menu)




        #  Dummy Display, need to be replaced 
        # options = ("Customer", "Administrator")

        # dropdownlist = ttk.OptionMenu(self, self.domain, options[0], *options)
        
        # dropdownlist.grid(row=0, column=1, padx=10, pady=10)

        

    