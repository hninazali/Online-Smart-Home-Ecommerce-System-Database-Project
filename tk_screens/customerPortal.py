import tkinter as tk
from tkinter import *

class CustomerPortal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # self.domain = tk.StringVar(self)

        def hello():
            print("hello!")

    # file new function
    # def file_new():
    #     file_new_frame.pack(fill="both", expand=1)


    def menuBar(self,root):
        menubar = tk.Menu(self)
        homeMenu = tk.Menu(self)
        purchaseMenu = tk.Menu(self)
        requestMenu = tk.Menu(self)
        profileMenu = tk.Menu(self)
        nestedHomeMenu = tk.Menu(self)
        nestedPurchaseMenu = tk.Menu(self)
        nestedRequestMenu = tk.Menu(self)
        nestedProfileMenu = tk.Menu(self)

        # pageMenu.add_command(label="PageOne")
        # menubar.add_cascade(label="PageOne", menu=pageMenu)

        menubar.add_cascade(label="Home", menu=homeMenu)
        homeMenu.add_cascade(label="hehehe", menu=nestedHomeMenu)
        # menubar.add_separator()
        menubar.add_cascade(label="Purchases", menu=purchaseMenu)
        purchaseMenu.add_cascade(label="wowooow",menu=nestedPurchaseMenu)

        menubar.add_cascade(label="Service Requests", menu=requestMenu)
        requestMenu.add_cascade(label="heloooo", menu=nestedRequestMenu)

        menubar.add_cascade(label="My Profile", menu=profileMenu)
        profileMenu.add_cascade(label="View Profile", menu=nestedProfileMenu)
        profileMenu.add_cascade(label="Change Password", menu=nestedProfileMenu)
        return menubar


        # root = tk.Frame(self)
        # root.tkraise()

        # my_menu = Menu(root)
        # my_menu = tk.Menu(self)

        # create a menu item
        # file_menu = tk.Menu(my_menu)
        # my_menu.add_cascade(label="File", menu=file_menu)
        # file_menu.add_command(label="New...", command=file_new)
        # file_menu.add_separator()
        # file_menu.add_command(label="Exit", command=root.destroy)

        # create some frames
        # file_new_frame = Frame(root,width=400, height=400, bg="red")


        # self.config(menu=my_menu)




        #  Dummy Display, need to be replaced 
        # options = ("Customer", "Administrator")

        # dropdownlist = ttk.OptionMenu(self, self.domain, options[0], *options)
        
        # dropdownlist.grid(row=0, column=1, padx=10, pady=10)

        

    