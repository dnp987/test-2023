'''
Created on July 10, 2020
@author: DNP Enterprises Inc.
'''
from datetime import datetime
import re
#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Quotes.Excel_utils2 import Excel_utils2
from Cars.CreateDealerSheet2 import CreateDealerSheet
from Cars.Scroll_Browser import Scroll_Browser
from Cars.browser_start import browser_start

if __name__ == '__main__':
    file_in = 'C:/Users/Home/Desktop/Cars/CarData.xlsx'
    data_in = Excel_utils2(file_in, 'Ford', 'in')
    file_out = data_in.sht.cell(3,7).value
    dealer = data_in.sht.cell(3,1).value
    url = data_in.sht.cell(3,2).value
    dealer_id = (data_in.sht.cell(3,3).value).split() # convert to a list for use later
    date_time = datetime.now().strftime('%Y %B %d %I %M %p') # get the date and time
    data_out = Excel_utils2(' ', date_time, 'out') # set the spreadsheet tab to the dealer name
    
    driver = browser_start(url, True) # run browser in headless mode
    #driver = browser_start(url) # run browser in non-headless, incognito mode
    
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".srp__found-header")))
    print (driver.title)
    num_cars = driver.find_element_by_css_selector(".srp__found-header").text
    num_cars = int(re.sub("[^0-9]", "", num_cars)) #remove text, keep the numeric part, and convert to integer for later use
    print ("Number of cars found on site: " , num_cars)
    scroll_pause_time = 10 # scroll all the way down until all pages are loaded
    Scroll_Browser(driver, scroll_pause_time)
   
    car_details = driver.find_elements_by_css_selector('.vehicle-card__details')
    details_links = driver.find_elements_by_css_selector('.vehicle-card__image-area [href]')
    
    zero = 0
    count = 0
    car_info = []
    for index, car in enumerate(car_details):
        car_text = car.find_elements_by_css_selector('.vehicle-card__title')
        link = (details_links[index].get_attribute('href')).split()
        car_desc = car_text[0].text
        car_desc = (car_desc +" ").split()[:4] # keep the year, make, and model, remove the rest
        year = car_desc[0].split() # convert the year to a list
        make = car_desc[1].split() # convert make to a list
        model = car_desc[2:] # model is already a list
        model = [' '.join(model)] # merge the model into one list element
        car_desc = year + make + model

        no_price = car.find_elements_by_css_selector('.vehicle-card__no-price') # if there's no price there's a different css selector used
        if len(no_price) >0:
            price = "0"
            zero += 1
                    
        raw_price = car.find_elements_by_css_selector('.aifs')
        if len(raw_price) >0:
            price = raw_price[0].text
            price = re.sub("[$,]", "", price) # remove $ and commas from the prices so that they're numeric
            price = price.strip('\n') # remove carriage return from price
            count += 1
        price = price.split() # convert to a list
        stock_num = car.find_elements_by_css_selector('.detailed-specs__value')[0].text # get the stock # for each car
        stock_num = stock_num.split() # convert to a list
        car_info.append(dealer_id + car_desc + price + stock_num + link)
        
    print ("Priced cars: ", count, "Unpriced cars: ", zero)

    car_info = sorted(car_info)
    for index, i in enumerate(car_info):
        print (index, ":", i)
    
    print ("Saving data in a spreadsheet....", file_out)
    CreateDealerSheet(data_out, car_info, date_time)
    print (dealer, "Total cars: " , count+zero)
    data_out.save_file(file_out)
    driver.quit() # Close the browser and end the session
