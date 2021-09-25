# Comments (25/ 9)
# Error : name 'login' is not defined in command = login

from tkinter import *
from tkinter import messagebox
import os
from mysql_connections.mysqldb import SQLDatabase
#import dashboard


class LoginWindow : 

    def __init__(self):
        self.win = Tk()
        db = SQLDatabase()
        # reset the window and background color
        self.canvas = Canvas(self.win, width=600, height=500, bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 600 / 2)
        y = int(height / 2 - 500 / 2)
        str1 = "600x500+" + str(x) + "+" + str(y)
        self.win.geometry(str1)

        self.win.resizable(0, 0)

    #     # disable resize of the window
    #     self.win.resizable(width=False, height=False)

        # change the title of the window
        self.win.title("Online Smart Home Ecommerce System | Login Window ")
        # self.win.iconbitmap(r"images/welcome.png")
    
    def add_frame(self):
        self.frame = Frame(self.win, height=400, width=450)
        self.frame.place(x=80, y=50)

        x, y = 70, 20
        self.img = PhotoImage(file='images/login.png')
        self.label = Label(self.frame, image=self.img)
        self.label.place(x = x + 80, y = y + 0)


    # remaining : add navbar


    # Designing window for registration
    def register(self):
        global register_screen
        register_screen = Toplevel(main_screen)
        register_screen.title("Register")
        register_screen.geometry("300x250")

        global username
        global password
        global username_entry
        global password_entry
        username = StringVar()
        password = StringVar()

        Label(register_screen, text="Please enter details below", bg="white").pack()
        Label(register_screen, text="").pack()
        username_lable = Label(register_screen, text="Username * ")
        username_lable.pack()
        username_entry = Entry(register_screen, textvariable=username)
        username_entry.pack()
        password_lable = Label(register_screen, text="Password * ")
        password_lable.pack()
        password_entry = Entry(register_screen, textvariable=password, show='*')
        password_entry.pack()
        Label(register_screen, text="").pack()
        Button(register_screen, text="Register", width=10, height=1, bg="blue", command = self.register_user).pack()


    # Designing window for login 

    def login(self):
        global login_screen
        login_screen = Toplevel(main_screen)
        login_screen.title("Login")
        login_screen.geometry("300x250")
        Label(login_screen, text="Please enter details below to login").pack()
        Label(login_screen, text="").pack()

        global username_verify
        global password_verify

        username_verify = StringVar()
        password_verify = StringVar()

        global username_login_entry
        global password_login_entry

        Label(login_screen, text="Username * ").pack()
        username_login_entry = Entry(login_screen, textvariable=username_verify)
        username_login_entry.pack()
        Label(login_screen, text="").pack()
        Label(login_screen, text="Password * ").pack()
        password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
        password_login_entry.pack()
        Label(login_screen, text="").pack()
        Button(login_screen, text="Login", width=10, height=1, command = self.login_verify).pack()

    # Implementing event on register button

    def register_user(self):

        username_info = username.get()
        password_info = password.get()

        file = open(username_info, "w")
        file.write(username_info + "\n")
        file.write(password_info)
        file.close()

        username_entry.delete(0, END)
        password_entry.delete(0, END)

        Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()

    # Implementing event on login button 

    def login_verify(self):
        username1 = username_verify.get()
        password1 = password_verify.get()
        username_login_entry.delete(0, END)
        password_login_entry.delete(0, END)
        
        SQLDatabase.getAdminLogin(username, password) # change pls


        list_of_files = os.listdir()
        if username1 in list_of_files:
            file1 = open(username1, "r")
            verify = file1.read().splitlines()
            if password1 in verify: 
                self.login_sucess()

            else:
                self.password_not_recognised()

        else:
            self.user_not_found()

    # Designing popup for login success

    def login_sucess(self):
        global login_success_screen
        login_success_screen = Toplevel(login_screen)
        login_success_screen.title("Success")
        login_success_screen.geometry("150x100")
        Label(login_success_screen, text="Login Success").pack()
        Button(login_success_screen, text="OK", command=self.delete_login_success).pack()

    # Designing popup for login invalid password

    def password_not_recognised(self):
        global password_not_recog_screen
        password_not_recog_screen = Toplevel(login_screen)
        password_not_recog_screen.title("Success")
        password_not_recog_screen.geometry("150x100")
        Label(password_not_recog_screen, text="Invalid Password ").pack()
        Button(password_not_recog_screen, text="OK", command=self.delete_password_not_recognised).pack()

    # Designing popup for user not found

    def user_not_found(self):
        global user_not_found_screen
        user_not_found_screen = Toplevel(login_screen)
        user_not_found_screen.title("Success")
        user_not_found_screen.geometry("150x100")
        Label(user_not_found_screen, text="User Not Found").pack()
        Button(user_not_found_screen, text="OK", command=self.delete_user_not_found_screen).pack()

    # Deleting popups

    def delete_login_success(self):
        login_success_screen.destroy()


    def delete_password_not_recognised(self):
        password_not_recog_screen.destroy()


    def delete_user_not_found_screen(self):
        user_not_found_screen.destroy()


        # Designing Main(first) window

    def main_account_screen(self):
        global main_screen
        main_screen = Tk()
        main_screen.geometry("300x250")
        main_screen.title("Account Login")
        Label(text="Select Your Action", bg="gray", width="300", height="2", fg="white", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Button(text="Login", height="2", width="30", command=self.login).pack()
        Label(text="").pack()
        Button(text="Register", height="2", width="30", command=self.register).pack()

        main_screen.mainloop()

 

logmein = LoginWindow()
logmein.main_account_screen()

