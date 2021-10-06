import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, LabelFrame
from db_connections.mongodb import MongoDB
from PIL import Image, ImageTk
mongo = MongoDB()
mongo.dropCollection("items")
mongo.dropCollection("products")
mongo.resetMongoState()

LARGEFONT = ("Verdana", 35)

class AdminAdvancedSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.wrapper1 = LabelFrame(self, text="Header")
        self.wrapper2 = LabelFrame(self, text="Products List")

        self.wrapper1.pack(fill=tk.X)
        self.wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)

        label = ttk.Label(self.wrapper1, text="Products List", font=LARGEFONT)
        label.grid(row=0, column=1, padx=10, pady=10)

        self.priceBox = ttk.Combobox(self.wrapper1 ,values = ["50", "60",
        "70","100","120","125","200",""])
        self.priceBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.priceBox.grid(column='1', padx='5', pady='5', row='2')
        
        self.colorBox = ttk.Combobox(self.wrapper1, values = ["White", "Blue",
        "Yellow", "Green", "Black",""])
        self.colorBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.colorBox.grid(column='1', padx='5', pady='5', row='3')

        self.factoryBox = ttk.Combobox(self.wrapper1, values = ["Malaysia", "China", "Philippines",""])
        self.factoryBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.factoryBox.grid(column='1', padx='5', pady='5', row='4')

        self.productionYearBox = ttk.Combobox(self.wrapper1, values = ["2014", "2015",
        "2016", "2017", "2018", "2019", "2020",""])
        self.productionYearBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.productionYearBox.grid(column='1', padx='5', pady='5', row='5')

        self.powerSupplyBox = ttk.Combobox(self.wrapper1, values = ["Battery", "USB",""])
        self.powerSupplyBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.powerSupplyBox.grid(column='1', padx='5', pady='5', row='6')

        self.advancedSearchButton = ttk.Button(self.wrapper1, text="Filter", command=self.search)
        self.advancedSearchButton.grid(column='2', padx='5', pady='5', row='6')

        self.priceLabel = ttk.Label(self.wrapper1)
        self.priceLabel.configure(text='Price')
        self.priceLabel.grid(column='0', padx='5', pady='5', row='2')

        self.colorLabel = ttk.Label(self.wrapper1)
        self.colorLabel.configure(text='Color')
        self.colorLabel.grid(column='0', padx='5', pady='5', row='3')

        self.factoryLabel = ttk.Label(self.wrapper1)
        self.factoryLabel.configure(text='Factory')
        self.factoryLabel.grid(column='0', padx='5', pady='5', row='4')

        self.productionYearLabel = ttk.Label(self.wrapper1)
        self.productionYearLabel.configure(text='Production Year')
        self.productionYearLabel.grid(column='0', padx='5', pady='5', row='5')

        self.powerSupplyLabel = ttk.Label(self.wrapper1)
        self.powerSupplyLabel.configure(text='Power Supply')
        self.powerSupplyLabel.grid(column='0', padx='5', pady='5', row='6')
        
        self.treeFrame= ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='300')

        cols = ("Item ID", "Category", "Model", "Price", "Cost", "Color", "Factory", "Warranty", "Production Year", "Power Supply", "Purchase Status", "Service Status")
        scroll_y = ttk.Scrollbar(self.treeFrame, orient = "vertical")
        scroll_x = ttk.Scrollbar(self.treeFrame, orient = "horizontal")
        self.itemTree = ttk.Treeview(self.treeFrame, columns = cols,show='headings',
        yscrollcommand = scroll_y.set, xscrollcommand = scroll_x.set)
        scrollbar = ttk.Scrollbar(self.wrapper2, orient="vertical", command=self.itemTree.yview)
        self.itemTree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=2, sticky="ns")

        for col in cols:
            self.itemTree.column(col, anchor="center", width=150)
            self.itemTree.heading(col, text=col)

        res = mongo.adminAdvancedSearch(self.mongoSearch())
        for r in  res:
            result = self.mongoToTree(r)
            self.itemTree.insert("", "end", values=result)
        self.itemTree.grid(row=6, column=1, columnspan=2)
    
    def search(self):
        for r in self.itemTree.get_children():
            self.itemTree.delete(r)

        res = mongo.adminAdvancedSearch(self.mongoSearch())
        for r in res:
            result = self.mongoToTree(r)
            self.itemTree.insert("", "end", values=result)

        self.itemTree.grid(row=6, column=1, columnspan=1)

    def mongoSearch(self):
        mongoSearch = ""

        price =  self.priceBox.get()
        color = self.colorBox.get()
        factory = self.factoryBox.get()
        productionYear = self.productionYearBox.get()
        powerSupply = self.powerSupplyBox.get()
        listSearch = []

        # if price:
        #     mongoSearch += "'Price': " + "'{}'".format(price) + ", "
        if color:
            listSearch.append('"Color": '+ '"{}"'.format(color))
        if factory:
            listSearch.append('"Factory": ' + '"{}"'.format(factory))
        if productionYear:
            listSearch.append('"ProductionYear": ' + '"{}"'.format(productionYear))
        if powerSupply:
            listSearch.append('"PowerSupply": ' + '"{}"'.format(powerSupply))
        print(listSearch)
        if not listSearch:
            return ""
        elif len(listSearch) == 1:
            return "{" + listSearch[0]+ "}"
        else:
            for s in listSearch[:-1]:
                mongoSearch = "{" + s + "}, "
            mongoSearch += "{" + str(listSearch[:-1]) + "}"
        return mongoSearch

    def mongoToTree(self, r):
        price = cost = warranty = 0
        re = (r["ItemID"], r["Category"], r["Model"], price, cost, r["Color"], r["Factory"], warranty, r["ProductionYear"], r["PowerSupply"], r["PurchaseStatus"], r["ServiceStatus"])
        return re