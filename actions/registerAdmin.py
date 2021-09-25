import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Menu, messagebox
import re
from dashboards.adminDashboard import AdminDashboard
import login as login
from mysql_connections.mysqldb import SQLDatabase
# import lib.request as request

class RegisterAdmin(tk.Frame):
    def __init__(self,master, username):
        self.username = username
        database = SQLDatabase()
        ttk.Frame.__init__(self, master)
        # Setting Window Width and height and anchor window to center of screen
        win_width, win_height = 1366, 768
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (win_width/2))-5
        y_cordinate = int((screen_height/2) - (win_height/2)) - 15
        master.geometry("{}x{}+{}+{}".format(win_width, win_height,
                                             x_cordinate, y_cordinate))
        master.resizable(0, 0)
        master.title("Online Smart Home Ecommerce System")
        master.iconbitmap("images/shopping.ico")
        bg_frame = ttk.Frame(master, width = win_width,height = win_width)
        bg_frame.place(x=0,y=0)

        #================ NavBar ==================#
        self.navBar = tk.LabelFrame(width=1600, height=130, bg="#4267b2")
        self.navBar.place(x=0, y=0)

        #home button
        home_icon = tk.PhotoImage(
            file='images/home_icon.png')
        home_btn = tk.Button(self.navBar, image=home_icon, bd=0,background='#4267b2',activebackground='#4267b2',command=lambda:master.frameSwitcher(login.LoginWindow, None))
        home_btn.image = home_icon
        home_btn.place(x=15,y=10)

        #================ Admin Registration box ==================#
        form_frame = ttk.Frame(bg_frame,border=1)
        form_frame.place(x=450,y=125,width=500,height=1000)
        form_heading  = ttk.Label(form_frame,text = "Register as Admin", font="Montserrat 20 bold",foreground='#4267b2')
        form_heading.grid(row=0,column=1,padx=25,pady=30)
        
        #Labels for input fields
        username = tk.Label(form_frame, text="Username")
        name = tk.Label(form_frame, text="Name")
        gender = tk.Label(form_frame, text="Gender")
        email = tk.Label(form_frame, text="Email")
        phoneNum = tk.Label(form_frame, text="Contact Number")
        password = tk.Label(form_frame, text="Password")
        confirmPass= tk.Label(form_frame, text="Confirm Password")

        #will organise into 2 seperate columns next time
        username.grid(row=1, column=0, pady=10)
        name.grid(row=2, column=0, pady=10)
        gender.grid(row=3, column=0, pady=10)
        email.grid(row=4, column=0, pady=10)
        phoneNum.grid(row=5, column=0, pady=10)
        password.grid(row=7, column=0, pady=10)
        confirmPass.grid(row=8, column=0, pady=10)

        #Entry boxes for entering info
        username_field = tk.Entry(form_frame)
        name_field = tk.Entry(form_frame)
        gender_field = ttk.Combobox(form_frame, width = 18, state="readonly", values=('M', "F", "Others"))
        email_field = tk.Entry(form_frame)
        phoneNum_field = tk.Entry(form_frame)
        address_field = tk.Entry(form_frame)
        password_field = tk.Entry(form_frame, show="*")
        confirmPass_field = tk.Entry(form_frame, show="*")

        username_field.grid(row=1, column=1, ipadx="100")
        name_field.grid(row=2, column=1, ipadx="100")
        gender_field.grid(row=3, column=1, ipadx="100")
        email_field.grid(row=4, column=1, ipadx="100")
        phoneNum_field.grid(row=5, column=1, ipadx="100")
        address_field.grid(row=6, column=1, ipadx="100")
        password_field.grid(row=7, column=1, ipadx="100")
        confirmPass_field.grid(row=8, column=1, ipadx="100")

        def registerAdmin():
            regexEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            regexNum = r'^\d+$'
            if (len(username_field.get()) < 6):
                messagebox.showerror("Error", "Username has to be at least 6 characters")
                return
            if (not name_field.get()):
                messagebox.showerror("Error", "Name field cannot be left blank!")
                return
            if (not gender_field.get()):
                messagebox.showerror("Error", "Gender cannot be left blank!")
                return
            if (not re.fullmatch(regexEmail, email_field.get())):
                messagebox.showerror("Error", "Invalid Email!")
                return
            if (len(phoneNum_field.get()) != 8 or not re.fullmatch(regexNum, phoneNum_field.get())):
                messagebox.showerror("Error", "Not a valid phone number!")
                return
            if (len(address_field.get()) < 5):
                messagebox.showerror("Error", "Not a valid address")
                return
            if (password_field.get() != confirmPass_field.get()):
                messagebox.showerror("Error", "Passwords do not match!")
                return
            if (len(password_field.get()) < 6):
                messagebox.showerror("Error", "Password has to be at least 6 characters")
                return
            #insert database logic and change frame switcher to admin main page
            database.createAdmin((username_field.get(), name_field.get(), gender_field.get(),
                    email_field.get(), phoneNum_field.get(), address_field.get(), password_field.get()))
            master.frameSwitcher(AdminDashboard, username_field.get())
            

        submit = tk.Button(form_frame, text="Submit", command=RegisterAdmin)
        submit.grid(row=9, column=1)

if __name__ == "__main__":
    registerAdmin = RegisterAdmin()
    registerAdmin.mainloop()