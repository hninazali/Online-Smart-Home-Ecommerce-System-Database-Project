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
                             command=lambda: controller.show_frame(RegisterPage, self.domain))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)

        self.domain = tk.StringVar(self)
        # Dropdown menu options
        options = ("Customer", "Administrator")

        dropdownlist = ttk.OptionMenu(self, self.domain, options[0], *options)
        
        dropdownlist.grid(row=3, column=1, padx=10, pady=10)
    


# second window frame page1
class LoginPage(tk.Frame):

    def __init__(self, parent, controller):

        self.domain = controller.getDomain()

        # input fields
        self.email = tk.StringVar()
        self.password = tk.StringVar()



        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 1", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)


        emailLabel = ttk.Label(self, text="Email:")
        emailLabel.grid(row=1, column=1, padx=10, pady=10)

        emailInput = ttk.Entry(self, textvariable=self.email)
        emailInput.grid(row=1, column=3, padx=10, pady=10)

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
        button1.grid(row=4, column=1, padx=10, pady=10)


    def handleLogin(self):
        if self.domain.get() == "Customer":
            print("logged in:", self.email.get(), self.password.get())
            res = db.getCustomerLogin(self.email.get(), self.password.get())
            # if res.startswith('(') and res.endswith(')'):
            if isinstance(res, tuple):
                print("ok")
            
            elif isinstance(res, str):
                print("login failed", type(res))
                messagebox.showerror(title="Login Failed", message=res)
        elif self.domain.get() == "Administrator":
            print("logged in:", self.email.get(), self.password.get())
            res = db.getAdminLogin(self.email.get(), self.password.get())
            # if res.startswith('(') and res.endswith(')'):
            if isinstance(res, tuple):
                print("ok")
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

        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.address = tk.StringVar()
        self.phoneNumber = tk.StringVar()
        self.gender = tk.StringVar()

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 2", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        namelabel = ttk.Label(self, text="Name:")
        namelabel.grid(row=1, column=1, padx=10, pady=10)

        nameInput = ttk.Entry(self, textvariable=self.name)
        nameInput.grid(row=1, column=3, padx=10, pady=10)

        emailLabel = ttk.Label(self, text="Email:")
        emailLabel.grid(row=2, column=1, padx=10, pady=10)

        emailInput = ttk.Entry(self, textvariable=self.email)
        emailInput.grid(row=2, column=3, padx=10, pady=10)

        passwordLabel = ttk.Label(self, text="Password:")
        passwordLabel.grid(row=3, column=1, padx=10, pady=10)

        passwordInput = ttk.Entry(self,show="*", textvariable=self.password)
        passwordInput.grid(row=3, column=3, padx=10, pady=10)

        addressLabel = ttk.Label(self, text="Address:")
        addressLabel.grid(row=4, column=1, padx=10, pady=10)

        addressInput = ttk.Entry(self, textvariable=self.address)
        addressInput.grid(row=4, column=3, padx=10, pady=10)

        phoneNumberLabel = ttk.Label(self, text="Phone:")
        phoneNumberLabel.grid(row=5, column=1, padx=10, pady=10)

        phoneNumberInput = ttk.Entry(self, textvariable=self.phoneNumber)
        phoneNumberInput.grid(row=5, column=3, padx=10, pady=10)

        genderLabel = ttk.Label(self, text="Gender:")
        genderLabel.grid(row=6, column=1, padx=10, pady=10)

        genderOptions = ttk.OptionMenu(self, self.gender, 'M', *("M","F"))
        genderOptions.grid(row=6, column=3, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Register",
                             command=self.handleRegister)

        # putting the button in its place by
        # using grid
        button1.grid(row=7, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=8, column=1, padx=10, pady=10)

    def setUserType(self,usertype):
        self.domain = usertype

    def handleRegister(self):
        print("regsitered")
        db.createCustomer()