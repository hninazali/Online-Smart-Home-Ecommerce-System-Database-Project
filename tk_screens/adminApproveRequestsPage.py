import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from db_connections.mysqldb import SQLDatabase
from tk_screens.viewProfileWindow import ViewProfileWindow
from tk_screens.changePasswordWindow import ChangePasswordWindow
from tk_screens.adminCompleteServicesPage import AdminCompleteServicesPage
#from tk_screens.adminPortal import AdminAdvancedSearch
#from tk_screens.adminPortal import AdminProductSearch
#from tk_screens.adminPortal import AdminItemSearch
db = SQLDatabase()

LARGEFONT = ("Calibri", 35, "bold")


class AdminApproveRequestsPage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.userID = None
        self.domain = None
        self.selectedRequests = []
        self.selectedServices = []

        self['background']='#F6F4F1'

        label = ttk.Label(self, text="Requests pending Approval", font=LARGEFONT)
        label.grid(row='0', column='4', padx='220', pady='10')

    def showTree(self):

        self.treeFrame = ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='400')
        self.treeFrame.grid(column='2', columnspan='6', row='2', rowspan='1', pady='20', padx='170')

        self.cols = ('Request ID', 'Service ID', 'Item ID', 'Request Date', 'Payment for Service', 'Request Status', 'Service Status')

        self.tree = ttk.Treeview(self.treeFrame, columns=self.cols, show='headings', height='10')
        self.tree.pack(side='left')
        scrollbar = ttk.Scrollbar(self.treeFrame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side = 'right', fill = 'y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        results = db.retrieveRequestsForApproval()

        for col in self.cols:
            self.tree.column(col, anchor="center", width=150)
            self.tree.heading(col, text=col)

        for r in results:
            self.tree.insert("", "end", values=self.polishData(r))

        # approve button removes requests from the list and change the request & service statuses to approved and in progress
        self.aButton = ttk.Button(self, text="Approve", command= lambda: self.approveRequests(), width=15)
        self.aButton.grid(row='5', column='4', padx='45', pady='5')

    def polishData(self, r):
        paymentStatus = ""
        if r[4] == 0:
            paymentStatus = "Waived"
        else:
            paymentStatus = "Paid"

        result = (r[0], r[1], r[2], r[3], paymentStatus, r[5], r[6])
        return result

    def approveRequests(self):

        values = self.tree.selection()

        for v in values:
            self.selectedRequests.append(self.tree.item(v)['values'][0])
            self.selectedServices.append(self.tree.item(v)['values'][1])     

        res = db.approveRequests(self.selectedRequests, self.selectedServices, self.controller.getUserID())

        if res is None:
            messagebox.showwarning(title="Request Approval", message="Please select record(s) to proceed.")
        elif res == len(self.selectedRequests):
            messagebox.showinfo(title="Requests Approval", message="Selected record(s) have been approved successfully!")
            for v in values:
                self.tree.delete(v)
        else:
            messagebox.showerror(title="Requests Approval", message="An error has occurred while request(s) were processed.")
        
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
        requestMenu.add_command(label="View Service Requests", command=lambda: self.controller.show_frame(AdminApproveRequestsPage, self.domain, self.userID))
    #     requestMenu.add_cascade(label="heloooo", menu=nestedRequestMenu)

        #service 
        serviceMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Services", menu=serviceMenu)#
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
        print("gui.py>AdminApproveRequestsPage> Domain Set:",self.domain.get())