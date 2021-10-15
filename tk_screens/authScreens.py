from tk_screens.adminPortal import *
from tk_screens.customerPortal import *
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label
from tk_screens.tkinterCustomButton import TkinterCustomButton
from db_connections.mysqldb import SQLDatabase
from PIL import Image, ImageTk

db = SQLDatabase()

LARGEFONT = ("Calibri", 35, "bold")
# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.domain = tk.StringVar(self)
        self.userID = tk.StringVar(self)
        self.controller = controller
        
        # label of frame Layout 2
        # label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        # place the photo in the frame
        # you can find the images from flaticon.com site
        
        # self.img = ImageTk.PhotoImage(Image.open("images/welcome.png").convert("RGB"))
        self.img = ImageTk.PhotoImage(Image.open("images/main_final.png").convert("RGB"))
        # self.img = tk.PhotoImage(file = "images/main_1.jpeg")
        self.label = ttk.Label(self, image=self.img)
        self.label.grid(row=0, column=2, padx=250, pady=20)
        
        # putting the grid in its place by using
        # grid
        # label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Login",
                             command=lambda: controller.show_frame(LoginPage, self.domain))
        

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=2, padx=5, pady=5)
        
        # def button_function():
        #     print("Button pressed")

        # button_1 = TkinterCustomButton(text="Login", corner_radius=10, command=lambda: controller.show_frame(LoginPage, self.domain))
        # button_1.place(x = 530,y = 650, anchor=tk.CENTER)

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Register",
                             command=lambda: self.handleRegister(self.domain))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=2, padx=5, pady=5)


        # Dropdown menu options
        options = ("Customer", "Administrator")

        dropdownlist = ttk.OptionMenu(self, self.domain, options[0], *options)
        
        dropdownlist.grid(row=3, column=2, padx=5, pady=5)

        # table = Table(parent= parent,columns=("FName", "LName", "Roll No"))
        # table.insertRow(('Amit', 'Kumar', '17701'))
        # table.insertRow(('Ankush', 'Mathur', '17702'))
        # tree = table.getTree()
        # tree.grid(row=4, column=1, padx=10, pady=10)

    def handleRegister(self, domain):
        if domain.get()=="Customer":
            self.controller.show_frame(RegisterPage, self.domain)
        else:
            messagebox.showerror(title="Registration Failed", message= "Please log in first to create a new administrator account.")

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

# second window frame page
class LoginPage(tk.Frame):

    def __init__(self, parent, controller):

        self.domain = controller.getDomain()

        # input fields
        self.userID = tk.StringVar()
        self.password = tk.StringVar()

        self.controller = controller

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Login Page", font=LARGEFONT, anchor='center')
        label.grid(row=6, column=7, padx=(400,0), pady=(100,50), columnspan=7)
        # label.grid_rowconfigure(1, weight=1)
        # label.grid_columnconfigure(1, weight=1)

        # background colour same as the welcome page image 
        self['background']='#F6F4F1'
            
        userIDLabel = ttk.Label(self, text="User ID:")
        userIDLabel.grid(row=7, column=7, padx=(400,0), pady=5)
        

        userIDInput = ttk.Entry(self, textvariable=self.userID)
        userIDInput.grid(row=7, column=8, padx=5, pady=5)
        

        passwordLabel = ttk.Label(self, text="Password:")
        passwordLabel.grid(row=8, column=7, padx=(400,0), pady=5)

        passwordInput = ttk.Entry(self,show="*", textvariable=self.password)
        passwordInput.grid(row=8, column=8, padx=5, pady=5)
        

        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text="Sign In",
                             command=self.handleLogin)

        # putting the button in its place by
        # using grid
        button2.grid(row=9, column=8, padx=0, pady=5)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Back to Welcome Page",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.grid(row=1, column=1, padx=(10,0), pady=10)


    def handleLogin(self):
        if self.domain.get() == "Customer":
            print("logged in:", self.userID.get(), self.password.get())
            res = db.getCustomerLogin(self.userID.get(), self.password.get())

            # if res.startswith('(') and res.endswith(')'):
            if isinstance(res, tuple):
                messagebox.showinfo(title="Login Success", message="Successfully logged in")
                self.controller.setUserID(self.userID.get()) # Change the auth state
                self.controller.setDomain(self.domain.get())
                self.controller.show_frame(CustomerPortal, domain = "Customer", userID = self.userID.get())
            elif isinstance(res, str):
                print("login failed", type(res))
                messagebox.showerror(title="Login Failed", message=res)
        elif self.domain.get() == "Administrator":
            print("logged in:", self.userID.get(), self.password.get())
            res = db.getAdminLogin(self.userID.get(), self.password.get())
            # if res.startswith('(') and res.endswith(')'):
            if isinstance(res, tuple):
                messagebox.showinfo(title="Login Success", message="Admin Successfully logged in")
                self.controller.setUserID(self.userID.get()) # Change the auth state
                self.controller.setDomain(self.domain.get())
                self.controller.show_frame(AdminPortal, domain = "Administrator", userID = self.userID.get())
            elif isinstance(res, str):
                print("login failed", type(res))
                messagebox.showerror(title="Login Failed", message=res)
    

    def setUserType(self, usertype):
        self.domain = usertype
        # Log
        print("gui.py>LoginPage> Domain Set:",self.domain.get())

    def setUserID(self, userid):
        self.userID = userid

