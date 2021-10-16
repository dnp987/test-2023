'''
Created on June 29, 2020
@author: DNP Enterprises Inc.
'''

from datetime import datetime
from time import sleep
import re
#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Quotes.Excel_utils2 import Excel_utils2
from Cars.CreateDealerSheet2 import CreateDealerSheet
from Cars.browser_start import browser_start

if __name__ == '__main__':
    file_in = 'C:/Users/Home/Desktop/Cars/CarData.xlsx'
    data_in = Excel_utils2(file_in, 'Ford', 'in')
    file_out = data_in.sht.cell(5,7).value
    dealer = data_in.sht.cell(5,1).value
    url = data_in.sht.cell(5,2).value
    dealer_id = (data_in.sht.cell(5,3).value).split() # convert to a list for use later
    date_time = datetime.now().strftime('%Y %B %d %I %M %p') # get the date and time
    data_out = Excel_utils2(' ', date_time, 'out') # set the spreadsheet tab to the dealer name
    #driver = browser_start(url, False)
    driver = browser_start(url, True)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".total-value"))) # wait for total cars in stock label to be displayed
    print (driver.title)
    num_cars = driver.find_element_by_css_selector(".total-value").text
    num_cars = re.sub("[^0-9]", "", num_cars) #remove text and keep the numeric part
    num_cars = int(num_cars) # convert string to integer for later use
    print ("Number of cars found on site: " , num_cars)
    count = 0
    zero = 0
    car_info = []
    pages_remaining = True
    while pages_remaining:
        car_desc = driver.find_elements_by_css_selector(".vehicle-title")
        car_prices = driver.find_elements_by_css_selector(".price-section")
        stock = driver.find_elements_by_css_selector('span.stock-number-value')
        details_links = driver.find_elements_by_css_selector('a.main-picture')
        
        car_link = []
        for index, links in enumerate(details_links):
            if index % 2 == 0: # take only the first link, drop the one after
                car_link.append(links.get_attribute('href'))
        
        for index, car in enumerate(car_desc):
            car_name = (car.text +" ").split()[:4] # keep the year, make, and model, remove the rest
            year = car_name[0].split() # convert the year to a list
            make = car_name[1].split() # convert make to a list
            model = car_name[2:] # model is already a list
            model = [' '.join(model)] # merge the model into one list element
            car_desc = year + make + model
            
            if car_prices[index].find_elements_by_css_selector('span.sale-price-text'): # if the price is "CONTACT US FOR PRICING"
                price = car_prices[index].find_element_by_css_selector('span.sale-price-text').text
                price = '0'
                zero += 1
                
            if car_prices[index].find_elements_by_css_selector('.sale-price-value'):
                price = car_prices[index].find_element_by_css_selector('.sale-price-value').text
                price = re.sub("[^0-9]", "", price)

            price = price.split() # convert to a list
            stock_num = (stock[index].text).split() # get the stock # for each car and convert to a list
            link = car_link[index].split()
            print (index, ":", car_desc, price, stock_num, link)
            car_info.append(dealer_id + car_desc + price + stock_num + link) 
        count = count + index +1
        print ("Running count: ", count)
  
        if count == num_cars: # if the running count == the number of cars displayed, we've got all the pages
            break

        driver.find_element_by_css_selector(".right-arrow").click() # click on Next link
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".total-value"))) # wait for total cars in stock label to be displayed
        sleep (6)

    print ("Total cars processed: ", count, " Total unpriced cars: ", zero)
                
    car_info = sorted(car_info)
    for index, i in enumerate(car_info):
        print (index, ":", i)
    
    print ("Saving data in a spreadsheet....", file_out)
    CreateDealerSheet(data_out, car_info, date_time)
    print (dealer, "Total cars: " , count)
    data_out.save_file(file_out)
       
    driver.quit() # Close the browser and end the session
