# ==================imports===================
import os
from tkinter import *
from tkinter import messagebox

def btn_clicked():
    print("Button Clicked")


window = Tk()
def Exit():
    sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=window)
    if sure == True:
        window.destroy()

window.protocol("WM_DELETE_WINDOW", Exit)

def emp():
    window.withdraw()
    os.system("python employee.py")
    window .deiconify()


def adm():
    window .withdraw()
    os.system("python admin.py")
    window.deiconify()


window.geometry("1000x600")
window.configure(bg = "#aab9c7")
canvas = Canvas(
    window,
    bg = "#aab9c7",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 511, y = 329,
    width = 175,
    height = 124)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    728.5, 147.0,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#eeeded",
    highlightthickness = 0)

entry0.place(
    x = 546.0, y = 131,
    width = 365.0,
    height = 30)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    728.5, 257.0,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#eeeded",
    highlightthickness = 0)

entry1.place(
    x = 546.0, y = 241,
    width = 365.0,
    height = 30)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    417.5, 247.5,
    image=background_img)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b1.place(
    x = 730, y = 328,
    width = 218,
    height = 106)

window.resizable(False, False)
window.mainloop()
