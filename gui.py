# code referenced and modified from this tutorial : https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/

import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label
from db_connections.mysqldb import SQLDatabase

LARGEFONT = ("Verdana", 35)

from tk_screens.authScreens import *
from tk_screens.customerPortal import *

class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):

        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # Variables that persist through frames
        self.domain = None

        # iterating through a tuple consisting
        # of the different page layouts
        # all new pages created add here
        for F in (StartPage, LoginPage, RegisterPage, CustomerPortal, AdminCategorySearch):

            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont, domain=None):
        frame = self.frames[cont]
        frame.tkraise()
        if domain:
            frame = self.frames[cont]
            frame.setUserType(domain)
            frame.tkraise()
            self.domain = domain
        else:
            frame = self.frames[cont]
            frame.tkraise()

    def getDomain(self):
        return self.domain



# Driver Code
app = tkinterApp()
app.mainloop()
