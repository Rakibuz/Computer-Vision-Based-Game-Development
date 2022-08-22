import mysql.connector

mydb= mysql.connector.connect(

    host="localhost",
    user="root",
    passwd="MySQL",
    database="my_test_db"
)

mycursor=mydb.cursor()