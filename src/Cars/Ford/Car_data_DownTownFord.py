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
    file_out = data_in.sht.cell(4,7).value
    dealer = data_in.sht.cell(4,1).value
    url = data_in.sht.cell(4,2).value
    dealer_id = (data_in.sht.cell(4,3).value).split() # convert to a list for use later
    date_time = datetime.now().strftime('%Y %B %d %I %M %p') # get the date and time
    data_out = Excel_utils2(' ', date_time, 'out') # set the spreadsheet tab to the dealer name
    driver = browser_start(url, True) # run browser in headless mode
    #driver = browser_start(url) # run browser in non-headless, incognito mode
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'li.resetButtonItem'))) # wait for Reset button to be displayed
    print (driver.title)
    num_cars = driver.find_element_by_css_selector('div.count.verticalAlignMid.inlineBlock').text
    num_cars = int(re.sub("[^0-9]", "", num_cars)) #remove text, keep the numeric part, and convert to integer for later use
    print ("Number of cars found on site: " , num_cars)
    
    count = 0
    zero = 0
    car_info = []
    pages_remaining = True
    while pages_remaining:
        
        try:
            driver.find_element_by_css_selector('.popCloseButton').click() # close the annoying pop-up if it appears
        except:
            pass
        
        car_desc = driver.find_elements_by_css_selector(".inventoryListVehicleTitle")
        car_prices = driver.find_elements_by_css_selector('.vehiclePriceDisplay' '[itemprop]')
        stock = driver.find_elements_by_css_selector('.field' '[itemprop = "sku"]')
        details_links = driver.find_elements_by_css_selector('.inventoryListVehicleTitle [href]')
        
        for index, car in enumerate(car_desc):
            car_name = (car.text +" ").split()[:4] # keep the year, make, and model, remove the rest
            year = car_name[0].split() # convert the year to a list
            make = car_name[1].split() # convert make to a list
            model = car_name[2:] # model is already a list
            model = [' '.join(model)] # merge the model into one list element
            car_desc = year + make + model
            price = re.sub("[$,]", "", car_prices[index].text) # remove $ and ',' from the price
            if (not price.isdigit()): # if the price is "Please call" or something non-numeric, set the price to 0
                price = '0'
                zero += 1
            price = price.split() # convert to a list
            stock_num = (stock[index].text).split() # convert to a list 
            link = (details_links[index].get_attribute('href')).split()
            print (index,":", car_desc, price, stock_num, link)
            car_info.append(dealer_id + car_desc + price + stock_num + link) 
            
        count = count + index +1
        print ("Running count: ", count)
          
        try:
            print (driver.find_element_by_link_text("Next").get_attribute('href'))
            driver.find_element_by_link_text("Next").click() # click on Next link
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'li.resetButtonItem'))) # wait for Reset button to be displayed
            sleep (4)
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
    