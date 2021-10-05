import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import pymongo


class searchFunction:
    def __init__(self):
         
        # simpleSearch
        self.searchFunction = tk.Tk()
        self.searchFunction.title("Search for your favourite products!")
        self.searchFunction.geometry('480x320')

        self.simpleSearchLabel = ttk.Label(self.searchFunction)
        self.simpleSearchLabel.configure(anchor='ne', background='#0bbbce', compound='bottom', font='TkIconFont')
        self.simpleSearchLabel.configure(foreground='#000000', text='Simple Search')
        self.simpleSearchLabel.place(anchor='nw', relx='0.42', rely='0.02', x='0', y='0')

        self.categoryLabel = ttk.Label(self.searchFunction)
        self.categoryLabel.configure(text='Category')
        self.categoryLabel.place(anchor='nw', relx='0.42', rely='0.1', x='0', y='0')

        vModel=[]
        self.modelBox = ttk.Combobox(self.searchFunction, values = vModel)
        self.modelBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.modelBox.place(anchor='nw', relx='0.6', rely='0.2', x='0', y='0')

        #ensure that only the right model shows when category selected
        def categoryAndModel(event):
            if self.categoryBox.get()=="Lights":
                vModel = ["Light1", "Light2", "SmartHome1",""]
            elif self.categoryBox.get()=="Locks":
                vModel = ["Safe1", "Safe2", "Safe3", "SmartHome1",""]
            else:
                vModel = []
            self.modelBox.configure(values = vModel)

        self.categoryBox = ttk.Combobox(self.searchFunction, values = ["Lights", "Locks",""])
        self.categoryBox.bind('<<ComboboxSelected>>', categoryAndModel)
        self.categoryBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.categoryBox.place(anchor='nw', relx='0.6', rely='0.1', x='0', y='0')
        


        self.searchButton = ttk.Button(self.searchFunction)
        self.searchButton.configure(text='Search')
        self.searchButton.place(anchor='nw', relx='0.42', rely='0.9', x='0', y='0')
        self.searchButton.bind('<1>', self.search, add='')

        #advanced search
        self.advancedSearchLabel = ttk.Label(self.searchFunction)
        self.advancedSearchLabel.configure(anchor='n', background='#6de7a4', font='TkDefaultFont', relief='flat')
        self.advancedSearchLabel.configure(state='normal', text='Advanced Search')
        self.advancedSearchLabel.place(anchor='nw', relx='0.42', rely='0.3', x='0', y='0')

        self.modelLabel = ttk.Label(self.searchFunction)
        self.modelLabel.configure(text='Model')
        self.modelLabel.place(anchor='nw', relx='0.45', rely='0.2', x='0', y='0')

        self.priceLabel = ttk.Label(self.searchFunction)
        self.priceLabel.configure(anchor='n', font='TkDefaultFont', text='Price')
        self.priceLabel.place(anchor='nw', relx='0.46', rely='0.4', x='0', y='0')

        self.colorLabel = ttk.Label(self.searchFunction)
        self.colorLabel.configure(anchor='n', font='TkDefaultFont', text='Color')
        self.colorLabel.place(anchor='nw', relx='0.46', rely='0.5', x='0', y='0')

        self.factoryLabel = ttk.Label(self.searchFunction)
        self.factoryLabel.configure(anchor='n', font='TkDefaultFont', text='Factory')
        self.factoryLabel.place(anchor='nw', relx='0.44', rely='0.6', x='0', y='0')
        
        self.productionYearLabel = ttk.Label(self.searchFunction)
        self.productionYearLabel.configure(anchor='n', font='TkDefaultFont', text='Production Year')
        self.productionYearLabel.place(anchor='nw', relx='0.35', rely='0.7', x='0', y='0')

        self.powerSupplyLabel = ttk.Label(self.searchFunction)
        self.powerSupplyLabel.configure(anchor='n', font='TkDefaultFont', text='Power Supply')
        self.powerSupplyLabel.place(anchor='nw', relx='0.37', rely='0.8', x='0', y='0')
        
        self.priceBox = ttk.Combobox(self.searchFunction,values = ["50", "60",
        "70","100","120","125","200",""])
        self.priceBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.priceBox.place(anchor='nw', relx='0.6', rely='0.4', x='0', y='0')

        self.colorBox = ttk.Combobox(self.searchFunction, values = ["White", "Blue",
        "Yellow", "Green", "Black",""])
        self.colorBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.colorBox.place(anchor='nw', relx='0.6', rely='0.5', x='0', y='0')
   
        self.factoryBox = ttk.Combobox(self.searchFunction, values = ["Malaysia", "China", "Philippines",""])
        self.factoryBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.factoryBox.place(anchor='nw', relx='0.6', rely='0.6', x='0', y='0')

        self.productionYearBox = ttk.Combobox(self.searchFunction, values = ["2014", "2015",
        "2016", "2017", "2018", "2019", "2020",""])
        self.productionYearBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.productionYearBox.place(anchor='nw', relx='0.6', rely='0.7', x='0', y='0')

        self.powerSupplyBox = ttk.Combobox(self.searchFunction, values = ["Battery", "USB",""])
        self.powerSupplyBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.powerSupplyBox.place(anchor='nw', relx='0.6', rely='0.8', x='0', y='0')

        self.homeButton = ttk.Button(self.searchFunction)
        self.homeButton.configure(text='Back to Home Page')
        self.homeButton.place(anchor='nw', x='0', y='0')
        self.homeButton.bind('<1>', self.returnhome, add='')

        

        # Main widget
        self.mainwindow = self.searchFunction
    
    def returnhome(self, event=None):
        pass
    
    #take inputs from comboboxes and bring to searchResults frame
    def search(self, event):
        mongoSearch = ""
        
        category = self.categoryBox.get()
        model = self.modelBox.get()
        price =  self.priceBox.get()
        color = self.colorBox.get()
        factory = self.factoryBox.get()
        productionYear = self.productionYearBox.get()
        powerSupply = self.powerSupplyBox.get()
        
        if category:
            mongoSearch += "'Category': " + "'{}'".format(category) + ", "
        if model:
            mongoSearch += "'Model': " + "'{}'".format(model) + ", "
        if price:
            mongoSearch += "'Color': " + "'{}'".format(price) + ", "
        if color:
            mongoSearch += "'Color': " + "'{}'".format(color) + ", "
        if factory:
            mongoSearch += "'Factory': " + "'{}'".format(factory) + ", "
        if productionYear:
            mongoSearch += "'ProductionYear': " + "'{}'".format(productionYear) + ", "
        if powerSupply:
            mongoSearch += "'PowerSupply': " + "'{}'".format(powerSupply)
        mongoSearch = "{" + mongoSearch + "}"
        print(mongoSearch)
        #connect to mongoDB to search
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client["assignment1"]
        items = db["items"]
        allrecords = items.find(eval(mongoSearch))
        allrecordsList = list(allrecords)
        print(allrecordsList)

        if len(allrecordsList) == 0:
            messagebox.showerror(title="No Available Items", message= "Sorry there are no such items available! Please try another search.")
        else:
            for row in allrecords:
                print(row)


    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = searchFunction()
    app.run()