# third window frame page2
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        self.domain = controller.getDomain()

        self.userID = tk.StringVar()
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.address = tk.StringVar()
        self.phoneNumber = tk.StringVar()
        self.gender = tk.StringVar()

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Register Page", font=LARGEFONT)
        label.grid(row=2, column=3, padx=5, pady=5, columnspan=11)

        self['background']='#F6F4F1'

        userIDlabel = ttk.Label(self, text="User ID:")
        userIDlabel.grid(row=3, column=3, padx=5, pady=5)

        userIDInput = ttk.Entry(self, textvariable=self.userID)
        userIDInput.grid(row=3, column=4,  padx=5, pady=5)


        namelabel = ttk.Label(self, text="Name:")
        namelabel.grid(row=4, column=3, padx=5, pady=5)

        nameInput = ttk.Entry(self, textvariable=self.name)
        nameInput.grid(row=4, column=4,  padx=5, pady=5)

        emailLabel = ttk.Label(self, text="Email:")
        emailLabel.grid(row=5, column=3,  padx=5, pady=5)

        emailInput = ttk.Entry(self, textvariable=self.email)
        emailInput.grid(row=5, column=4,  padx=5, pady=5)

        passwordLabel = ttk.Label(self, text="Password:")
        passwordLabel.grid(row=6, column=3,  padx=5, pady=5)

        passwordInput = ttk.Entry(self,show="*", textvariable=self.password)
        passwordInput.grid(row=6, column=4,  padx=5, pady=5)

        addressLabel = ttk.Label(self, text="Address:")
        addressLabel.grid(row=7, column=3, padx=5, pady=5)

        addressInput = ttk.Entry(self, textvariable=self.address)
        addressInput.grid(row=7, column=4,  padx=5, pady=5)

        phoneNumberLabel = ttk.Label(self, text="Phone:")
        phoneNumberLabel.grid(row=8, column=3,  padx=5, pady=5)

        phoneNumberInput = ttk.Entry(self, textvariable=self.phoneNumber)
        phoneNumberInput.grid(row=8, column=4,  padx=5, pady=5)

        genderLabel = ttk.Label(self, text="Gender:")
        genderLabel.grid(row=9, column=3,  padx=5, pady=5)

        genderOptions = ttk.OptionMenu(self, self.gender, 'M', *("M","F"))
        genderOptions.grid(row=9, column=4,  padx=5, pady=5)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Register",
                             command=self.handleRegister)

        # putting the button in its place by
        # using grid
        button1.grid(row=10, column=3,  padx=5, pady=5)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Back to Welcome Page",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=10, column=4,  padx=5, pady=5)

    def setUserType(self,usertype):
        self.domain = usertype

    '''
    Returns True if any of the fields are empty.
    '''
    def checkEmptyField(self):
        for element in [self.userID.get(), self.name.get(), self.email.get(), self.password.get(), self.address.get(), self.phoneNumber.get(), self.gender.get()]:
            if element=="" or element=='' or element==' ':
                return True
        return False

    def handleRegister(self):        
        if self.domain.get()=="Customer":
            if self.checkEmptyField():
                messagebox.showerror(title="Registration Failed", message="Please fill in all fields")
            else:
                res = db.createCustomer([self.userID.get(), self.name.get(), self.email.get(), self.password.get(), self.address.get(), self.phoneNumber.get(), self.gender.get()])
                if res : 
                    # messagebox.showerror(title="Registration Failed", message=res)
                    messagebox.showerror(title="Registration Failed", message="There is an existing user with the given User ID! Please use a different User ID.")
                else : 
                    messagebox.showinfo(title="Registration Success", message= "Succesfully created a customer account!")
        
    
            
