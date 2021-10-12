from pymongo import MongoClient, errors
import os
import json


class MongoDB():
    def __init__(self):
        try:
            # try to instantiate a client instance
            self.client = MongoClient("mongodb://localhost:27017")
            # print the version of MongoDB server if connection successful
            # print ("server version:", self.client.server_info()["version"])

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

    def findItemByID(self, itemID, database_name="oshes"):
        cursor = self.client[database_name]["items"].find({"ItemID": itemID})
        return list(cursor)

    def adminProductSearch(self, category, model, database_name="oshes"):
        if category == "" and model == "":
            cursor = self.client[database_name]["products"].find()
        elif category == "":
            cursor = self.client[database_name]["products"].find({"Model": model})
        elif model == "":
            cursor = self.client[database_name]["products"].find({"Category": category})
        else:
            cursor = self.client[database_name]["products"].find({"Category": category, "Model": model})
        return list(cursor)
    
    def soldLevel(self, database_name="oshes"):
        cursor = self.client[database_name]["products"].aggregate([{ "$lookup": { "from": "items", "localField": "Model", "foreignField": "Model", "as": "relation"}},
        { "$project": {
                "ProductID": 1,
                "relation": {
                    "$filter": {
                        "input": "$relation",
                        "as": "r",
                        "cond": { 
                            "$eq": [ "$$r.PurchaseStatus", "Sold" ] 
                            }
                    }
                }
            }
        } ,
        { "$group": { "_id": "$ProductID", "total": { "$sum": { "$size":"$relation" } }}},
        { "$sort": { "_id" : 1 } }])
        return list(cursor)
    
    def unsoldLevel(self, database_name="oshes"):
        cursor = self.client[database_name]["products"].aggregate([{ "$lookup": { "from": "items", "localField": "Model", "foreignField": "Model", "as": "relation"}},
        { "$project": {
                "ProductID": 1,
                "relation": {
                    "$filter": {
                        "input": "$relation",
                        "as": "r",
                        "cond": { 
                            "$eq": [ "$$r.PurchaseStatus", "Unsold" ] 
                            }
                    }
                }
            }
        } ,
        { "$group": { "_id": "$ProductID", "total": { "$sum": { "$size":"$relation" } }}},
        { "$sort": { "_id" : 1 } }])
        return list(cursor)

    def adminAdvancedSearch(self, search, database_name="oshes"):
        if search == "" or search == "{}":
            cursor = self.client[database_name]["items"].find()
        else:
            cursor = self.client[database_name]["items"].find(search)
        return list(cursor)

    def findModelfromPrice(self, price, database_name="oshes"):
        cursor = self.client[database_name]["products"].find({"Price ($)": int(price)})
        product = list(cursor)
        result =  {}
        result["Category"] = product[0]['Category']
        result["Model"] = product[0]['Model']
        return result

    def findPriceCostWarranty(self, category, model, database_name="oshes"):
        product = self.client[database_name]["products"].find({'Category': category, 'Model': model})[0]
        result = {}
        result["Price"] = product['Price ($)']
        result["Cost"] = product['Cost ($)']
        result["Warranty"] = product['Warranty (months)']
        return (result)
    # Find the product that matches the item's attributes. Return the ID
    def getProductID(self, itemdict):
        # ItemDict should contain the model and category (common columns between items and products collections)
        cursor = self.client['oshes']["products"].find(itemdict, {"ProductID": 1})
        li = list(cursor)
        # print("Serached for:",itemdict, "Found products:", li)
        # print("Found Product:", li[0]["ProductID"])
        return li[0]["ProductID"]


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
        itemsSQL = []  # Array of SQL Values as a tuple to load items
        productsSQL = []  # Array of SQL Values as a tuple to load products

        arr2=list(self.client['oshes']['products'].find({}))

        # for product in arr2:
        #     string = "INSERT INTO products VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\");".format(
        #          product["ProductID"], product["Model"], product["Category"], product["Warranty (months)"], product["Cost ($)"], product["Price ($)"])
        #     productsSQL.append(string)

        for product in arr2:
            string = (product["ProductID"], product["Model"], product["Category"], product["Warranty (months)"], product["Cost ($)"], product["Price ($)"])
            productsSQL.append(string)


        # arr=list(self.client['oshes']['items'].find({}))

        # for item in arr:
        #     customerID = "customer1" # Change this later
        #     productID = int(self.getProductID({
        #         "Category": item["Category"],
        #         "Model": item["Model"]
        #     })) # Change this later
        #     print("Found Product:", productID)
            
        #     if item["ServiceStatus"] == '':
        #         item["ServiceStatus"] = 'Completed'  # Change this later
        #     string = "INSERT INTO items VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\");".format(
        #         item["ItemID"], item["Color"], item["Factory"], item["PowerSupply"], item["PurchaseStatus"], item["ProductionYear"], customerID, productID, None)
        #     itemsSQL.append(string)

        arr=list(self.client['oshes']['items'].find({}))

        for item in arr:
            productID = int(self.getProductID({
                "Category": item["Category"],
                "Model": item["Model"]
            })) # Change this later
            print("Found Product:", productID)
            
            if item["ServiceStatus"] == '':
                item["ServiceStatus"] = 'Completed'  # Change this later
            string = (item["ItemID"], item["Color"], item["Factory"], item["PowerSupply"], item["PurchaseStatus"], item["ProductionYear"], None, productID, None)
            itemsSQL.append(string)

        return itemsSQL, productsSQL

if __name__ == "__main__":
    from mysqldb import SQLDatabase
    db = MongoDB()
    items, products = db.convertMongotoSQL()

    db = SQLDatabase()
    db.resetMySQLState()

    db.loadMongo(items, products)
    # db.dropCollection("products")
    # db.dropCollection("items")
    # print(db.adminAdvancedSearch({"Color": "Blue"}))
    # print(db.findProducts(category="Lights", model="Light1", domain="Customer"))