from pymongo import MongoClient, errors
import os
import json

class MongoDB():
    def __init__(self):
        try:
            # try to instantiate a client instance
            self.client = MongoClient("mongodb+srv://user:oshespassword@singapore.gznlc.mongodb.net/test")
            # print the version of MongoDB server if connection successful
            print ("server version:", self.client.server_info()["version"])

        except errors.ServerSelectionTimeoutError as err:
            print(err)

    # Returns true if the collection was dropped successfully, for data reinit function
    def dropCollection(self, collection_name, database_name="oshes"):
        return self.client[database_name][collection_name].drop()

    def resetMongoState(self, database_name="oshes"):
        # if called from db_connections and if called from tk-screens 
        try:
            files = os.listdir("./JSON_files")
            rootdir = "./JSON_files"
        except:
            files = os.listdir("../JSON_files")
            rootdir = "../JSON_files"

        # Define the order of json files to load
        files = ["items.json", "products.json"]

        # For each element in the array, insert into the collection (table) inside the database
        for file in files:
            fullpath = os.path.join(rootdir, file)
            collectionName = file.split('.')[0] # splits the file string name to get the collectionName
            with open(fullpath, 'r') as jsonfile:
                jsonstr = json.load(jsonfile)
                print(jsonstr)
                self.client[database_name][collectionName].insert_many(jsonstr)


    # TODO: ask prof 
    def findItems(self, category, model, database_name="oshes", domain="Customer"): #mode=[Administrator/Customer]
        if domain == "Customer":
            # tempdict = {"ItemID":1, "Category":1, "Color":1, "Factory":1, "PowerSupply":1, "PurchaseStatus":0, "ProductionYear":1, "Model":1, "ServiceStatus":0}
            tempdict = {"PurchaseStatus":0, "ServiceStatus":0}
            cursor = self.client[database_name]["items"].find({"Category": category, "Model": model}, tempdict)
            return list(cursor)
        elif domain == "Administrator":
            cursor = self.client[database_name]["items"].find({"Category": category, "Model": model})
            return list(cursor)

    def findProducts(self, category, model, database_name="oshes", domain="Customer"): #mode=[Administrator/Customer]
        if domain == "Customer":
            # tempdict = {"ItemID":1, "Category":1, "Color":1, "Factory":1, "PowerSupply":1, "PurchaseStatus":0, "ProductionYear":1, "Model":1, "ServiceStatus":0}
            tempdict = {"Cost ($)":0}
            cursor = self.client[database_name]["products"].find({"Category": category, "Model": model}, tempdict)
            return list(cursor)
        elif domain == "Administrator":
            cursor = self.client[database_name]["products"].find({"Category": category, "Model": model})
            return list(cursor)


    # Returns instance of DeleteResult. Execute query.deleted_count for the number of deleted documents
    # TODO: test
    def purchase(self, ItemID, database_name="oshes"):
        query = self.client[database_name]["items"].delete_one({"ItemID": ItemID})
        return query
    
    # The input for now is a dictionary (item)
    def insertItem(self, itemdict, database_name='oshes'):
        query = self.client[database_name]["items"].insert_one(itemdict)

    def getClient(self):
        return self.client

    
    def convertMongotoSQL(self):
        itemsSQL = []  # Array of SQL Commands to load items
        productsSQL = []  # Array of SQL commands to load products
        # items = open("../JSON_files/items.json")
        # arr = json.load(items)

        arr=list(self.client['oshes']['items'].find({}))

        for item in arr:
            if item["ServiceStatus"] == '':
                item["ServiceStatus"] = 'Completed'  # Change this later
            string = "INSERT INTO items VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\");".format(
                item["ItemID"], item["Category"], item["Color"], item["Factory"], item["PowerSupply"], item["PurchaseStatus"], item["ProductionYear"], item["Model"], item["ServiceStatus"])
            itemsSQL.append(string)

        # items.close()

        # products = open("../JSON_files/products.json")
        # arr2 = json.load(products)
        arr2=list(self.client['oshes']['products'].find({}))

        for product in arr2:
            string = "INSERT INTO products VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\");".format(
                product["Category"], product["Cost ($)"], product["Model"], product["Price ($)"], product["ProductID"], product["Warranty (months)"],)
            productsSQL.append(string)

        # products.close()

        # with open("../db_scripts/items.sql", 'w+') as f:
        #     for item in itemsSQL:
        #         f.write(item+"\n")

        # with open("../db_scripts/products.sql", 'w+') as f:
        #     for product in productsSQL:
        #         f.write(product+"\n")

        return itemsSQL, productsSQL

if __name__ == "__main__":
    db = MongoDB()
    obj1, obj2 = db.convertMongotoSQL()
    # db.dropCollection("products")
    # db.dropCollection("items")
    # db.resetMongoState()
    # print(db.findItems(category="Lights", model="Light1", domain="Administrator"))
    # print(db.findProducts(category="Lights", model="Light1", domain="Customer"))
    