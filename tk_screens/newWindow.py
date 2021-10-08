from tkinter import Toplevel, Label
class NewWindow(Toplevel):
    
    def __init__(self, master = None):
        # Pass in the controller from the other frames as master
        super().__init__(master = master)
        self.title("New Window")
        self.geometry("200x200")
        label = Label(self, text ="This is a new Window")
        label.pack()