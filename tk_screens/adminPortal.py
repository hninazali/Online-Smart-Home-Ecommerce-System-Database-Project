import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, Entry
from db_connections.mysqldb import SQLDatabase

db = SQLDatabase()

# class Table:
      
#     def __init__(self,root, total_rows, total_columns, i=0, j=0):
#     # code for creating table
#         for i in range(total_rows):
#             for j in range(total_columns):
                
#                 self.e = Entry(root, width=20, fg='blue',
#                                 font=('Arial',16,'bold'))
                    
#                 self.e.grid(row=i, column=j)
#                 self.e.insert(i, lst[i][j])

class Table:
    def __init__(self, parent, columns):
        self.tree = ttk.Treeview(parent, columns=columns, show='headings')
        self.tree.heading('#1', text='First Name')
        self.tree.heading('#2', text='Last Name')
        self.tree.heading('#3', text='Email')

        contacts = []
        for n in range(1, 100):
            contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

        for contact in contacts:
            self.tree.insert('', tk.END, values=contact)

        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
    
    # bind the select event
    def item_selected(self, event):
        for selected_item in self.tree.selection():
            # dictionary
            item = self.tree.item(selected_item)
            # list
            record = item['values']
            #
            tk.showinfo(title='Information',
                    message=','.join(record))


    def getTree(self):
        return self.tree



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

        # table = Table(self, ['#1', '#2', '#3']).getTree()
        # table.grid(row=2, column=1, padx=10, pady=10)

        columns = ('#1', '#2', '#3')

        tree = ttk.Treeview(self, columns=columns, show='headings')

        # define headings
        tree.heading('#1', text='First Name')
        tree.heading('#2', text='Last Name')
        tree.heading('#3', text='Email')

        # generate sample data
        contacts = []
        for n in range(1, 100):
            contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

        # adding data to the treeview
        for contact in contacts:
            tree.insert('', tk.END, values=contact)


        # bind the select event
        def item_selected(event):
            for selected_item in tree.selection():
                # dictionary
                item = tree.item(selected_item)
                # list
                record = item['values']
                #
                tk.showinfo(title='Information',
                        message=','.join(record))


        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.grid(row=2, column=0, sticky='nsew')


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