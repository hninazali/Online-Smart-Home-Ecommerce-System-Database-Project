import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, Entry
from db_connections.mysqldb import SQLDatabase

db = SQLDatabase()

class AdminPortal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.domain = tk.StringVar(self)

        # Reset Button
        resetButton = ttk.Button(self, text="Reset SQLDB", command=self.resetDB)
        resetButton.grid(row=0, column=1, padx=10, pady=10)
        #  Dummy Display 
        options = ("Customer", "Administrator")

        dropdownlist = ttk.OptionMenu(self, self.domain, options[0], *options)
        
        dropdownlist.grid(row=1, column=1, padx=10, pady=10)

    def resetDB(self):
        db.resetMySQLState()
# In addition, provide a MYSQL database initialization function under the Administrator login. 
# At the beginning of your  presentation, you are required to apply this function to reinitialize the MYSQL database. 
# When the MYSQL database is initialized,  provide a function to allow the Administrator to display the following information (Purchase status= “SOLD” and  Purchase status=“UNSOLD”) on the items in the MySQL tables:


# Comment : more screns for the admin portal will be defined as individual page/ popup classes in this file

# DB_CONFIG = {
#     'host': 'localhost',
#     'user': 'loff',
#     'pass': 'loff',
#     'db': 'loff',
#     'char': 'utf8',
#     'file': 'create-db-loff.sql'
# }

# def get_sql_from_file(filename=DB_CONFIG['file']):
#     """
#     Get the SQL instruction from a file

#     :return: a list of each SQL query whithout the trailing ";"
#     """
#     from os import path

#     # File did not exists
#     if path.isfile(filename) is False:
#         print("File load error : {}".format(filename))
#         return False

#     else:
#         with open(filename, "r") as sql_file:
#             # Split file in list
#             ret = sql_file.read().split(';')
#             # drop last empty entry
#             ret.pop()
#             return ret

# request_list = self.get_sql_from_file()

# if request_list is not False:

#     for idx, sql_request in enumerate(request_list):
#         self.message = self.MSG['request'].format(idx, sql_request)
#         cursor.execute(sql_request + ';')