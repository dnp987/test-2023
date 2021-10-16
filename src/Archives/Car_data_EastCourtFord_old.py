'''
Created on July 10, 2020
@author: DNP Enterprises Inc.
Since the next page icon is not easily readable, the total number of cars and cars displayed per page is used to navigate this site
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

if __name__ == '__main__':
    file_in = 'C:/Users/Home/Desktop/Cars/CarData.xlsx'
    file_out = 'C:/Users/Home/Desktop/Cars/CarPrices-EastCourtFord.xlsx'
    data_in = Excel_utils2(file_in, 'FordDealers', 'in')
    dealer = data_in.sht.cell(2,1).value
    base_url = data_in.sht.cell(2,2).value
    date_time = datetime.now().strftime('%Y-%B-%d %I:%M %p') # get the date and time
    data_out = Excel_utils2(' ', dealer, 'out') # set the spreadsheet tab to the dealer name

    browser = "C:\\Selenium\\chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(browser) # Open Chrome
    #driver.maximize_window() # maximize the browser window
    wait = WebDriverWait(driver, 10)
              
    driver.get(base_url) # Navigate to the test website
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".lg\:leading-tight"))) # wait for number of cars to be displayed
    print (driver.title)
    num_cars = driver.find_element_by_css_selector(".lg\:leading-tight").text
    num_cars = int(re.sub("[^0-9]", "", num_cars))
    print ("Number of cars found on site: " , num_cars)
    cars_per_page = 50
    num_pages = num_cars // cars_per_page
    if num_cars % cars_per_page >0: # if the number of cars per page doesn't divide evenly into the total number of cars, we need one more page
        num_pages += 1
    count = 0
    car_info = []
    print ("# of pages: ", num_pages)
    
    for page in range(num_pages):
        if page >0:
            url = base_url[:-1] + str(page+1) # remove the last character of the base url and add the next page number
            print (url)
            driver.get(url) # Navigate to the test website
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".lg\:leading-tight"))) # wait for number of cars to be displayed
            #sleep(4)

        car_desc = driver.find_elements_by_css_selector('h3' '.text-black')
        prices = driver.find_elements_by_tag_name('strong')
        #print ("# of car_desc: ", len(car_desc), "# of  prices: ", len(prices))
           
        for index, car in enumerate(car_desc):
            car_name = (car.text +" ").split()[:3] # keep the year, make, and model, remove the rest
            car_name = ' ' .join(car_name) # convert the list to a string for later
            price = re.sub("[$,]", "", prices[index].text) # remove $ and ',' from the price
            if (not price.isdigit()): # if the price is "Please call" or something non-numeric, set the price to 0
                price = '0'
            print (index,":", car_name, price)
            car_info.append((car_name + " " + price).split())
            count +=1
 
    print ("Total cars processed: ", count)
            
    car_info = sorted(car_info)
    for index, i in enumerate(car_info):
        print (index, ":", i)
        
    print ("Saving data in a spreadsheet....")
    CreateDealerSheet(data_out, car_info, date_time)
    print (dealer, "Total cars: " , count)
    data_out.save_file(file_out)
       
    driver.quit() # Close the browser and end the sesssion
