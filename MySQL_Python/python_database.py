import mysql.connector

mydb= mysql.connector.connect(

    host="localhost",
    user="root",
    passwd="MySQL",
   # database="testdatabase"
)

# print(db)

# if(db):
#     print("Connection Scueessful")
# else:
#     print("Connection Unsuccessful")

mycursor=mydb.cursor()
#mycursor.execute("CREATE DATABASE my_test_db")
mycursor.execute("Show databases")

for db in mycursor:
    print(db)

