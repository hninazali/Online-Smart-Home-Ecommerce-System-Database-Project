import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label
from tk_screens.adminProductSearch import AdminProductSearch 
from tk_screens.adminItemSearch import AdminItemSearch

class CustomerPortal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.domain = tk.StringVar(self)
        
        #  Dummy Display, need to be replaced 
        options = ("Customer", "Administrator")

        dropdownlist = ttk.OptionMenu(self, self.domain, options[0], *options)
        
        dropdownlist.grid(row=0, column=1, padx=10, pady=10)

        button1 = ttk.Button(self, text="Search Product",
                             command=lambda: controller.show_frame(AdminProductSearch))
        button1.grid(row=4, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Search Item",
                             command=lambda: controller.show_frame(AdminItemSearch))
        button2.grid(row=4, column=2, padx=10, pady=10)
    