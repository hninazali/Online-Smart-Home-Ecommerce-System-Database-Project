import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from db_connections.mongodb import MongoDB
from PIL import Image, ImageTk
# from tk_screens.adminPortal import AdminPortal

mongo = MongoDB()
mongo.dropCollection("items")
mongo.dropCollection("products")
mongo.resetMongoState()

LARGEFONT = ("Calibri", 35, "bold")

class AdminAdvancedSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Products List", font=LARGEFONT)
        label.grid(row=0, column=3, padx=10, pady=10)

        self['background']='#F6F4F1'

        # button1 = ttk.Button(self, text="Back to Admin Home",
        #                      command=lambda: controller.show_frame(AdminPortal))
        # button1.grid(row=1, column=3, padx=5, pady=5)

        self.priceBox = ttk.Combobox(self ,values = ["50", "60",
        "70","100","120","125","200",""])
        self.priceBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.priceBox.grid(column='2', padx='5', pady='5', row='2')
        
        self.colorBox = ttk.Combobox(self, values = ["White", "Blue",
        "Yellow", "Green", "Black",""])
        self.colorBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.colorBox.grid(column='2', padx='5', pady='5', row='3')

        self.factoryBox = ttk.Combobox(self, values = ["Malaysia", "China", "Philippines",""])
        self.factoryBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.factoryBox.grid(column='2', padx='5', pady='5', row='4')

        self.productionYearBox = ttk.Combobox(self, values = ["2014", "2015",
        "2016", "2017", "2018", "2019", "2020",""])
        self.productionYearBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.productionYearBox.grid(column='2', padx='5', pady='5', row='5')

        self.powerSupplyBox = ttk.Combobox(self, values = ["Battery", "USB",""])
        self.powerSupplyBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.powerSupplyBox.grid(column='2', padx='5', pady='5', row='6')

        self.advancedSearchButton = ttk.Button(self, text="Filter", command=self.search)
        self.advancedSearchButton.grid(column='3', padx='5', pady='5', row='6')

        self.priceLabel = ttk.Label(self)
        self.priceLabel.configure(text='Price')
        self.priceLabel.grid(column='1', padx='5', pady='5', row='2')

        self.colorLabel = ttk.Label(self)
        self.colorLabel.configure(text='Color')
        self.colorLabel.grid(column='1', padx='5', pady='5', row='3')

        self.factoryLabel = ttk.Label(self)
        self.factoryLabel.configure(text='Factory')
        self.factoryLabel.grid(column='1', padx='5', pady='5', row='4')

        self.productionYearLabel = ttk.Label(self)
        self.productionYearLabel.configure(text='Production Year')
        self.productionYearLabel.grid(column='1', padx='5', pady='5', row='5')

        self.powerSupplyLabel = ttk.Label(self)
        self.powerSupplyLabel.configure(text='Power Supply')
        self.powerSupplyLabel.grid(column='1', padx='5', pady='5', row='6')

        self.treeFrame= ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='300')
        self.treeFrame.grid(column='2', columnspan='6', row='7', rowspan='1')

        self.cols = ("Item ID", "Category", "Model", "Price", "Cost", "Color", "Factory", "Warranty", "Production Year", "Power Supply", "Purchase Status", "Service Status")

        self.tree = ttk.Treeview(self.treeFrame, columns = self.cols,show='headings')
        self.tree.pack(side='left')
        scroll_y = Scrollbar(self.treeFrame, orient = 'vertical', command = self.tree.yview)
        scroll_y.pack(side = RIGHT, fill = Y)
        self.tree.configure(yscrollcommand = scroll_y.set)
        
        for col in self.cols:
            self.tree.column(col, anchor="center", width=100)
            self.tree.heading(col, text=col)

        res = mongo.adminAdvancedSearch(self.mongoSearch())
        for r in  res:
            result = self.mongoToTree(r)
            self.tree.insert("", "end", values=result)
    
    def search(self):
        for r in self.tree.get_children():
            self.tree.delete(r)

        for col in self.cols:
            self.tree.heading(col, text=col)

        stringsearch = self.mongoSearch()
        allrecordsList = mongo.adminAdvancedSearch(stringsearch)
        messagebox.showinfo(title="Search Results", message= "{} items available based on your search!".format(len(allrecordsList)))

        if len(allrecordsList) == 0:
            pass
        else:
            for record in allrecordsList:
                result = self.mongoToTree(record)
                self.tree.insert("", "end", values=result)

    def mongoSearch(self):
        mongoSearch = ""

        price =  self.priceBox.get()
        color = self.colorBox.get()
        factory = self.factoryBox.get()
        productionYear = self.productionYearBox.get()
        powerSupply = self.powerSupplyBox.get()
        category = ""
        model = ""

        if price:
            catandmod = self.findModelfromPrice(price)
            if category and category != catandmod[0]:
                category = "no output"
            if model and model != catandmod[1]:
                model = "no output"
            else:
                category = catandmod[0]
                model = catandmod[1]   
        dictSearch = {}   

        if category:
             dictSearch["Category"] = category
        if model:
            dictSearch["Model"] = model
        if color:
             dictSearch["Color"] = color
        if factory:
            dictSearch["Factory"] = factory
        if productionYear:
            dictSearch["ProductionYear"] = productionYear
        if powerSupply:
            dictSearch["PowerSupply"] = powerSupply
        return dictSearch

    def findModelfromPrice(self, price):
        product = mongo.findModelfromPrice(price)
        Category = product["Category"]
        Model = product["Model"]
        return (Category, Model)

    def mongoToTree(self, r):
        # To get price, cost, warranty from product (not avail in item)
        pcw = mongo.findPriceCostWarranty(r["Category"], r["Model"])
        re = (r["ItemID"], r["Category"], r["Model"], pcw["Price"], pcw["Cost"], r["Color"], r["Factory"], pcw["Warranty"], r["ProductionYear"], r["PowerSupply"], r["PurchaseStatus"], r["ServiceStatus"])
        return re