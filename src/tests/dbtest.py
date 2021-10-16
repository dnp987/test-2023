'''
Created on Aug 10, 2020

@author: DNP Enterprises Inc.
'''
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost", 
    user = "dnp",
    password = "Npaapita5",
    database = "carsdb"
)
print (mydb)

mycursor = mydb.cursor()

sql = "Delete from dealers" # Clean out database
mycursor.execute(sql)

dealer_id = 'EASTCOURTFORD'
dealer_name = 'Eastcourt Ford'
dealer_location = 'Toronto'
dealer_address = '4700 Sheppard Avenue East , Toronto ON M1S3V6'
dealer_phone = '416 123 1234'

sql = "INSERT into dealers (ID, Name, Location, Address, Phone) values (%s, %s, %s, %s, %s)"
val = (dealer_id, dealer_name, dealer_location, dealer_address, dealer_phone)
mycursor.execute(sql, val)
mycursor.executemany(sql, val) # for when you're inserting more than one value
mydb.commit()
print (mycursor.rowcount, "records inserted")

mycursor.execute("select * from dealers")
myresult = mycursor.fetchall()

for x in myresult:
    print (x)