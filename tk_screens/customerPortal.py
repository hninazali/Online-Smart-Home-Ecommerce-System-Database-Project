import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label
from tk_screens.adminCategorySearch import AdminCategorySearch

class CustomerPortal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.domain = tk.StringVar(self)
        
        #  Dummy Display 
        options = ("Customer", "Administrator")

        dropdownlist = ttk.OptionMenu(self, self.domain, options[0], *options)
        
        dropdownlist.grid(row=0, column=1, padx=10, pady=10)

        button1 = ttk.Button(self, text="Search Page",
                             command=lambda: controller.show_frame(AdminCategorySearch))

        # putting the button in its place
        # by using grid
        button1.grid(row=4, column=1, padx=10, pady=10)
    