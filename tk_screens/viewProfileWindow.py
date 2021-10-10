from tkinter import Toplevel
import tkinter as tk

class ViewProfileWindow(Toplevel):
    
    def __init__(self, master = None):
        # Pass in the controller from the other frames as master
        super().__init__(master = master)
        self.title("Search Products")
        self.geometry('1050x600')

        

