import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from tkinter import *
import pymongo

class searchFunction:
    def __init__(self):
        self.searchFunction = tk.Tk()
        self.searchFunction.geometry('1200x600')
        self.searchFunction.grid_propagate(0)
        #self.searchFunction.resizable(False, False)


        ####Buttons####
        self.homeButton = ttk.Button(self.searchFunction)
        self.homeButton.configure(text='Home')
        self.homeButton.grid(column='1', padx='3', pady='3', row='1')

        self.searchButton = ttk.Button(self.searchFunction)
        self.searchButton.configure(text='Search')
        self.searchButton.grid(column='7', padx='5', pady='5', row='9')
        self.searchButton.bind('<1>', self.search, add='')

        self.buyButton = ttk.Button(self.searchFunction)
        self.buyButton.configure(text='Buy')
        self.buyButton.grid(column='7', pady='20', row='11', sticky='e')
        

        ####Comboboxes####
        vModel=[]
        self.modelBox = ttk.Combobox(self.searchFunction, values = vModel)
        self.modelBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.modelBox.grid(column='4', padx='5', pady='5', row='3')

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
        self.categoryBox.configure(state='readonly')
        self.categoryBox.grid(column='4', padx='5', pady='5', row='2')
        
        self.priceBox = ttk.Combobox(self.searchFunction,values = ["50", "60",
        "70","100","120","125","200",""])
        self.priceBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.priceBox.grid(column='7', padx='5', pady='5', row='2')
        
        self.colorBox = ttk.Combobox(self.searchFunction, values = ["White", "Blue",
        "Yellow", "Green", "Black",""])
        self.colorBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.colorBox.grid(column='7', padx='5', pady='5', row='3')

        self.factoryBox = ttk.Combobox(self.searchFunction, values = ["Malaysia", "China", "Philippines",""])
        self.factoryBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.factoryBox.grid(column='7', padx='5', pady='5', row='4')

        self.productionYearBox = ttk.Combobox(self.searchFunction, values = ["2014", "2015",
        "2016", "2017", "2018", "2019", "2020",""])
        self.productionYearBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.productionYearBox.grid(column='7', padx='5', pady='5', row='5')

        self.powerSupplyBox = ttk.Combobox(self.searchFunction, values = ["Battery", "USB",""])
        self.powerSupplyBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.powerSupplyBox.grid(column='7', padx='5', pady='5', row='6')

        ####Labels####
        self.simpleSearchLabel = ttk.Label(self.searchFunction)
        self.simpleSearchLabel.configure(background='#a6f991', text='Simple Search')
        self.simpleSearchLabel.grid(column='2', padx='5', pady='5', row='2')

        self.advancedSearchLabel = ttk.Label(self.searchFunction)
        self.advancedSearchLabel.configure(background='#b19bee', text='Advanced Search')
        self.advancedSearchLabel.grid(column='5', padx='5', pady='5', row='2')

        self.priceLabel = ttk.Label(self.searchFunction)
        self.priceLabel.configure(text='Price')
        self.priceLabel.grid(column='6', padx='5', pady='5', row='2')

        self.colorLabel = ttk.Label(self.searchFunction)
        self.colorLabel.configure(text='Color')
        self.colorLabel.grid(column='6', padx='5', pady='5', row='3')

        self.factoryLabel = ttk.Label(self.searchFunction)
        self.factoryLabel.configure(text='Factory')
        self.factoryLabel.grid(column='6', padx='5', pady='5', row='4')

        self.productionYearLabel = ttk.Label(self.searchFunction)
        self.productionYearLabel.configure(text='Production Year')
        self.productionYearLabel.grid(column='6', padx='5', pady='5', row='5')

        self.powerSupplyLabel = ttk.Label(self.searchFunction)
        self.powerSupplyLabel.configure(text='Power Supply')
        self.powerSupplyLabel.grid(column='6', padx='5', pady='5', row='6')

        self.categoryLabel = ttk.Label(self.searchFunction)
        self.categoryLabel.configure(text='Category')
        self.categoryLabel.grid(column='3', padx='5', pady='5', row='2')

        self.modelLabel = ttk.Label(self.searchFunction)
        self.modelLabel.configure(text='Model')
        self.modelLabel.grid(column='3', padx='5', pady='5', row='3')
        
        ####Item display####
        self.treeFrame= ttk.Frame(self.searchFunction)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='300')
        self.treeFrame.grid(column='2', columnspan='6', row='10', rowspan='1')

        cols = ("Category","Model", "Price", "Color","Factory", "Production Year", "Power Supply")
        scroll_y = Scrollbar(self.treeFrame, orient = VERTICAL)
        scroll_x = Scrollbar(self.treeFrame, orient = HORIZONTAL)
        self.itemTree = ttk.Treeview(self.treeFrame, columns = cols,show='headings',
        yscrollcommand = scroll_y.set, xscrollcommand = scroll_x.set)
        scroll_y.pack(side = RIGHT, fill = Y)
        scroll_x.pack(side = BOTTOM, fill = X)
        self.itemTree.pack(expand='false', fill='both', side='top')

        for col in cols:
            self.itemTree.column(col, anchor="center", width=150)
            self.itemTree.heading(col, text=col)


        self.availItems = ttk.Label(self.searchFunction)
        self.availItems.configure(text='Number of items available:')
        self.availItems.grid(column='2', columnspan='2', row='9')
        
        
        # Main widget
        self.mainwindow = self.searchFunction
    

    def run(self):
        self.mainwindow.mainloop()

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

        #uncomment printstatement to show output in terminal
        print(mongoSearch)

        #connect to mongoDB to search
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client["assignment1"]
        items = db["items"]
        allrecords = items.find(eval(mongoSearch))

        #uncomment to print records in terminal
        allrecordsList = list(allrecords)
        print(allrecordsList)

        if len(allrecordsList) == 0:
            messagebox.showerror(title="No Available Items", message= "Sorry there are no such items available! Please try another search.")
        else:
            for record in allrecords:
                result = self.mongoToTree(record)
                self.itemTree.insert("", "end", values=result)


    def mongoToTree(self, r):
        #need to figure a way to get price from products collection
        price =  "N/A"
        re = (r["ItemID"], r["Model"], r["Category"], r["Color"], r["Factory"], r["PowerSupply"], r["ProductionYear"], r["PurchaseStatus"], price)
        return re




if __name__ == '__main__':
    app = searchFunction()
    app.run()