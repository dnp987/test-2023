'''
Created on Aug 21, 2020

@author: DNP Enterprises Inc.
Loads the carsdb.dealers database from spreadsheets
'''
import mysql.connector
import openpyxl

if __name__ == '__main__':
    
    mydb = mysql.connector.connect( # setup the database connection
    host = "localhost", 
    user = "dnp",
    password = "Npaapita5",
    database = "carsdb"
    )
    mycursor = mydb.cursor()
    sql = "Delete from dealers" # Clean out database
    mycursor.execute(sql)
    
    car_data_file = 'C:/Users/Home/Desktop/Cars/CarData.xlsx'
    wkbk = openpyxl.load_workbook(car_data_file)

    for sheet in wkbk.sheetnames: #get each sheet
        print ("Loading: ", sheet)
        wksh = wkbk[sheet]
        record_count = 0
        for index, row in enumerate(wksh.rows): # for each sheet, scan the rows for data
            if index == 0:
                continue # skip first row which is for column headings
            dealer_name = row[0].value
            dealer_id = row[2].value
            dealer_address = row[3].value
            dealer_location = row[4].value
            dealer_phone = row[5].value
            print ("Name: ", dealer_name, "ID: ", dealer_id, "Address: ",  dealer_address, "Location: ", dealer_location, "Phone: ", dealer_phone)
            sql = 'INSERT into dealers (ID, Name, Location, Address, Phone) VALUES (%s, %s, %s, %s, %s)'
            val = (dealer_id, dealer_name, dealer_location, dealer_address, dealer_phone)
            record_count +=1
            mycursor.execute(sql, val)
            mydb.commit()
        print (mycursor.rowcount, "records inserted for ,", )
        print ("total records added from ", sheet, " :  ", record_count)
            