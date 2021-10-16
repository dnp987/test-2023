'''
Created on July 21, 2020
@author: DNP Enterprises Inc.
'''
from datetime import datetime
from time import sleep
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Quotes.Excel_utils2 import Excel_utils2
from Cars.CreateDealerSheet2 import CreateDealerSheet
from Cars.Scroll_Browser import Scroll_Browser

if __name__ == '__main__':
    file_in = 'C:/Users/Home/Desktop/Cars/CarData.xlsx'
    file_out = 'C:/Users/Home/Desktop/Cars/Mazda/CarPrices-ScarboroMazda.xlsx'
    data_in = Excel_utils2(file_in, 'Mazda_Dealers', 'in')
    dealer = data_in.sht.cell(7,1).value
    url = data_in.sht.cell(7,2).value
    #url = "https://www.scarboromazda.ca/en/used-inventory"

    date_time = datetime.now().strftime('%Y-%B-%d %I:%M %p') # get the date and time
    data_out = Excel_utils2(' ', dealer, 'out') # set the spreadsheet tab to the dealer name

    browser = "C:\\Selenium\\chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(browser) # Open Chrome
    driver.maximize_window() # maximize the browser window
    wait = WebDriverWait(driver, 10)
              
    driver.get(url) # Navigate to the test website
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".header__logo"))) # wait for dealer logo to be displayed
    print (driver.title)
    num_cars = driver.find_element_by_css_selector('.number')
    print ("Number of cars found on site: " , num_cars.text)
    
    count = 0
    zero = 0
    car_info = []
    scroll_pause_time = 4
    remaining_pages = True
    while remaining_pages: # load all of the data
        car_desc = driver.find_elements_by_css_selector('.car-name')
        car_prices = driver.find_elements_by_css_selector('.price')
    
        for index, car in enumerate(car_desc):
            #car_name = (car.text +" ").split()[:4] # keep the year, make, and model, remove the rest
            car_name = (car.text +" ").split() # convert to a list
            year = car_name[0].split() # convert the year to a list
            make = car_name[1].split() # convert make to a list
            model = car_name[2:] # model is already a list
            print ("***", year, make, model)
            if make == 'Mazda3':
                model = "3"
                make = "Mazda"
            if make == 'Mazda6':
                model = "6"
                make = "Mazda"
            
            print ("@@@", make, model)
                    
            model = [' '.join(model)] # merge the model into one list element
            car_desc = year + make + model
            price = car_prices[index].text
            price = re.sub("[^0-9]", "", price) #remove text and keep the numeric part
            if len(price) == 0: # if the price is "Call for price" or something non-numeric, set the price to 0
                price = '0'
                zero += 1
            price = price.split() # convert to a list
            print (index,":", car_desc, price)
            car_info.append(car_desc + price) 
            count += 1
            print ("Running count: ", count)
        try:
            driver.find_element_by_css_selector('.listing-used-button-loading').click() # get the next set of data
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".header__logo"))) # wait for dealer logo to be displayed
            Scroll_Browser(driver, scroll_pause_time) # scroll all the way down until all pages are loaded
            sleep(4)
            try:
                driver.find_element_by_css_selector('.cherry-popper-13463').click() # if a pop-up appears, close it
            except:
                pass
        except: # if the "LOAD MORE" button is not there, we've got all the data
            print ("Are we there yet?")
            break
                
    car_info = sorted(car_info)
    for index, i in enumerate(car_info):
        print (index, ":", i)
        
    print ("Saving data in a spreadsheet....")
    CreateDealerSheet(data_out, car_info, date_time)
    print (dealer, "Total cars: " , count, " Total unpriced cars: ", zero)
    data_out.save_file(file_out)
       
    driver.quit() # Close the browser and end the sesssion
