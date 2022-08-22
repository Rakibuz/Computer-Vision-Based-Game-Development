import mysql.connector

mydb= mysql.connector.connect(

    host="localhost",
    user="root",
    passwd="MySQL",
    database="my_test_db"
)

mycursor=mydb.cursor()

#mycursor.execute("Create table employee(name varchar(200), sal int(20))")

mycursor.execute("Show tables")

for tb in mycursor:
    print(tb)