import tkinter as tk
from tkinter import *

class CustomerPortal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.domain = tk.StringVar(self)
        self.controller = controller

    # file new function
    # def file_new():
    #     file_new_frame.pack(fill="both", expand=1)

    def hello(self):
        print("hello")


    def menuBar(self,root):
        menubar = tk.Menu(root)
        # nestedProductMenu = tk.Menu(self)
        # nestedItemMenu = tk.Menu(self)
        # nestedRequestMenu = tk.Menu(self)
        # nestedServiceMenu = tk.Menu(self)
        # nestedProfileMenu = tk.Menu(self)

        #home - view products
        productMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Home", menu=productMenu)
        productMenu.add_command(label="View Products", command=self.hello)
        # productMenu.add_cascade(label="hehehe", menu=nestedProductMenu) #only for adding more nested menus to menus


        #purchases
        purchaseMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Purchases", menu=purchaseMenu)
        purchaseMenu.add_command(label="View My Purchases", command=self.hello)
        # itemMenu.add_cascade(label="wowooow",menu=nestedItemMenu)
        
        #service requests
        requestMenu = tk.Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Service Requests", menu=requestMenu)
        requestMenu.add_command(label="View My Service Requests", command=self.hello)
    #     requestMenu.add_cascade(label="heloooo", menu=nestedRequestMenu)


        #profile
        profileMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="My Profile", menu=profileMenu)
        profileMenu.add_command(label="View Profile", command=self.hello)
        profileMenu.add_separator()
        profileMenu.add_command(label="Logout", command=self.hello)      
        
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


        

    