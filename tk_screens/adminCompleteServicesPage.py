import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, LabelFrame
from db_connections.mysqldb import SQLDatabase
from tk_screens.viewProfileWindow import ViewProfileWindow
from tk_screens.changePasswordWindow import ChangePasswordWindow
#from tk_screens.adminApproveRequestsPage import AdminApproveRequestsPage
db = SQLDatabase()

LARGEFONT = ("Calibri", 35, "bold")


class AdminCompleteServicesPage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.userID = None
        self.domain = None
        self.selectedRequests = []
        self.selectedServices = []
        self['background']='#F6F4F1'

        # set style to classic so that background can be changed, error on macbooks
        # tk.Frame.__init__(self, parent)
        # style = ttk.Style(self)
        # style.theme_use('classic')
        label = ttk.Label(self, text="Services pending Completion", font=LARGEFONT)
        label.grid(row=0, column=4, padx=350, pady=10)

    def showTree(self):

        self.treeFrame = ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='400')
        self.treeFrame.grid(column='2', columnspan='6', row='2', rowspan='1', pady='20', padx='245')

        self.cols = ('Request ID', 'Service ID', 'Item ID', 'Request Date', 'Request Status', 'Service Status')

        results = db.retrieveServicesToComplete(self.controller.getUserID())

        self.tree = ttk.Treeview(self.treeFrame, columns=self.cols, show='headings', height='10')
        self.tree.pack(side='left')
        scrollbar = ttk.Scrollbar(self.treeFrame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side = 'right', fill = 'y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        for col in self.cols:
            self.tree.column(col, anchor="center", width=150)
            self.tree.heading(col, text=col)

        for r in results:
            self.tree.insert("", "end", values=r)

        # approve button removes requests from the list and change the request & service statuses to approved and in progress
        self.cButton = ttk.Button(self, text="Completed", command= lambda: self.completeServices(), width=15)
        self.cButton.grid(row='5', column='4', padx='35', pady='5')

    def completeServices(self):

        values = self.tree.selection()

        for v in values:
            self.selectedRequests.append(self.tree.item(v)['values'][0])
            self.selectedServices.append(self.tree.item(v)['values'][1])

        res = db.completeService(self.selectedRequests, self.selectedServices)

        if res is None:
            messagebox.showwarning(title="Services Completion", message="Please select record(s) to proceed.")
        elif res == len(self.selectedRequests):
            messagebox.showinfo(title="Services Completion", message="Selected record(s) have been updated successfully!")
            for v in values:
                self.tree.delete(v)
        else:
            messagebox.showerror(title="Services Completion", message="An error has occurred while records(s) were processed.")
        
        self.selectedRequests.clear()
        self.selectedServices.clear()

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
        requestMenu.add_command(label="View Service Requests", command=lambda: self.controller.show_frame(AdminApproveRequestsPage))
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

        self.showTree()      
        
        return menubar
    
    def setUserType(self, userID):
        self.domain = userID
        # Log
        print("gui.py>AdminCompleteServicesPage> Domain Set:", self.domain.get())

        self.showTree()
