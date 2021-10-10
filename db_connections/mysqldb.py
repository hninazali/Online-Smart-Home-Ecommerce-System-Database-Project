import tkinter as tk
import tkinter.ttk as ttk
import pymysql
import os

class SQLDatabase():
    def __init__(self):
        try:
            self.connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", database="oshes", autocommit=True)
            self.c = self.connection.cursor()
        except:
            print("Oshes Database does not exist. Creating now")
            tempconnection = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", autocommit=True)
            tempcursor = tempconnection.cursor()
            tempcursor.execute("CREATE DATABASE oshes;")
            tempconnection.commit()

            tempcursor.close()
            tempconnection.close()

            self.connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", database="oshes", autocommit=True)
            self.c = self.connection.cursor()


    # remaining : where to add the create tables codes 

    # TODO: Consider initializing the connection as None and invoke this function to connect
    def connect(self, dbname = "oshes"):
        self.connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", database="oshes", autocommit=True)
        self.c = self.connection.cursor()

    def createDB(self):
        print("createDB: Oshes Database does not exist. Creating now")
        tempconnection = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", autocommit=True)
        tempcursor = tempconnection.cursor()
        tempcursor.execute("CREATE DATABASE oshes;")
        tempconnection.commit()
        tempcursor.close()
        tempconnection.close()

    # Create Customer - DONE
    def createCustomer(self, custInfo):
        addCust = ("INSERT INTO customer "
               "(customerID, name, email, password, address, phoneNumber, gender) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        try:   
            self.c.execute(addCust, custInfo)
            self.connection.commit()
        except Exception as e:
            return e

    # DISABLED
    def createAdmin(self, adminInfo): 
        addAdmin = ("INSERT INTO admin "
               "(adminID, name, password, gender, phoneNumber)"
               "VALUES (%s, %s, %s, %s, %s)")  
        # self.c.execute(addAdmin, adminInfo)
        # self.connection.commit()
        try:   
            self.c.execute(addAdmin, adminInfo)
            self.connection.commit()
        except Exception as e:
            return e

    # get Login
    def getCustomerLogin(self, customerID, password):
        getCustomerLogin = ("SELECT * FROM customer WHERE customerID = %s AND password=%s")
        
        self.c.execute(getCustomerLogin, (customerID,password))
        details = self.c.fetchone()
        if details:
            return details
        else:
            getCustomerLogin = ("SELECT * FROM customer WHERE customerID = %s")
            self.c.execute(getCustomerLogin, (customerID))
            details = self.c.fetchone()

            if details:
                return ("Incorrect Password")
            else:
                return ("User doesn't exist")
        

    def getAdminLogin(self, adminID, password):
        getAdminLogin = ("SELECT * FROM admin WHERE adminID = %s AND password=%s")
        
        self.c.execute(getAdminLogin, (adminID,password))
        details = self.c.fetchone()
        if details:
            return details
        else:
            getAdminLogin = ("SELECT * FROM admin WHERE adminID = %s")
            self.c.execute(getAdminLogin, (adminID))
            details = self.c.fetchone()

            if details:
                return ("Incorrect Password")
            else:
                return ("Admin User doesn't exist")

    # DONE: Changed to send to mysql
    def changePassword(self, newPassword, userID, domain):
        if domain == "Administrator":
            changeAdminPass = ("UPDATE admin SET password = %s WHERE adminID = %s")
            self.c.execute(changeAdminPass, (newPassword, userID))
            self.connection.commit()
        elif domain == "Customer":
            changeCustPass = ("UPDATE customer SET password = %s WHERE customerID = %s")
            self.c.execute(changeCustPass, (newPassword, userID))
            self.connection.commit()
        else:
            raise Exception("Check domain in changePassword")


    # Reset the whole database with the sql scripts in db_scripts/
    def resetMySQLState(self):
        # dropDatabase()
        # self.createDB()
        rootdir = "./db_scripts"
        # Just in case someone cd into this dir and run the script
        # TODO: Specify the order of scripts to be executed
        try:
            files = os.listdir("./db_scripts")
        except:
            files = os.listdir("../db_scripts")
            rootdir = "../db_scripts"
        
        # Drop Tables
        tables = ["items","products","Customer","admin"]
        for table in tables:
            print("executing: Drop table "+table)
            sql = "DROP TABLE IF EXISTS {}"
            self.c.execute(sql.format(table))

        #table.sql creates admin, customer, product and item table while customer and admin sqls create new users
        files = ["table.sql", "customer.sql", "admin.sql"]

        for file in files:
            with open(os.path.join(rootdir, file)) as f:
                allCmd = f.read().split(';')
                allCmd.pop()

                for idx, sql_request in enumerate(allCmd):
                    self.c.execute(sql_request + ';')
                    print("Executing:", sql_request)
        self.connection.commit()

    def loadMongo(self, items, products):
        for product in products:
            print("Executing:", product)
            self.c.execute(product)
            self.connection.commit()

        for item in items:
            print("Executing:", item)
            self.c.execute(item)
            self.connection.commit()



    def getConnection(self):
        return self.connection

# # this methods will be callable without any requirements for the database
# class DBOps():
#     def dropDatabase(self):
#         print("Dropping Databases")
#         try:
#             tempc = pymysql.connect(host="localhost", port=3306, user="root", passwd="password")
#             cur = tempc.cursor()
#             print("check1")
#             cur.execute("CREATE DATABASE oshes;")
#             tempc.commit()

#             tempc.select_db("oshes")

#             cur.execute("DROP DATABASE oshes;")
#             tempc.commit()
#             print("check2")
            
#         except:
#             raise Exception("DB oshes does not exist")


# # Exists outside of the class. Drops the oshes database if it exists
# def dropDatabase():
#     print("Dropping Databases")
#     try:
#         tempc = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", database="oshes")
#         cur = tempc.cursor()
#         # print("check1")
#         cur.execute("DROP DATABASE oshes;")
#         tempc.commit()
#         # print("check2")
        
#     except:
#         print("DB oshes does not exist")


if __name__ == "__main__":
    db = SQLDatabase()
    # db.changePassword('aa', 'bb', "Customer")
    # print(db.getCustomerLogin('aa','aa'))
    db.resetMySQLState()


    # db.resetMySQLState()
    # Testing Functions

    # # Create customer
    # db.createCustomer(["brenda3","Brenda3","brenda3@gmail.com","password","1 Street", "4444", "F"])
    # db.createAdmin(["admin2","Admin2","password", "F", "5555" ])
    
    

    # login
    # email = 'brenda2@gmail.com'
    # print(db.getCustomerLogin(email,"password")) # correct
    # print(db.getCustomerLogin(email,"Aassword")) # incoreect password
    # print(db.getCustomerLogin("a"+email,"password")) # user doesnt exist

    