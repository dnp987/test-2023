'''
Created on June 29, 2020
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

if __name__ == '__main__':
    file_in = 'C:/Users/Home/Desktop/Cars/CarData.xlsx'
    file_out = 'C:/Users/Home/Desktop/Cars/CarPrices-DownTownFord.xlsx'
    data_in = Excel_utils2(file_in, 'Dealers', 'in')
    dealer = data_in.sht.cell(4,1).value
    url = data_in.sht.cell(4,2).value
    #url = "https://www.downtownford.ca/Used-Inventory?Make=ford"
    #url = "https://www.downtownford.ca/Used-Inventory"

    date_time = datetime.now().strftime('%Y-%B-%d %I:%M %p') # get the date and time
    data_out = Excel_utils2(' ', dealer, 'out') # set the spreadsheet tab to the dealer name

    browser = "C:\\Selenium\\chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(browser) # Open Chrome
    #driver.maximize_window() # maximize the browser window
    wait = WebDriverWait(driver, 10)
              
    driver.get(url) # Navigate to the test website
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".compareButton"))) # wait for Compare button to be displayed
    print (driver.title)
    num_cars = driver.find_element_by_css_selector("#inventorySearchResultsContainer > div > div.resultsHeaderRow.resultsHeaderRowLayout.resultsInteractionRow.clearFix > div.count.verticalAlignMid.inlineBlock > span")
    print ("Number of cars founds on site: " , num_cars.text)
      
    count = 0
    car_info = []
    pages_remaining = True
    while pages_remaining:
        car_desc = driver.find_elements_by_css_selector(".inventoryListVehicleTitle")
        car_prices = driver.find_elements_by_css_selector('.vehiclePriceDisplay' '[itemprop]')
        
        for index, car in enumerate(car_desc):
            car_name = car.text[4:] # remove "Used" from the car description
            price = re.sub("[$,]", "", car_prices[index].text) # remove $ and ',' from the price
            if (not price.isdigit()): # if the price is "Please call" or something non-numeric, set the price to 0
                price = '0'
            print (index,":", car_name, price)
            car_info.append((car_name + " " + price).split()) 
            
        count = count + index +1
        print ("Running count: ", count)
          
        try:
            print (driver.find_element_by_link_text("Next").get_attribute('href'))
            driver.find_element_by_link_text("Next").click() # click on Next link
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".compareButton"))) # wait for Compare button to be displayed
            #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".icon-Arrow-Left-4")))
            #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventoryListVehicleTitle"))) 
            sleep (1)
        except:
            print ("Total cars processed: ", count)
            pages_remaining = False
            
    car_info = sorted(car_info)
    for index, i in enumerate(car_info):
        print (index, ":", i)
        
    print ("Saving data in a spreadsheet....")
    row = 1
    for car_line in car_info:
        col = 0
        for car_item in car_line:
            if (not car_item.isdigit()) and col>= 3 : # if the item isn't numeric then skip it
                continue
            elif (col ==3 and len(car_item) <4 and len(car_item) >1): # skip item that's numeric but not a price, except if it's 0
                continue
            data_out.set_cell(row, col+1, car_item, "Arial", False, 10 )
            col +=1
        row+=1
    data_out.set_cell(row+1, 1, ("Prices as of: " + date_time), "Arial", False, 10)
    print (dealer, "Total cars: " , count)
    data_out.save_file(file_out)
       
    driver.quit() # Close the browser and end the sesssion
