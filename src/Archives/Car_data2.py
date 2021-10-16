'''
Created on June 16, 2020

@author: Home
'''
from requests_html import HTMLSession
import pyppdf.patch_pyppeteer
import re
from datetime import datetime
from Quotes.Excel_utils2 import Excel_utils2

if __name__ == '__main__':
    file_in = 'C:/Users/Home/Desktop/Cars/CarData.xlsx'
    file_out = 'C:/Users/Home/Desktop/Cars/CarPrices-DonWayFord.xlsx'
    data_in = Excel_utils2(file_in, 'Dealers', 'in')
    dealer = data_in.sht.cell(3,1).value
    url = data_in.sht.cell(3,2).value
    date_time = datetime.now().strftime('%Y-%B-%d %I:%M %p') # get the date and time
    data_out = Excel_utils2(' ', dealer, 'out') # set the spreadsheet tab to the dealer name
    
    session = HTMLSession()
    response = session.get(url, headers = {"User-Agent": "Mozilla/5.0"}, timeout = 10) # get the car data from the dealer URL
    if response.status_code == 200:
        print ("request status: OK")
    else:
        print ("request problem:", response.status_code)
    
    response.html.render(scrolldown=100, sleep=1)
    num_cars = response.html.find('h5')[0].text
    num_cars = re.sub("[^0-9]", "", num_cars) #remove text and keep the numeric part
    print ('# of cars: ', num_cars)
    
    car_details = response.html.find('.vehicle-card__details')
    zero = 0
    count = 0
    car_info = []
    for index, car in enumerate(car_details):
        car_text = car.find('.vehicle-card__title')[0].text # get the car description - make and model
        
        if car.find('.vehicle-card__no-price'): # if "contact us for price" is displayed instead of the price, then the price is $0
            price = "0"
            zero += 1
            
        if car.find('.aifs'):
            price = car.find('.aifs')[0].text
            price = re.sub("[$,]", "", price) # remove $ and commas from the prices so that they're numeric
            count += 1
        car_info.append((car_text + " " + price).split())
        
    car_info = sorted(car_info)
    for index, i in enumerate(car_info):
        print (index, i)
    
    count =index # count the car data
           
    print ("# of priced cars: ", count, " # of unpriced cars: ", zero, )

    row = 1
    for car_line in car_info:
        col = 0
        for car_item in car_line:
            if (not car_item.isdigit()) and col>= 3 : # if the item isn't numeric then skip it
                continue
            elif (col ==3 and len(car_item) <4 and len(car_item) >1): # skip item that's numeric but not a price, except if it's 0
                continue 
            data_out.set_cell(row, col+1, car_item, "Arial", False, 10 )
            col +=1
        row+=1

    data_out.set_cell(row+1, 1, ("Prices as of: " + date_time), "Arial", False, 10)
    print (dealer, "Total cars: " , num_cars)
    data_out.save_file(file_out)

    response.close()
    session.close()