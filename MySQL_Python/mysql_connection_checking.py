from datetime import datetime
import mysql.connector

db= mysql.connector.connect(

    host="localhost",
    user="root",
    passwd="MySQL",
    database="testdatabase"
)

mycursor=db.cursor()
#mycursor.execute("CREATE DATABASE testdatabase")

#mycursor.execute("CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED,personID int PRIMARY KEY AUTO_INCREMENT)")

#mycursor.execute("DESCRIBE Person")
# for x in mycursor:
#     print(x)

# mycursor.execute("INSERT INTO Person (name,age) VALUES (%s,%s)",("hafiz",27))
# db.commit()

# mycursor.execute("SELECT *FROM Person")
# for x in mycursor:
#     print(x)

#mycursor.execute("CREATE TABLE Test(name varchar(50) NOT NULL,created datetime NOT NULL, gender ENUM('M','F','O') NOT NULL, id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")

mycursor.execute("INSERT INTO Test (name,created,gender) VALUES (%s,%s,%s)",('Zara',datetime.now(),"F"))
db.commit()