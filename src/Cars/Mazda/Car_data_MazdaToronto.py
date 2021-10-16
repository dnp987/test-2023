'''
Created on July 21, 2020
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
from Cars.mazda_fix import mazda_fix
from Cars.browser_start import browser_start

if __name__ == '__main__':
    file_in = 'C:/Users/Home/Desktop/Cars/CarData.xlsx'
    data_in = Excel_utils2(file_in, 'Mazda', 'in') # filename and path, tab name,, input or output
    file_out = data_in.sht.cell(5,7).value
    dealer = data_in.sht.cell(5,1).value
    url = data_in.sht.cell(5,2).value
    dealer_id = (data_in.sht.cell(5,3).value).split() # convert to a list for use later
    date_time = datetime.now().strftime('%Y %B %d %I %M %p') # get the date and time
    data_out = Excel_utils2(' ', date_time, 'out') # set the spreadsheet tab to the dealer name
    driver = browser_start(url, True)
    #driver = browser_start(url)
    driver.implicitly_wait(10) # set the default wait intervals
    wait = WebDriverWait(driver, 10)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'new-listing-title'))) # wait for the page title to load
    print (driver.title)
    num_cars = driver.find_element_by_css_selector(".v3-vehicle-count").text # get the total cars for sale
    num_cars = int(re.sub("[^0-9]", "", num_cars)) #remove text, keep the numeric part, and convert to integer for later use
    print ("Number of cars found on site: " , num_cars)
    scroll_pause_time = 2 # scroll all the way down until all pages are loaded
    Scroll_Browser(driver, scroll_pause_time)
  
    zero = 0
    count = 0
    car_info = []
    car_details = driver.find_elements_by_css_selector('.veh-info-1')
    details_links = driver.find_elements_by_css_selector('.btn-instock-inv-1 .btn-view-detail')
    for index, car in enumerate(car_details):
        car_text = car.find_element_by_css_selector('.vehicle-year-make-model').text
        car_desc = (car_text +" ").split()[:5] # keep the year, make, and model, remove the rest
        year = car_desc[0].split() # convert the year to a list
        make = car_desc[1] 
        model = car_desc[2:] # model is already a list
        make, model = mazda_fix(make, model)
        model = [' '.join(model)] # merge the model into one list element
        make = make.split() # convert make to a list
        car_desc = year + make + model
        price =  car.find_element_by_css_selector('.vehicle-price-2-new').text 
        price = re.sub("[^0-9]", "", price) #remove text and keep the numeric part
        if len(price) == 0: # if the price is "Call for price" or something non-numeric, set the price to 0
            price = '0'
            zero += 1
        else:
            count += 1
        price = price.split() # convert price to a list
        stock = driver.find_elements_by_css_selector('td.table-col-1' '[itemprop = "sku"]')
        stock_num = (stock[index].text).split() # get the car stock # and convert to a list
        link = (details_links[index].get_attribute('href')).split()
        print (index, ": ", car_desc, price, stock_num, link)
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
