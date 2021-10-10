from tkinter import Toplevel
from tkinter import ttk
import tkinter as tk
from db_connections.mysqldb import SQLDatabase


class ChangePasswordWindow(Toplevel):
    
    def __init__(self, master = None):
        # Pass in the controller from the other frames as master
        super().__init__(master = master)
        self.db = SQLDatabase()

        self.title("Search Products")
        self.geometry('400x300')
        self.master = master # Controller in frames

        self.oldPassword = tk.StringVar()
        self.newPassword = tk.StringVar()

        pass1Label = ttk.Label(self, text="Old Password:")
        pass1Label.grid(row=0, column=1, padx=5, pady=5)
        pass1Input = ttk.Entry(self, textvariable=self.oldPassword)
        pass1Input.grid(row=0, column=3,  padx=5, pady=5)

        pass2Label = ttk.Label(self, text="New Password:")
        pass2Label.grid(row=1, column=1, padx=5, pady=5)
        pass2Input = ttk.Entry(self, textvariable=self.newPassword)
        pass2Input.grid(row=1, column=3,  padx=5, pady=5)


        button1 = ttk.Button(self, text="Change Password",
                             command=self.handleChangePassword)

        button1.grid(row=2, column=2, padx=5, pady=5)

    # Returns a string if the login was successful or failed
    def checkAuthState(self):
        userID = self.master.getUserID()
        domain = self.master.getDomain()
        if domain == "Customer":
            return self.db.getCustomerLogin(userID, self.oldPassword.get())
        elif domain == "Admin":
            return self.db.getAdminLogin(userID, self.oldPassword.get())
        else:
            raise Exception("Check User type in changePasswordwindow.py")

    def handleChangePassword(self):
        if self.checkAuthState() == "User doesn't exist" or self.checkAuthState() =="Incorrect Password":
            print("Auth Error! Please check password"+self.checkAuthState()) # TODO: Change to popup or warning
        else:
            print("Password Change Approved:", self.checkAuthState())
            self.db.changePassword(self.newPassword.get(), self.master.getUserID(), self.master.getDomain())

