import mysql.connector

mydb= mysql.connector.connect(

    host="localhost",
    user="root",
    passwd="MySQL",
    database="my_test_db"
)

mycursor=mydb.cursor()

sql="UPDATE employee SET sal=60000 WHERE name='rakibuz'"
mycursor.execute(sql)
mydb.commit()
