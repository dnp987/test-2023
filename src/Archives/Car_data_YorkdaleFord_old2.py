'''
Created on July 14, 2020
@author: DNP Enterprises Inc.
'''
# -*- coding: utf-8 -*-

from datetime import datetime
from time import sleep
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Quotes.Excel_utils2 import Excel_utils2
from Cars.CreateDealerSheet2 import CreateDealerSheet

if __name__ == '__main__':
    file_in = 'C:/Users/Home/Desktop/Cars/CarData.xlsx'
    file_out = 'C:/Users/Home/Desktop/Cars/CarPrices-YorkdaleFord.xlsx'
    data_in = Excel_utils2(file_in, 'FordDealers', 'in')
    dealer = data_in.sht.cell(6,1).value
    url = data_in.sht.cell(6,2).value
    #url = "https://yorkdaleford.com/pre-owned-inventory//"
    date_time = datetime.now().strftime('%Y-%B-%d %I:%M %p') # get the date and time
    data_out = Excel_utils2(' ', dealer, 'out') # set the spreadsheet tab to the dealer name
    browser = "C:\\Selenium\\chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(browser) # Open Chrome
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 10)
              
    driver.get(url) # Navigate to the test website
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1'))) # wait for heading/title to be displayed
    print (driver.find_element_by_css_selector('h1').text)
    count = 0
    car_info = []
    pages_remaining = True
    active_color = driver.find_element_by_link_text('\xbb').value_of_css_property('color') #get the color of the next page link while it's active/not grayed out
    current_color = active_color
    
    while pages_remaining: 
        car_desc = driver.find_elements_by_css_selector('a'  "[ui-sref='detail({ slug: item.getSlug() })']" '.ng-binding') # get the car description
        car_prices = driver.find_elements_by_css_selector('.price' '.ng-binding') # get the car prices
        
        for index, car in enumerate(car_desc):
            car_name = (car.text +" ").split()[:3] # keep the year, make, and model, remove the rest
            car_name = ' ' .join(car_name) # convert the list to a string for later
            price = re.sub("[^0-9]", "", car_prices[index].text) #remove text and keep the numeric part
            if len(price) == 0: # if the price is "Call for price" or something non-numeric, set the price to 0
                price = '0'
            #print (index, ":", car_name, price)
            car_info.append((car_name + " " + price).split()) 
            
        count = count + index +1
        print ("Running count: ", count)
        
        if active_color != current_color: # last page has been reached if the next page icon ">>" has changed color
            break
        
        print (driver.find_element_by_css_selector("[aria-label=Next]").get_attribute('href'))
        driver.find_element_by_link_text('\xbb').click() # click on >> next page link
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1'))) # wait for heading/title to be displayed
        sleep(2)
        current_color = driver.find_element_by_link_text('\xbb').value_of_css_property('color')
        
    print ("Total cars processed: ", count)
    car_info = sorted(car_info)
    for index, i in enumerate(car_info):
        print (index, ":", i)
    
    print ("Saving data in a spreadsheet....")
    CreateDealerSheet(data_out, car_info, date_time)
    print (dealer, "Total cars: " , count)
    data_out.save_file(file_out)
       
    driver.quit() # Close the browser and end the session
