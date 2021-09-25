import tkinter as tk
from tkinter import messagebox
from tkinter.constants import BOTH, CENTER, DISABLED, END, LEFT, NORMAL
import tkinter.ttk as ttk
from typing import Text
from dashboards.dashboard import CustomerDashboard
# import lib.purchases as purchase
from mysql_connections.mysqldb import SQLDatabase
# import lib.request as request
from login import LoginWindow 
import re

class UserProfilePage(tk.Frame):
    def __init__(self,master, username):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.username = username
        database = SQLDatabase()
        self.info = database.getCustLogin(self.username)
        win_width, win_height = 1366, 768
        bg_frame = ttk.Frame(master,width=win_width,height=win_height)


        #================ NavBar ==================#
        self.navBar = tk.LabelFrame(width=1600, height=130, bg="#4267b2")
        self.navBar.place(x=0, y=0)
        #home button
        home_icon = tk.PhotoImage(
            file='images/home_icon.png')
        home_btn = tk.Button(self.navBar, image=home_icon, bd=0,background='#4267b2',activebackground='#4267b2',command=lambda:master.frameSwitcher(CustomerDashboard, self.username))
        home_btn.image = home_icon
        home_btn.place(x=15,y=10)

        # purchase button
        '''
        To add: command to link to purchase page
        '''
        purchase_img = tk.PhotoImage(
            file='images/purchase_outline.png')
        purchase_btn = tk.Button(self.navBar, image=purchase_img, bd=0,background='#4267b2',activebackground='#4267b2',command=lambda:master.frameSwitcher(purchase.PurchasePage, self.username))
        purchase_btn.image = purchase_img
        purchase_btn.place(x=160,y=0)

        # request button
        # request_label = tk.Label(self.navBar,text= "Your \n Requests",bg="#4267b2",anchor="center")
        # request_label.config(font="Verdana 20 bold",fg="snow")
        # request_label.place(x=500,y=20)
        '''
        To add: command to link to request page
        '''
        request_img = tk.PhotoImage(
            file='images/request_outline.png')
        request_btn = tk.Button(self.navBar, image=request_img, bd=0,background='#4267b2',activebackground='#4267b2',command=lambda:master.frameSwitcher(request.RequestPage, self.username))
        request_btn.image = request_img
        request_btn.place(x=360,y=0)

        '''
        To add: command to fetch name
        '''
        customer_img = tk.PhotoImage(
            file='images/customer.png')
        customer_label = tk.Label(self.navBar,image=customer_img,background='#4267b2')
        customer_label.image = customer_img
        customer_label.place(x = 980, y = 0)
        #Profile button
        profile_icon = tk.PhotoImage(file='static/profile_icon.png')
        profile_btn = tk.Button(self.navBar,image=profile_icon, bd=0,background='#4267b2',activebackground='#4267b2',)
        profile_btn.image = profile_icon
        profile_btn.place(x=1150,y=10)
        
        #logout button
        logout_icon = tk.PhotoImage(file='static/logout_icon.png')
        '''
        To add: command to link to login page
        '''
        logout_btn = tk.Button(self.navBar, image=logout_icon, bd=0,background='#4267b2',activebackground='#4267b2',command=lambda:master.frameSwitcher(LoginWindow, None))
        logout_btn.image = logout_icon
        logout_btn.place(x=1250,y=10)
        
        #================ Scroll Frame ==================#
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
        canvas = tk.Canvas(bg_frame, width=win_width- 55,height=win_height-140)
        scrollbar = ttk.Scrollbar(bg_frame, orient="vertical", command=canvas.yview)
        canvas.bind('<Configure>', on_configure)
        frame = ttk.Frame(canvas)
        canvas.create_window((win_width / 2 - 350,100), window=frame, anchor='nw')  
        canvas.configure(yscrollcommand = scrollbar.set)

        #================ bodyFrame ==================#
        profile_frame = ttk.Frame(frame)

        #change password

        changePassLabel = ttk.Label(frame, text="Change Password",font="Montserrat 20 bold",foreground='#4267b2')
        changePassLabel.pack(pady=25)
        chgPassFrame = ttk.Frame(frame)
        chgPassFrame.pack()

        currentPassLabel = tk.Label(chgPassFrame, text="Current Password")
        currentPassLabel.grid(row=1, column=0,padx=25, pady=25)
        currentPassEntry = tk.Entry(chgPassFrame, show="*")
        currentPassEntry.grid(row = 1, column=1)

        newPassLabel = tk.Label(chgPassFrame, text = "New Password")
        newPassLabel.grid(row=1, column=2,padx=25, pady=25)
        newPassEntry = tk.Entry(chgPassFrame, show="*")
        newPassEntry.grid(row=1,column=3)

        def changePass():
            currentPass = currentPassEntry.get()
            newPass = newPassEntry.get()

            #database query
            custPass = self.info[6]
            if currentPass == "" or newPass == "":
                messagebox.showerror("Error", "Password fields cannot be left blank")
                return
            if currentPass != custPass:
                messagebox.showerror("Error", "Current Password is incorrect!")
                return
            if len(newPass) < 6:
                messagebox.showerror("Error", "New password has to be more than 6 characters")
                return
            database.changePassword(newPass, self.username, False)
            messagebox.showinfo("Success", "Password changed successfully")
            return
            
        changePassBtn = tk.Button(frame, text="Change Password",font="Montserrat 12 bold",anchor="center",fg="#FFFFFF",bg="#4267b2",width=15,command=changePass)
        changePassBtn.pack()

        divider = tk.Label(frame, text="____________________________________________________________________________________________________________________________")
        divider.pack()

        #change email
        changeEmailLabel = tk.Label(frame, text="Change Email",font="Montserrat 20 bold",foreground='#4267b2')
        changeEmailLabel.pack(pady=25)
        chgEmailFrame = tk.Frame(frame, border = 1)
        chgEmailFrame.pack()

        currentEmailLabel = tk.Label(chgEmailFrame, text="Current Email")
        currentEmailLabel.grid(row=1, column=0,padx=25)
        currentEmailEntry = tk.Entry(chgEmailFrame)
        currentEmailEntry.grid(row = 1, column=1)
        currentEmailEntry.insert(0, self.info[3])
        currentEmailEntry.configure(state=DISABLED)

        newEmailLabel = tk.Label(chgEmailFrame, text = "New Email")
        newEmailLabel.grid(row=1, column=2,padx=25, pady=25)
        newEmailEntry = tk.Entry(chgEmailFrame)
        newEmailEntry.grid(row=1,column=3)

        def changeEmail():
            newEmail = newEmailEntry.get()
            regexEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if newEmail == "":
                messagebox.showerror("Error", "Email field cannot be left blank")
                return
            if (not re.fullmatch(regexEmail, newEmail)):
                messagebox.showerror("Error", "Invalid Email!")
                return
            database.changeEmail(newEmail, self.username)
            messagebox.showinfo("Success", "Email changed successfully")
            currentEmailEntry.configure(state=NORMAL)
            currentEmailEntry.delete(0, END)
            currentEmailEntry.insert(0, newEmail)
            currentEmailEntry.configure(state=DISABLED)
            return
            
        changeEmailBtn = tk.Button(frame, text="Change Email",font="Montserrat 12 bold",anchor="center",fg="#FFFFFF",bg="#4267b2",width=15, command=changeEmail)
        changeEmailBtn.pack()

        divider = tk.Label(frame, text="____________________________________________________________________________________________________________________________")
        divider.pack()

        #change number
        changeNumLabel = tk.Label(frame, text="Change Number",font="Montserrat 20 bold",foreground='#4267b2')
        changeNumLabel.pack(pady=25)
        chgNumFrame = tk.Frame(frame, border = 1)
        chgNumFrame.pack()


        currentNumLabel = tk.Label(chgNumFrame, text="Current Number")
        currentNumLabel.grid(row=1, column=0,padx=25)
        currentNumEntry = tk.Entry(chgNumFrame)
        currentNumEntry.grid(row = 1, column=1)
        currentNumEntry.insert(0, self.info[4])
        currentNumEntry.configure(state=DISABLED)

        newNumLabel = tk.Label(chgNumFrame, text = "New Number")
        newNumLabel.grid(row=1, column=2,padx=25, pady=25)
        newNumEntry = tk.Entry(chgNumFrame)
        newNumEntry.grid(row=1,column=3)

        def changeNum():
            newNum = newNumEntry.get()
            regexNum = r'^\d+$'
            if newNum == "":
                messagebox.showerror("Error", "Number field cannot be left blank")
                return
            if (not re.fullmatch(regexNum, newNum) or len(newNum) != 8):
                messagebox.showerror("Error", "Invalid Number!") 
                return
            database.changeNum(newNum, self.username, False)
            messagebox.showinfo("Success", "Number changed successfully")
            currentNumEntry.configure(state=NORMAL)
            currentNumEntry.delete(0, END)
            currentNumEntry.insert(0, newNum)
            currentNumEntry.configure(state=DISABLED)
            return
            
        changeNumBtn = tk.Button(frame, text="Change Number",font="Montserrat 12 bold",anchor="center",fg="#FFFFFF",bg="#4267b2",width=15, command=changeNum)
        changeNumBtn.pack()
        
        divider = tk.Label(frame, text="____________________________________________________________________________________________________________________________")
        divider.pack()

        #change address
        changeAddrLabel = tk.Label(frame, text="Change Address",font="Montserrat 20 bold",foreground='#4267b2')
        changeAddrLabel.pack(pady=25)
        chgAddrFrame = tk.Frame(frame, border = 1)
        chgAddrFrame.pack()

        currentAddrLabel = tk.Label(chgAddrFrame, text="Current Address")
        currentAddrLabel.grid(row=1, column=0,padx=25)
        currentAddrEntry = tk.Entry(chgAddrFrame)
        currentAddrEntry.grid(row = 1, column=1)
        currentAddrEntry.insert(0, self.info[5])
        currentAddrEntry.configure(state=DISABLED)

        newAddrLabel = tk.Label(chgAddrFrame, text = "New Address")
        newAddrLabel.grid(row=1, column=2,padx=25, pady=25)
        newAddrEntry = tk.Entry(chgAddrFrame)
        newAddrEntry.grid(row=1,column=3)

        def changeAddr():
            newAddr = newAddrEntry.get()
            if newAddr == "":
                messagebox.showerror("Error", "Address field cannot be left blank")
                return
            if (len(newAddr) <5):
                messagebox.showerror("Error", "Invalid Address!") 
                return
            #new Addr to SQLDatabase
            database.changeAddress(newAddr, self.username)
            messagebox.showinfo("Success", "Address changed successfully")
            currentAddrEntry.configure(state=NORMAL)
            currentAddrEntry.delete(0, END)
            currentAddrEntry.insert(0, newAddr)
            currentAddrEntry.configure(state=DISABLED)
            return
            
        changeAddrBtn = tk.Button(frame, text="Change Address",font="Montserrat 12 bold",anchor="center",fg="#FFFFFF",bg="#4267b2",width=15, command=changeAddr)
        changeAddrBtn.pack()
        
        
        profile_frame.pack()
        bg_frame.place(x = 33, y = 125) 
        canvas.pack(side=LEFT, fill="both", expand=True)
        scrollbar.pack(side="right", fill='y')

if __name__ == "__main__":
    profile = UserProfilePage()
    profile.mainloop()