import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label

class CustomerPortal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.domain = tk.StringVar(self)
        # Dropdown menu options
        options = ("Customer", "Administrator")

        dropdownlist = ttk.OptionMenu(self, self.domain, options[0], *options)
        
        dropdownlist.grid(row=0, column=1, padx=10, pady=10)
    