'''
Created on July 20, 2020
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
    data_in = Excel_utils2(file_in, 'Mazda', 'in') # filename and path, tab name,, input or output
    file_out = data_in.sht.cell(3,7).value
    dealer = data_in.sht.cell(3,1).value
    url = data_in.sht.cell(3,2).value
    dealer_id = (data_in.sht.cell(3,3).value).split() # convert to a list for use later
    date_time = datetime.now().strftime('%Y %B %d %I %M %p') # get the date and time
    data_out = Excel_utils2(' ', date_time, 'out') # set the spreadsheet tab to the dealer name
    driver = browser_start(url, True)
    #driver = browser_start(url)
    driver.implicitly_wait(10) # set the default wait intervals
    wait = WebDriverWait(driver, 20)
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".title__primary")))# wait for the page title to load
    print (driver.title)
    num_cars = driver.find_element_by_css_selector(".inventory-listing__results-info-count").text # get the total cars for sale
    num_cars = int(re.sub("[^0-9]", "", num_cars)) #remove text, keep the numeric part, and convert to integer for later use
    print ("Number of cars found on site: " , num_cars)
   
    zero = 0
    count = 0
    car_info = []
    pages_remaining = True
    while pages_remaining:
        car_desc = driver.find_elements_by_css_selector('a.inventory-list-layout__preview-name')
        car_prices = driver.find_elements_by_css_selector('.inventory-list-layout__preview-price-current')
        raw_stock = driver.find_elements_by_css_selector('.inventory-list-layout__preview-stock')
        details_links = driver.find_elements_by_css_selector('.inventory-list-layout__preview-actions-cta [href]')
        
        for index, car in enumerate(car_desc):
            car_name = (car.text +" ").split()[:5] # keep the year, make, and model, remove the rest
            if '-' in car_name:
                car_name = car_name[0: car_name.index("-")]
                 
            year = car_name[0].split() # convert the year to a list
            make = car_name[1]
            model = car_name[2:] # model is already a list
            make, model = mazda_fix(make, model)    
            make = make.split() #convert to a list
            model = [' '.join(model)] # merge the model into one list element
            car_desc = year + make + model
            price = car_prices[index].text
            price = re.sub("[^0-9]", "", price) #remove text and keep the numeric part
            if len(price) == 0: # if the price is "Call for price" or something non-numeric, set the price to 0
                price = '0'
                zero += 1
            price = price.split() # convert to a list
            stock_num = ((raw_stock[index].text).split('Inventory #')[1]).split()
            link = (details_links[index].get_attribute('href')).split()
            print (index,":", car_desc, price, stock_num, link)
            car_info.append(dealer_id + car_desc + price + stock_num + link) 
            
        count = count + index +1
        print ("Running count: ", count)
          
        try:
            next_page = driver.find_element_by_css_selector('[data-theme-sprite = "simple-arrow-right"]')
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-theme-sprite = "simple-arrow-right"]'))) # wait for right arrow to be displayed
            next_page.click()
        except:
            print ("Total cars processed: ", count, " Total unpriced cars: ", zero)
            pages_remaining = False
            
    car_info = sorted(car_info)
    for index, i in enumerate(car_info):
        print (index, ":", i)
        
    print ("Saving data in a spreadsheet....", file_out)
    CreateDealerSheet(data_out, car_info, date_time)
    print (dealer, "Total cars: " , count)
    data_out.save_file(file_out)
       
    driver.quit() # Close the browser and end the session
