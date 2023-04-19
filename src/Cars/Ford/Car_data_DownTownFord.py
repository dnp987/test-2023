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
    file_out = data_in.sht.cell(4,7).value
    dealer = data_in.sht.cell(4,1).value
    url = data_in.sht.cell(4,2).value
    dealer_id = (data_in.sht.cell(4,3).value).split() # convert to a list for use later
    date_time = datetime.now().strftime('%Y %B %d %I %M %p') # get the date and time
    data_out = Excel_utils2(' ', date_time, 'out') # set the spreadsheet tab to the dealer name
    driver = browser_start(url, True) # run browser in headless mode
    #driver = browser_start(url) # run browser in non-headless, incognito mode
    wait = WebDriverWait(driver, 10)
    #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-asset-name="Downtown Ford Logo Click For Homepage"]')))
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.count')))
    print (driver.title)
    num_cars = driver.find_element(By.CSS_SELECTOR, 'span.count').text
    num_cars = int(re.sub("[^0-9]", "", num_cars)) #remove text, keep the numeric part, and convert to integer for later use
    print ("Number of cars found on site: " , num_cars)
    
    count = 0
    zero = 0
    car_info = []
    pages_remaining = True
    while pages_remaining:
        
        try:
            driver.find_element(By.CSS_SELECTOR, '.popCloseButton').click() # close the annoying pop-up if it appears
        except:
            pass
        
        car_desc = driver.find_elements(By.CSS_SELECTOR, ".inventoryListVehicleTitle")
        car_prices = driver.find_elements(By.CSS_SELECTOR, '.vehiclePriceDisplay' '[itemprop]')
        stock = driver.find_elements(By.CSS_SELECTOR, 'div.textboxContentWrapperInner em')
        details_links = driver.find_elements(By.CSS_SELECTOR, '.inventoryListVehicleTitle [href]')

        for index, (car, price, stk, links) in enumerate(zip(car_desc, car_prices, stock, details_links)):
            car_name = (car.text +" ").split()[:4] # keep the year, make, and model, remove the rest
            year = car_name[0].split() # convert the year to a list
            make = car_name[1].split() # convert make to a list
            model = car_name[2:] # model is already a list
            model = [' '.join(model)] # merge the model into one list element
            car_desc = year + make + model
            price = re.sub("[$,]", "", price.text) # remove $ and ',' from the price
            if (not price.isdigit()): # if the price is "Please call" or something non-numeric, set the price to 0
                price = '0'
                zero += 1
            price = price.split() # convert to a list
            stock_num = stk.text[8:].split() # remove "Stock #:" and keep the stock #
            link = links.get_attribute('href').split()
            print (index,":", car_desc, price, stock_num, link)
            car_info.append(dealer_id + car_desc + price + stock_num + link) 
            
        count = count + index +1
        print ("Running count: ", count)
          
        try:
            next_page = driver.find_element(By.LINK_TEXT, "Next")
            print (next_page.get_attribute('href'))
            next_page.click() # click on Next link
            sleep (2)
        except:
            pages_remaining = False
        
    close_out(driver, dealer, count, zero, num_cars, data_out, file_out, date_time, car_info)
        