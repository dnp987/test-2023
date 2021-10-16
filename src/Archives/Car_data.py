'''
Created on May 29, 2020

@author: Home
'''
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from Quotes.Excel_utils2 import Excel_utils2

if __name__ == '__main__':
    file_in = 'C:/Users/Home/Desktop/Cars/CarData.xlsx'
    file_out = 'C:/Users/Home/Desktop/Cars/CarPrices-EastCourtFordLincoln.xlsx'
    data_in = Excel_utils2(file_in, 'Dealers', 'in')
    dealer = data_in.sht.cell(2,1).value
    date_time = datetime.now().strftime('%Y-%B-%d %I:%M %p') # get the date and time
    data_out = Excel_utils2(' ', dealer, 'out') # set the spreadsheet tab to the dealer name
    URL = data_in.sht.cell(2,2).value
    
    page = requests.get(URL) # get the car data from the dealer URL
    soup = BeautifulSoup(page.content, 'html.parser')
    prices = soup.find_all('strong')
    cars = soup.find_all('h3')
    
    car_data = [ ]
    for index, car in enumerate(cars):
        print (car)
        price = (prices[index].text).strip("$") # remove $ and commas from the prices so that they're numeric
        price = price.replace(',' , '')
        car_data.append((car.text + " " + price).split())
        
    count =index +1 # count the car data
    car_data = sorted(car_data)
        
    row = 1
    for car_line in car_data:
        col = 0
        for car_item in car_line:
            if (not car_item.isdigit()) and col>= 3: # if the item isn't numeric then skip it
                continue
            data_out.set_cell(row, col+1, car_item, "Arial", False, 10 )
            col +=1
        row+=1

    data_out.set_cell(row+1, 1, ("Prices as of: " + date_time), "Arial", False, 10)
    print (dealer, "Total cars: " , count)
    data_out.save_file(file_out)