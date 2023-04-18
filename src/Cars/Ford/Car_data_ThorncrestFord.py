'''
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
    file_out = data_in.sht.cell(7,7).value
    dealer = data_in.sht.cell(7,1).value
    base_url = data_in.sht.cell(7,2).value
    dealer_id = (data_in.sht.cell(7,3).value).split() # convert to a list for use later
    date_time = datetime.now().strftime('%Y %B %d %I %M %p') # get the date and time
    data_out = Excel_utils2(' ', date_time, 'out') # set the spreadsheet tab to the dealer name
    headless = True
    #headless = False
    driver = browser_start(base_url, headless) # run browser in headless mode
    wait = WebDriverWait(driver, 30)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.headline1'))) # wait for USED VEHICLES to appear
    print (driver.title)
    num_cars = int(driver.find_elements(By.CSS_SELECTOR, 'span.inventory-listing-charlie__results-info-count')[1].text)
    print ("Number of cars found on site: " , num_cars)
    
    count = 0
    zero = 0
    car_info = []
  
    pages_remaining = True
    while pages_remaining:
        car_desc = driver.find_elements(By.CSS_SELECTOR, '.inventory-tile-section-vehicle-name--model-name') # model
        year_make = driver.find_elements(By.CSS_SELECTOR, '.inventory-tile-section-vehicle-name--year-make') # year, make
        prices = driver.find_elements(By.CSS_SELECTOR, '.inventory-tile-section-price-tabs-panel-item__total-financeLease>span.inventory-tile-section-price-tabs-panel-item__total-value>span.price') # prices
        stock = driver.find_elements(By.CSS_SELECTOR, '.inventory-tile-section-stock-number') # stock #
        details_links = driver.find_elements(By.LINK_TEXT, 'See More') # links
        #test1 = driver.find_elements(By.CSS_SELECTOR,  '[data-image-container]>a') # another way to get the links
                                   
        for index, (car, yr_mk, price, stk, links)  in enumerate(zip(car_desc, year_make, prices, stock,details_links)):
            model = [''.join(car.text)] # merge the model into one list element
            year = yr_mk.text[:4].split() # convert to a list
            make = yr_mk.text[5:].split() # convert to a list
            #xx = (car_trim[index].text).split(" ", 1)
                       
            #if len(xx) >1 and xx[1] == 'SPORT': # this dealer doesn't display Mazda Sport properly, has it backwards
            #        model = model , " ",  xx[1] , " " + xx[0]
            #        model = [''.join(model)] # merge the model into one list element
            #else:
            #    model = model, '  ', (car_trim[index].text).split(" ", 1)[0]
            #    model = [''.join(model)] # merge the model into one list element
            
            car_details = year + make + model
            price = re.sub("[^0-9]", "", price.text[:-3]) #remove last .00 and text, keep the numeric part
            if len(price) == 0: # if the price is "Call for price" or something non-numeric, set the price to 0
                price = '0'
                zero += 1
            price = price.split() # convert to a list
            stock_num = (stk.text[7:]).split() # get the stock # for each car and convert to a list
            link = (links.get_attribute('href')).split() # convert to a list
            print (index,":", car_details, price, stock_num, link)
            car_info.append(dealer_id + car_details + price + stock_num + link)
            count +=1
        print ("Running count: ", count)
            
        try:
            driver.find_element(By.CSS_SELECTOR, '.simple-arrow-right').click() # click on Right arrow to get to the next page unless we're at the last page, then it won't be there
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".headline1"))) # wait for USED VEHICLES to appear
            sleep (2)
        except:
            pages_remaining = False # right arrow isn't displayed, last page reached
       
    print ("Total cars processed: ", count, " Total unpriced cars: ", zero)
    car_info = sorted(car_info)
    for index, i in enumerate(car_info):
        print (index, ":", i)
        
    close_out(driver, dealer, count, num_cars, data_out, file_out, date_time, car_info)
    