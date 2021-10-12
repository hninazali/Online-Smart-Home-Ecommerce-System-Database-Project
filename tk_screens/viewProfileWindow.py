from tkinter import Toplevel
import tkinter as tk
from db_connections.mysqldb import SQLDatabase
from tkinter import ttk

class ViewProfileWindow(Toplevel):
    
    def __init__(self, master = None):
        # Pass in the controller from the other frames as master
        super().__init__(master = master)
        self.title("View Profile")
        self.geometry('400x300')

        self['background']='#F6F4F1'
        
        self.userID = self.master.getUserID()
        self.domain = self.master.getDomain()
        self.db = SQLDatabase()
        
        connection = self.db.getConnection()
        cursor = connection.cursor()
        if self.domain == "Customer":
            sql = "SELECT * FROM Customer WHERE customerID = %s"
            cursor.execute(sql, (self.userID))
            details = cursor.fetchone()
            # print(details)
            userIDLabel = ttk.Label(self, text="User ID: {}\nName: {}\nEmail: {}\nAddress: {}\nPhone Number: {}\nGender: {}\n".format(details[0], details[1], details[2], details[4], details[5], details[6]))
            userIDLabel.grid(row=1, column=4, padx=5, pady=5)
        elif self.domain == "Administrator":
            sql = "SELECT * FROM admin WHERE adminID = %s"
            cursor.execute(sql, (self.userID))
            details = cursor.fetchone()
            # print(details)
            userIDLabel = ttk.Label(self, text="User ID: {}\nName: {}\nGender: {}\nPhone Number: {}\n".format(details[0], details[1], details[3], details[4]))
            userIDLabel.grid(row=1, column=4, padx=5, pady=5)
        else:
            raise Exception("Unrecognized domain Error")
        






        

