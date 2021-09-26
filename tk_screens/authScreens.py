from tk_screens.customerPortal import CustomerPortal
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label
from mysql_connections.mysqldb import SQLDatabase
from PIL import Image, ImageTk
db = SQLDatabase()

LARGEFONT = ("Verdana", 35)
# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.domain = tk.StringVar(self)
        self.controller = controller

        # label of frame Layout 2
        # label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        # place the photo in the frame
        # you can find the images from flaticon.com site
        
        self.img = ImageTk.PhotoImage(Image.open("images/welcome.png").convert("RGB"))
        self.label = ttk.Label(self, image=self.img)
        self.label.grid(row=0, column=4, padx=10, pady=10)
        

        # putting the grid in its place by using
        # grid
        # label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Login",
                             command=lambda: controller.show_frame(LoginPage, self.domain))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Register",
                             command=lambda: self.handleRegister(self.domain))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)


        # Dropdown menu options
        options = ("Customer", "Administrator")

        dropdownlist = ttk.OptionMenu(self, self.domain, options[0], *options)
        
        dropdownlist.grid(row=3, column=1, padx=10, pady=10)

    def handleRegister(self, domain):
        if domain.get()=="Customer":
            self.controller.show_frame(RegisterPage, self.domain)
        else:
            messagebox.showerror(title="Registration Failed", message= "Please log in first to create a new administrator account.")



# second window frame page1
class LoginPage(tk.Frame):

    def __init__(self, parent, controller):

        self.domain = controller.getDomain()

        # input fields
        self.userID = tk.StringVar()
        self.password = tk.StringVar()

        self.controller = controller

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Login Page", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)


        userIDLabel = ttk.Label(self, text="User ID:")
        userIDLabel.grid(row=1, column=1, padx=10, pady=10)

        userIDInput = ttk.Entry(self, textvariable=self.userID)
        userIDInput.grid(row=1, column=3, padx=10, pady=10)

        passwordLabel = ttk.Label(self, text="Password:")
        passwordLabel.grid(row=2, column=1, padx=10, pady=10)

        passwordInput = ttk.Entry(self,show="*", textvariable=self.password)
        passwordInput.grid(row=2, column=3, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text="Sign In",
                             command=self.handleLogin)

        # putting the button in its place by
        # using grid
        button2.grid(row=3, column=1, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.grid(row=3, column=3, padx=10, pady=10)


    def handleLogin(self):
        if self.domain.get() == "Customer":
            print("logged in:", self.userID.get(), self.password.get())
            res = db.getCustomerLogin(self.userID.get(), self.password.get())
            # if res.startswith('(') and res.endswith(')'):
            if isinstance(res, tuple):
                messagebox.showinfo(title="Login Success", message="Successfully logged in")
                self.controller.show_frame(CustomerPortal)
            elif isinstance(res, str):
                print("login failed", type(res))
                messagebox.showerror(title="Login Failed", message=res)
        elif self.domain.get() == "Administrator":
            print("logged in:", self.userID.get(), self.password.get())
            res = db.getAdminLogin(self.userID.get(), self.password.get())
            # if res.startswith('(') and res.endswith(')'):
            if isinstance(res, tuple):
                messagebox.showinfo(title="Login Success", message="Admin Successfully logged in")
                self.controller.show_frame(CustomerPortal)
            elif isinstance(res, str):
                print("login failed", type(res))
                messagebox.showerror(title="Login Failed", message=res)
    

    def setUserType(self, usertype):
        self.domain = usertype
        # Log
        print("gui.py>LoginPage> Domain Set:",self.domain.get())

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
        label.grid(row=0, column=4, padx=10, pady=10)

        userIDlabel = ttk.Label(self, text="User ID:")
        userIDlabel.grid(row=1, column=1, padx=10, pady=10)

        userIDInput = ttk.Entry(self, textvariable=self.userID)
        userIDInput.grid(row=1, column=3, padx=10, pady=10)


        namelabel = ttk.Label(self, text="Name:")
        namelabel.grid(row=2, column=1, padx=10, pady=10)

        nameInput = ttk.Entry(self, textvariable=self.name)
        nameInput.grid(row=2, column=3, padx=10, pady=10)

        emailLabel = ttk.Label(self, text="Email:")
        emailLabel.grid(row=3, column=1, padx=10, pady=10)

        emailInput = ttk.Entry(self, textvariable=self.email)
        emailInput.grid(row=3, column=3, padx=10, pady=10)

        passwordLabel = ttk.Label(self, text="Password:")
        passwordLabel.grid(row=4, column=1, padx=10, pady=10)

        passwordInput = ttk.Entry(self,show="*", textvariable=self.password)
        passwordInput.grid(row=4, column=3, padx=10, pady=10)

        addressLabel = ttk.Label(self, text="Address:")
        addressLabel.grid(row=5, column=1, padx=10, pady=10)

        addressInput = ttk.Entry(self, textvariable=self.address)
        addressInput.grid(row=5, column=3, padx=10, pady=10)

        phoneNumberLabel = ttk.Label(self, text="Phone:")
        phoneNumberLabel.grid(row=6, column=1, padx=10, pady=10)

        phoneNumberInput = ttk.Entry(self, textvariable=self.phoneNumber)
        phoneNumberInput.grid(row=6, column=3, padx=10, pady=10)

        genderLabel = ttk.Label(self, text="Gender:")
        genderLabel.grid(row=7, column=1, padx=10, pady=10)

        genderOptions = ttk.OptionMenu(self, self.gender, 'M', *("M","F"))
        genderOptions.grid(row=7, column=3, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Register",
                             command=self.handleRegister)

        # putting the button in its place by
        # using grid
        button1.grid(row=8, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=8, column=3, padx=10, pady=10)

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
                    messagebox.showerror(title="Registration Failed", message=res)
                else : 
                    messagebox.showinfo(title="Registration Success", message= "Succesfully created a customer account!")
        
    
            