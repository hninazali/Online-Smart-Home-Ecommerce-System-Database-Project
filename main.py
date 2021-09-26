from tkinter import *
from tk_screens.authScreen import LoginWindow, RegisterWindow

class WelcomeWindow:

    #create a constructor
    def __init__(self):
        # create a tkinter window
        self.win = Tk()

        #reset the window and background color
        self.canvas = Canvas(self.win, width=1000, height=800, bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 1000 / 2)
        y = int(height / 2 - 800 / 2)
        str1 = "1000x800+" + str(x) + "+" + str(y)
        self.win.geometry(str1)

        #disable resize of the window
        self.win.resizable(width=False, height=False)

        #change the title of the window
        self.win.title("Online Smart Home Ecommerce System | Welcome Window")
        self.domain = StringVar()

    def add_frame(self):
        #create a inner frame
        self.frame = Frame(self.win, height=800, width=750)
        self.frame.place(x=150, y=10)

        x, y = 70, 20

        # place the photo in the frame
        # you can find the images from flaticon.com site
        self.img = PhotoImage(file='images/welcome.png')
        self.label = Label(self.frame, image=self.img)
        self.label.place(x=x+80, y=y+0)

        self.labeltitle = Label(self.frame, text="Welcome to Online Smart Home Ecommerce System")
        self.labeltitle.config(font=("helvetica", 20, 'bold'))
        self.labeltitle.place(x=10, y=y+150)

        self.Loginbutton = Button(self.frame,  text="Login", font=(
            'helvetica', 20), bg='dark green', fg='white', command=self.login)
        self.Loginbutton.place(x=x+30, y=y+200)

        self.Registerbutton = Button(self.frame, text="Register", font=(
            'helvetica', 20), bg='dark green', fg='white', command=self.register)
        self.Registerbutton.place(x=x+30, y=y+250)

        # Dropdown menu options
        options = ["Customer", "Administrator"]
        
        # initial menu text
        self.domain.set("Choose User Type")
        
        # Create Dropdown menu
        drop = OptionMenu( self.frame , self.domain , *options )
        drop.place(x=x+30, y=y+300)

        self.win.mainloop()

    #open a new window on button press
    def login(self):
        # destroy current window
        self.win.destroy()

        #open the new window
        log = LoginWindow()
        log.add_frame()

    def register(self):
        self.win.destroy()

        regis = RegisterWindow()
        regis.add_frame()

    def getUserType(self):
        return self.domain

if __name__ == "__main__":
    x = WelcomeWindow()
    x.add_frame()
