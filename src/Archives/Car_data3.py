'''
Created on June 16, 2020
@author: DNP Enterprises Inc.
reached a possible dead end because the next page is not always consistently found
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
    url = "https://www.downtownford.ca/Used-Inventory"
    date_time = datetime.now().strftime('%Y-%B-%d %I:%M %p') # get the date and time
    data_out = Excel_utils2(' ', dealer, 'out') # set the spreadsheet tab to the dealer name
    
    session = HTMLSession()
    response = session.get(url, headers = {"User-Agent": "Mozilla/5.0"}, timeout = 10) # get the car data from the dealer URL
    if response.status_code == 200:
        print ("Request status: OK")
    else:
        print ("Request problem:", response.status_code)
        quit() # quit the program if the request didn't work
              
    print ("Before initial render:", response.html.next())
    response.html.render(retries = 2, sleep = 2, wait = 2)
    sleep(0.5)
    print ("After initial render:", response.html.next())
    #print ("Absolute links: ", response.html.absolute_links)
    num_cars = response.html.find('.count')
    ''''print (num_cars[0].attrs)
    for index, i in enumerate(num_cars):
        print (index, ": ", i.text) '''
    print (num_cars[5].text, "cars found")
    
    car_details = response.html.find('.inventoryListVehicleTitle')
    car_prices = response.html.find('.vehiclePriceDisplay' '[itemprop]')
    '''for  index, i in enumerate(car_prices):
        print ("Car_prices", index, ": ", i.attrs, " ", i.text) '''
    
    for index, car in enumerate(car_details):
        car_name = car.text[4:] # remove "Used" from the car description
        price = re.sub("[$,]", "", car_prices[index].text) # remove $ and ',' from the price
        if (not price.isdigit()): # if the price is "Please call" or something non-numeric, set the price to 0
            price = '0'
        print (index, " ", car_name, price)

    next_page = response.html.next()
    print ("Before while loop: ", next_page)
    j =0
    while next_page != None:
        response = session.get(next_page, timeout = 5)
        response.html.render(retries = 2, sleep = 2, wait = 2)
        sleep (0.5)
        next_page = response.html.next()
        print ("Inside while loop: ", next_page)
        j+= 1
        print ("Count: ", j)

    
    response.close()
    session.close()