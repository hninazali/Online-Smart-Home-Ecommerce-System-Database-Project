# Comments (25/ 9)
# this page seems to work but login page has error of not being able to detect methods (cuz of the OOP way)
# reference from this youtube video https://www.youtube.com/watch?v=1Bqg6UT8rps
# github code for the video found in https://github.com/hardeepbharaj1295/Python-Tkinter-Mysql/blob/master/login.py


from tkinter import *
import login
from dashboards.dashboard import CustomerDashboard
from dashboards.adminDashboard import AdminDashboard
from actions.registerAdmin import RegisterAdmin as registerAdmin
from actions.registerUser import RegisterUser as registerUser

class WelcomeWindow:

    #create a constructor
    def __init__(self):
        # create a tkinter window
        self.win = Tk()

        #reset the window and background color
        self.canvas = Canvas(self.win, width=600, height=500, bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

        #show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 600 / 2) 
        y = int(height / 2 - 500 / 2)
        str1 = "600x500+"+ str(x) + "+" + str(y)
        self.win.geometry(str1)

        #disable resize of the window
        self.win.resizable(width=False, height=False)

        #change the title of the window
        self.win.title("Online Smart Home Ecommerce System | Welcome Window")

    def frameSwitcher(self, frame_class, username):
        newFrame = frame_class(self, username)
        if self.frame is not None:
            self.frame.destroy()
            #can include conition for if is login screen
        self.frame = newFrame
        self.frame.pack()

    def add_frame(self):
        #create a inner frame
        self.frame = Frame(self.win, height=300, width=450)
        self.frame.place(x=80, y=50)

        x, y = 70, 20

        # place the photo in the frame
        # you can find the images from flaticon.com site
        self.img = PhotoImage(file='images/welcome.png')
        self.label = Label(self.frame, image=self.img)
        self.label.place(x=x+80, y=y+0)

        #create login form
        self.labeltitle = Label(self.frame, text="Welcome to Online Smart Home Ecommerce System")
        self.labeltitle.config(font=("Courier", 14, 'bold'))
        self.labeltitle.place(x=40, y=y+150)

        self.button = Button(self.frame, text="Continue", font=('helvetica', 20, 'italic')
                             , bg='dark green', fg='black', command=self.login)
        self.button.place(x=x+80, y=y+200)

        self.win.mainloop()

    #open a new window on button press
    def login(self):
        # destroy current window
        self.win.destroy()
        #open the new window
        log = login.LoginWindow()
        log.add_frame()

    def refresh(self):
        self.destroy()
        self.__init__()


if __name__ == "__main__":
    x = WelcomeWindow()
    x.add_frame()
    x.mainloop()