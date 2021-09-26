# import pymysql
# def login(email, password):
#     connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='password',
#                              database='oshes',
#                              cursorclass=pymysql.cursors.DictCursor)

#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT * FROM Customer WHERE email=%s"
#         cursor.execute(sql,(email))
#         result = cursor.fetchone()
#         print(result)
# login("aung@test.com", "test")