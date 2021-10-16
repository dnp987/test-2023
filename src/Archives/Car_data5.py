'''
Created on June 16, 2020
@author: DNP Enterprises Inc.
'''
from requests_html import HTMLSession
import re
from time import sleep
import pyppdf.patch_pyppeteer
from datetime import datetime
from Quotes.Excel_utils2 import Excel_utils2

if __name__ == '__main__':
    file_in = 'C:/Users/Home/Desktop/Cars/CarData.xlsx'
    file_out = 'C:/Users/Home/Desktop/Cars/CarPrices-DownTownFord.xlsx'
    data_in = Excel_utils2(file_in, 'Dealers', 'in')
    dealer = data_in.sht.cell(4,1).value
    #url = data_in.sht.cell(4,2).value
    #url = "https://www.downtownford.ca/Used-Inventory?Make=ford"
    base_url = "https://www.downtownford.ca/Used-Inventory"
    date_time = datetime.now().strftime('%Y-%B-%d %I:%M %p') # get the date and time
    data_out = Excel_utils2(' ', dealer, 'out') # set the spreadsheet tab to the dealer name
    #url = base_url+'?Page='
    # https://www.downtownford.ca/Used-Inventory?Page=1
    session = HTMLSession()
    response = session.get(base_url, headers = {"User-Agent": "Mozilla/5.0"}, timeout = 5) # get the car data from the dealer URL
    if response.status_code == 200:
        print ("Request status: OK")
    else:
        print ("Request problem:", response.status_code)
        quit() # quit the program if the request didn't work
              
    response.html.render(retries = 2, sleep = 2, wait = 2)
    sleep(0.5)
    num_cars = response.html.find('.count')[5].text
    num_cars = int(num_cars)
    print (num_cars, "cars found")
    cars_per_page = 12
    num_pages = num_cars//cars_per_page
    if num_cars%cars_per_page >0:
        num_pages +=1
    print ("# of pages: ", num_pages)
    urls = []
    count = 0
    for x in range(1, num_pages+1):
        urls.append(base_url + "?Page=" +str( x))

    for url in urls:
        response = session.get(url, timeout = 5) # load the url
        response.html.render(retries = 2, sleep = 5, wait = 5)
        print ("Getting data for ", url)
        car_details = response.html.find('.inventoryListVehicleTitle')
        #print ("car_detals:", car_details)
        #for index, i in enumerate(car_details):
            #print (index, i)
            
        car_prices = response.html.find('.vehiclePriceDisplay' '[itemprop]')
        #print ("car_prices:", car_prices)
        #for index, i in enumerate(car_prices):
            #print (index, i)
        car_info = []
        for index, car in enumerate(car_details):
            car_name = car.text[4:] # remove "Used" from the car description
            price = re.sub("[$,]", "", car_prices[index].text) # remove $ and ',' from the price
            if (not price.isdigit()): # if the price is "Please call" or something non-numeric, set the price to 0
                price = '0'
            print (index, " ", car_name, price)
        car_info.append((car_name + " " + price).split())
        car_info = sorted(car_info)
        count +=1 # count the car data
    
    print ("total # of cars: ", count+1)
    
    response.close()
    session.close()