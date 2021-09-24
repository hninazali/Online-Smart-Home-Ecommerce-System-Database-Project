# class Database():
#     def __init__(self):
#         self.connection = mysql.connector.connect(host="localhost", port=3306, user="root", passwd="password", database="bt2102db")
#         self.c = self.connection.cursor()

#     #login functions
#     def createCustomer(self, custInfo):
#         addCust = ("INSERT INTO customer "
#                "(customer_id, customer_name, gender, email_address, phone_number, address, password) "
#                "VALUES (%s, %s, %s, %s, %s, %s, %s)")   
#         self.c.execute(addCust, custInfo)
#         self.connection.commit()

#     def createAdmin(self, adminInfo):
#         addAdmin = ("INSERT INTO admin "
#                "(admin_id, admin_name, gender, phone_number, password)"
#                "VALUES (%s, %s, %s, %s, %s)")  
#         self.c.execute(addAdmin, adminInfo)
#         self.connection.commit()

#     def getCustLogin(self, id):
#         getCustLogin = ("SELECT * FROM customer WHERE customer_id = %s")
#         self.c.execute(getCustLogin, (id,))
#         details = self.c.fetchone()
#         return details

#     def getAdminLogin(self, id):
#         getAdminLogin = ("SELECT * FROM admin WHERE admin_id = %s")
#         self.c.execute(getAdminLogin, (id,))
#         details = self.c.fetchone()
#         return details

#     def changePassword(self, newPass, username, isAdmin):
#         if (isAdmin):
#             changeAdminPass = ("UPDATE admin SET password = %s WHERE admin_id = %s")
#             self.c.execute(changeAdminPass, (newPass, username))
#             self.connection.commit()
#         else:
#             changeCustPass = ("UPDATE customer SET password = %s WHERE customer_id = %s")
#             self.c.execute(changeCustPass, (newPass, username))
#             self.connection.commit()

#     def changeNum(self, newNum, username, isAdmin):
#         if (isAdmin):
#             changeAdminNum = ("UPDATE admin SET phone_number = %s WHERE admin_id = %s")
#             self.c.execute(changeAdminNum, (newNum, username))
#             self.connection.commit()
#         else:
#             changeCustNum = ("UPDATE customer SET password = %s WHERE customer_id = %s")
#             self.c.execute(changeCustNum, (newNum, username))
#             self.connection.commit()
    
#     def changeEmail(self, newEmail, username):
#         changeCustEmail = ("UPDATE customer SET email_address = %s WHERE customer_id = %s")
#         self.c.execute(changeCustEmail, (newEmail, username))
#         self.connection.commit()

#     def changeAddress(self, newAddress, username):
#         changeCustAddress = ("UPDATE customer SET address = %s WHERE customer_id = %s")
#         self.c.execute(changeCustAddress, (newAddress, username))
#         self.connection.commit()

#     def beginService(self, serviceReq):
#         beginService = ("UPDATE service SET service_status = %s WHERE request_id = %s")
#         beginRequest = ("UPDATE requests SET request_status = %s WHERE request_id = %s")
#         self.c.execute(beginService, ("In progress", serviceReq[0]))
#         self.c.execute(beginRequest, ("Approved", serviceReq[0]))
#         self.connection.commit()

#     def completeService(self, serviceReq):
#         completeService = ("UPDATE service SET service_status = %s WHERE request_id = %s")
#         completeRequest = ("UPDATE requests set request_status = %s WHERE request_id = %s")
#         self.c.execute(completeService, ("Completed", serviceReq[0]))
#         self.c.execute(completeRequest, ("Completed", serviceReq[0]))
#         self.connection.commit()

#     def retrieveService(self):
#         allReq = ("SELECT requests.request_id, items.item_id, items.category, items.model, requests.request_date, service.service_status FROM ((service INNER JOIN requests ON service.request_id = requests.request_id) INNER JOIN items ON service.item_id = items.item_id)")
#         self.c.execute(allReq, ())
#         results = self.c.fetchall()
#         print(results)
#         return results
import pymysql
def login(email, password):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             database='oshes',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM Customer WHERE email=%s"
        cursor.execute(sql,(email))
        result = cursor.fetchone()
        print(result)
login("aung@test.com", "test")