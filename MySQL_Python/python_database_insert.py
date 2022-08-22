import mysql.connector

mydb= mysql.connector.connect(

    host="localhost",
    user="root",
    passwd="MySQL",
    database="my_test_db"
)

mycursor=mydb.cursor()

sqlform="Insert into employee(name,sal) values(%s,%s)"

employees= [("Rakibuz",20000),("amit",30000),("mubin",40000)]
mycursor.executemany(sqlform,employees)
mydb.commit()