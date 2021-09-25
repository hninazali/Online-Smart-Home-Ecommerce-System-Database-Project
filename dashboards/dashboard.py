import tkinter as tk
import tkinter.ttk as ttk
import time
import os
import sys
from userProfile import UserProfilePage
# from lib.purchases import *
# from lib.request import *
# import lib.mongodb as mongodb
import login as login
from mysql_connections.mysqldb import SQLDatabase
from datetime import date

class CustomerDashboard(tk.Frame): 
    def __init__(self, username):
        ttk.Frame.__init__(self, self.win)
        self.username=username
        print(self.username)
        # Setting Window Width and height and anchor window to center of screen
        win_width, win_height = 1366, 768
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (win_width/2))-5
        y_cordinate = int((screen_height/2) - (win_height/2)) - 15
        self.win.geometry("{}x{}+{}+{}".format(win_width, win_height,
                                             x_cordinate, y_cordinate))
        self.win.resizable(0, 0)
        self.win.title("Online Smart Home Ecommerce System")
        self.win.iconbitmap("static/shopping.ico")
        bg_frame = ttk.Frame(self.win, width = win_width,height = win_width)
        bg_frame.place(x=0,y=0)

        #================ NavBar ==================#
        self.navBar = tk.LabelFrame(width=1366, height=130, bg="#4267b2")
        self.navBar.place(x=0, y=0)

        #home button
        home_icon = tk.PhotoImage(
            file='images/home_icon.png')
        home_btn = tk.Button(self.navBar, image=home_icon, bd=0,background='#4267b2',activebackground='#4267b2',)
        home_btn.image = home_icon
        home_btn.place(x=15,y=10)

        #Profile button
        profile_icon = tk.PhotoImage(file='images/profile_icon.png')
        profile_btn = tk.Button(self.navBar,image=profile_icon, bd=0,background='#4267b2',activebackground='#4267b2',command=lambda:self.win.frameSwitcher(UserProfilePage, self.username))
        profile_btn.image = profile_icon
        profile_btn.place(x=1150,y=10)

        #logout button
        logout_icon = tk.PhotoImage(file='images/logout_icon.png')

        '''
        To add: command to link to login page
        '''
        logout_btn = tk.Button(self.navBar, image=logout_icon, bd=0,background='#4267b2',activebackground='#4267b2',command=lambda:self.win.frameSwitcher(login.Login, None))
        logout_btn.image = logout_icon
        logout_btn.place(x=1250,y=10)

if __name__ == "__main__":
    customerDashboard = CustomerDashboard()
    customerDashboard.mainloop()