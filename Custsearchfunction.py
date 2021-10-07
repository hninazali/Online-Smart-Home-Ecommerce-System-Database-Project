import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from tkinter import *
import pymongo
import pymysql
from datetime import date

#connect to mongoDB to search
global client
client = pymongo.MongoClient("mongodb://localhost:27017")
global db
db = client["assignment1"]

#connect to mysql database to register purchases
global con
con = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", database="oshes")


class searchFunction:
    def __init__(self):
        self.searchFunction = tk.Tk()
        self.searchFunction.geometry('1050x600')
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
        self.buyButton.bind('<Button-1>', self.buyItem)

        

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

        cols = ("itemID","Category","Model", "Price", "Color","Factory", "Production Year", "Power Supply")
        scroll_y = Scrollbar(self.treeFrame, orient = VERTICAL)
        self.itemTree = ttk.Treeview(self.treeFrame, columns = cols,show='headings',
        yscrollcommand = scroll_y.set)
        scroll_y.pack(side = RIGHT, fill = Y)
        self.itemTree.pack(expand='false', fill='both', side='top')
        
        for col in cols:
            self.itemTree.column(col, anchor="center", width=110)
            self.itemTree.heading(col, text=col)



        self.availItems = ttk.Label(self.searchFunction)
        self.availItems.configure(text='Number of items available:')
        self.availItems.grid(column='2', columnspan='2', row='9')
        
        
        # Main widget
        self.mainwindow = self.searchFunction
    

    

     #take inputs from comboboxes and bring to searchResults frame
    def search(self, event):
        self.itemTree.delete(*self.itemTree.get_children())
        mongoSearch = ""
        
        category = self.categoryBox.get()
        model = self.modelBox.get()
        price =  self.priceBox.get()
        color = self.colorBox.get()
        factory = self.factoryBox.get()
        productionYear = self.productionYearBox.get()
        powerSupply = self.powerSupplyBox.get()
        print(price)

        ##special handeling for price
        if price:
            catandmod = self.findCatNModfromPrice(price)
            if category and category != catandmod[0]:
                category = "no output"
            if model and model != catandmod[1]:
                model = "no output"
            else:
                category = catandmod[0]
                model = catandmod[1]       

        if category:
            mongoSearch += "'Category': " + "'{}'".format(category) + ", "
        if model:
            mongoSearch += "'Model': " + "'{}'".format(model) + ", "
        if color:
            mongoSearch += "'Color': " + "'{}'".format(color) + ", "
        if factory:
            mongoSearch += "'Factory': " + "'{}'".format(factory) + ", "
        if productionYear:
            mongoSearch += "'ProductionYear': " + "'{}'".format(productionYear) + ", "
        if powerSupply:
            mongoSearch += "'PowerSupply': " + "'{}'".format(powerSupply)
        
        mongoSearch = "{" + mongoSearch + "'PurchaseStatus': 'Unsold'" + "}"

        #uncomment print statement to show output in terminal
        #print(mongoSearch)

        items = db["items"]
        allrecords = items.find(eval(mongoSearch))
        allrecordsList = list(allrecords)
        #uncomment to print records in terminal
        #print(allrecordsList)

        if len(allrecordsList) == 0:
            messagebox.showerror(title="No Available Items", message= "Sorry there are no such items available! Please try another search.")
        else:
            for record in allrecordsList:
                result = self.mongoToTree(record)
                self.itemTree.insert("", "end", values=result)
    
    def findCatNModfromPrice(self, price):
        products = db["products"]
        product = products.find({'Price ($)': price})[0]
        category = product['Category']
        model = product['Model']
        return(category, model)

    def findPrice(self, category, model):
        products = db["products"]
        product = products.find({'Category': category, 'Model': model})[0]
        price = product['Price ($)']
        return (price)

    def buyItem(self, a):
        curItem = self.itemTree.focus()
        extractID = self.itemTree.item(curItem)['values'][0]


        #update mysql database, need to get current customer id
        updateStatement = "UPDATE Item SET PurchaseStatus = 'Sold',dateOfPurchase = %s, customerID = %s  WHERE ItemID = %s"
        val = (date.today().isoformat(),"001", extractID)
        con.ping()  # reconnecting mysql
        with con.cursor() as cursor:         
            cursor.execute(updateStatement , val)
        con.commit()
        con.close()


        #delete item and show purchase success
        self.itemTree.delete(self.itemTree.focus())
        messagebox.showinfo(title="Purchase Successful", message= "Thank you for your purchase!")
        

    def mongoToTree(self, r):
        price = self.findPrice(r["Category"], r["Model"])
        re = (r["ItemID"], r["Category"], r["Model"], price, r["Color"], r["Factory"], r["ProductionYear"], r["PowerSupply"])
        return re

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = searchFunction()
    app.run()