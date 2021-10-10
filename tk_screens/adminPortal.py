import tkinter as tk
# from tkinter import *
from tkinter import ttk, messagebox, PhotoImage, Label, Entry, Menu
from db_connections.mysqldb import SQLDatabase
from db_connections.mongodb import MongoDB
# from tk_screens.authScreens import StartPage -- Circular import with authScreens

db = SQLDatabase()
mongodb = MongoDB()

LARGEFONT = ("Verdana", 35)

class AdminPortal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.domain = tk.StringVar(self)
        self.controller = controller

        # Reset Button
        resetButton = ttk.Button(self, text="Reset SQLDB", command=self.resetDB)
        resetButton.grid(row=3, column=6, padx=10, pady=10)


        createAdminButton = ttk.Button(self, text="Create New Admin",
                             command=lambda: controller.show_frame(CreateAdminPage, self.domain))

        createAdminButton.grid(row=3, column=7, padx=10, pady=10)

        self['background']='#F6F4F1'

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
    

    def resetDB(self):
        print("Reloading databases")
        db.resetMySQLState()
        items, products = mongodb.convertMongotoSQL()
        db.loadMongo(items, products)
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


