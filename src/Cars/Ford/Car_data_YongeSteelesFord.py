'''
Created on June 29, 2020
@author: DNP Enterprises Inc.
'''

from datetime import datetime
from time import sleep
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Quotes.Excel_utils2 import Excel_utils2
from Cars.browser_start import browser_start
from Cars.close_out import close_out

if __name__ == '__main__':
    file_in = 'C:/Users/dpenn/Desktop/Cars/CarData.xlsx'
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
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.page-main-h1'))) # wait for total cars in stock label to be displayed
    print (driver.title)
    num_cars = driver.find_element(By.CSS_SELECTOR, '.text-lg').text
    num_cars = re.sub("[^0-9]", "", num_cars) #remove text and keep the numeric part
    num_cars = int(num_cars) # convert string to integer for later use
    print ("Number of cars found on site: " , num_cars)
    count = 0
    zero = 0
    car_info = []
    pages_remaining = True
    while pages_remaining:
        car_desc = driver.find_elements(By.CSS_SELECTOR, ".vehicle-title")
        car_prices = driver.find_elements(By.CSS_SELECTOR, ".price-section")
        stock = driver.find_elements(By.CSS_SELECTOR, 'span.stock-number-value')
        details_links = driver.find_elements(By.CSS_SELECTOR, 'a.main-picture:first-child') # finds two for each car, only select the first one

        for index, (car, prices, stk, links) in enumerate(zip(car_desc, car_prices, stock, details_links)):
            car_name = (car.text +" ").split()[:4] # keep the year, make, and model, remove the rest
            year = car_name[0].split() # convert the year to a list
            make = car_name[1].split() # convert make to a list
            model = car_name[2:] # model is already a list
            model = [' '.join(model)] # merge the model into one list element
            car_desc = year + make + model
            
            if prices.find_elements(By.CSS_SELECTOR, 'span.sale-price-text'): # if the CSS selector is there, the price is "CONTACT US FOR PRICING"
                price = prices.find_element(By.CSS_SELECTOR, 'span.sale-price-text').text
                price = '0'
                zero += 1
                
            if prices.find_elements(By.CSS_SELECTOR, '.sale-price-value'): # if the CSS selector is there, the price is a number
                price = prices.find_element(By.CSS_SELECTOR, '.sale-price-value').text
                price = re.sub("[^0-9]", "", price)

            price = price.split() # convert to a list
            stock_num = (stk.text).split() # get the stock # for each car and convert to a list
            link = (links.get_attribute('href')).split()
            print (index, ":", car_desc, price, stock_num, link)
            car_info.append(dealer_id + car_desc + price + stock_num + link) 
        count = count + index +1
        print ("Running count: ", count)
  
        if count == num_cars: # if the running count == the number of cars displayed, we've got all the pages
            break

        driver.find_element(By.CSS_SELECTOR, ".right-arrow").click() # click on Next link
        print ("Next page clicked")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".page-main-h1"))) # wait for total cars in stock label to be displayed
        #sleep (6)

    close_out(driver, dealer, count, zero, num_cars, data_out, file_out, date_time, car_info)
