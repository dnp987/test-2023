'''
Created on July 21, 2020
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
from Cars.mazda_fix import mazda_fix
from Cars.browser_start import browser_start

if __name__ == '__main__':
    file_in = 'C:/Users/Home/Desktop/Cars/CarData.xlsx'
    data_in = Excel_utils2(file_in, 'Mazda', 'in')
    file_out = data_in.sht.cell(7,7).value
    dealer = data_in.sht.cell(7,1).value
    url = data_in.sht.cell(7,2).value
    dealer_id = (data_in.sht.cell(7,3).value).split() # convert to a list for use later
    date_time = datetime.now().strftime('%Y %B %d %I %M %p') # get the date and time
    data_out = Excel_utils2(' ', date_time, 'out') # set the spreadsheet tab to the dealer name
    driver = browser_start(url, True)
    #driver = browser_start(url)
    driver.maximize_window() # maximize the browser window
    wait = WebDriverWait(driver, 10) # set the default web element wait time
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".listing-used-button-loading"))) # wait for "LOAD MORE" data button
    print (driver.title)
    num_cars = driver.find_element_by_css_selector('.number')
    print ("Number of cars found on site: " , num_cars.text)
    scroll_pause_time = 4 
    page_count = 0
    
    while True:
        try:
            driver.find_element_by_css_selector('.listing-used-button-loading').click() # get the next set of data
            page_count +=1
            sleep(6) # need at least 4-6 seconds pause for the page data to load and settle.
            try:
                driver.find_element_by_css_selector('.cherry-popper-13463-close').click() # close the annoying pop-up if it appears
            except:
                continue
        except:
            print (page_count, " pages in total")
            break
         
    car_desc = driver.find_elements_by_css_selector('.car-name') # car description, make, model
    car_prices = driver.find_elements_by_css_selector('.price') # car prices
    stock = driver.find_elements_by_css_selector('div.car-info > div:nth-child(1)') # car stock #
    details_links = driver.find_elements_by_css_selector('.car-image')
     
    count = 0
    zero = 0
    car_info = []
    for index, car in enumerate(car_desc):
        car_name = (car.text +" ").split() # convert to a list
        year = car_name[0].split() # convert the year to a list
        make = car_name[1] 
        model = car_name[2:] # model is already a list
        make, model = mazda_fix(make, model)    
        make = make.split() # convert to a list
        model = [' '.join(model)] # merge the model into one list element
        car_desc = year + make + model
        price = car_prices[index].text
        price = re.sub("[^0-9]", "", price) #remove text and keep the numeric part
        if len(price) == 0: # if the price is "Call for price" or something non-numeric, set the price to 0
            price = '0'
            zero += 1
        price = price.split() # convert to a list
        stock_num = stock[index].text
        stock_num = (re.sub("[#]", "", stock_num)).split() # remove "#" from the stock number and convert to a list
        # link = (details_links[index].get_attribute('src')).split()
        link = ('https://www.scarboromazda.ca/en/used-inventory').split() # set to the dealer's site since the url's can't be easily found
        print (index,":", car_desc, price, stock_num, link)
        car_info.append(dealer_id + car_desc + price + stock_num + link) 
        count += 1

    car_info = sorted(car_info)
    for index, i in enumerate(car_info):
        print (index, ":", i)
        
    print ("Saving data in a spreadsheet....", file_out)
    CreateDealerSheet(data_out, car_info, date_time)
    print (dealer, "Total cars: " , count, " Total unpriced cars: ", zero)
    data_out.save_file(file_out)
       
    driver.quit() # Close the browser and end the session
    