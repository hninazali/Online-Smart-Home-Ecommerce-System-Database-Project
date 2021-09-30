import tkinter as tk
import tkinter.ttk as ttk
import pymysql
import os

class SQLDatabase():
    def __init__(self):
        self.connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", database="oshes")
        self.c = self.connection.cursor()

    # remaining : where to add the create tables codes 


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
               "(adminID, password, name, gender, phoneNumber)"
               "VALUES (%s, %s, %s, %s, %s)")  
        self.c.execute(addAdmin, adminInfo)
        self.connection.commit()

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


    def changePassword(self, newPass, username, isAdmin):
        if (isAdmin):
            changeAdminPass = ("UPDATE admin SET password = %s WHERE admin_id = %s")
            self.c.execute(changeAdminPass, (newPass, username))
            self.connection.commit()
        else:
            changeCustPass = ("UPDATE customer SET password = %s WHERE customer_id = %s")
            self.c.execute(changeCustPass, (newPass, username))
            self.connection.commit()

    def changeNum(self, newNum, username, isAdmin):
        if (isAdmin):
            changeAdminNum = ("UPDATE admin SET phone_number = %s WHERE admin_id = %s")
            self.c.execute(changeAdminNum, (newNum, username))
            self.connection.commit()
        else:
            changeCustNum = ("UPDATE customer SET password = %s WHERE customer_id = %s")
            self.c.execute(changeCustNum, (newNum, username))
            self.connection.commit()
    
    def changeEmail(self, newEmail, username):
        changeCustEmail = ("UPDATE customer SET email_address = %s WHERE customer_id = %s")
        self.c.execute(changeCustEmail, (newEmail, username))
        self.connection.commit()

    def changeAddress(self, newAddress, username):
        changeCustAddress = ("UPDATE customer SET address = %s WHERE customer_id = %s")
        self.c.execute(changeCustAddress, (newAddress, username))
        self.connection.commit()

    def beginService(self, serviceReq):
        beginService = ("UPDATE service SET service_status = %s WHERE request_id = %s")
        beginRequest = ("UPDATE requests SET request_status = %s WHERE request_id = %s")
        self.c.execute(beginService, ("In progress", serviceReq[0]))
        self.c.execute(beginRequest, ("Approved", serviceReq[0]))
        self.connection.commit()

    def completeService(self, serviceReq):
        completeService = ("UPDATE service SET service_status = %s WHERE request_id = %s")
        completeRequest = ("UPDATE requests set request_status = %s WHERE request_id = %s")
        self.c.execute(completeService, ("Completed", serviceReq[0]))
        self.c.execute(completeRequest, ("Completed", serviceReq[0]))
        self.connection.commit()

    def retrieveService(self):
        allReq = ("SELECT requests.request_id, items.item_id, items.category, items.model, requests.request_date, service.service_status FROM ((service INNER JOIN requests ON service.request_id = requests.request_id) INNER JOIN items ON service.item_id = items.item_id)")
        self.c.execute(allReq, ())
        results = self.c.fetchall()
        print(results)
        return results

    # Reset the whole database with the sql scripts in db_scripts/
    def resetMySQLState(self):
        rootdir = "./db_scripts"
        # Just in case someone cd into this dir and run the script
        # TODO: Specify the order of scripts to be executed
        try:
            files = os.listdir("./db_scripts")
        except:
            files = os.listdir("../db_scripts")
            rootdir = "../db_scripts"

        files = ["table.sql", "customer.sql", "admin.sql"]

        for file in files:
            with open(os.path.join(rootdir, file)) as f:
                allCmd = f.read().split(';')
                allCmd.pop()

                for idx, sql_request in enumerate(allCmd):
                    self.c.execute(sql_request + ';')

if __name__ == "__main__":
    db = SQLDatabase()
    db.resetMySQLState()
    # Testing Functions

    # Create customer
    # db.createCustomer(["brenda3","Brenda3","brenda3@gmail.com","password","1 Street", "4444", "F"])
    # db.createAdmin(["admin2","Admin2", "F", "5555", "password"])
    

    # login
    # email = 'brenda2@gmail.com'
    # print(db.getCustomerLogin(email,"password")) # correct
    # print(db.getCustomerLogin(email,"Aassword")) # incoreect password
    # print(db.getCustomerLogin("a"+email,"password")) # user doesnt exist

    