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
from Cars.CreateDealerSheet2 import CreateDealerSheet
from Cars.browser_start import browser_start

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
        years = driver.find_elements(By.CSS_SELECTOR, '.inventory-tile-section-vehicle-name--year-make') # year, make
        prices = driver.find_elements(By.CSS_SELECTOR, 'span.price') # prices
        stock = driver.find_elements(By.CSS_SELECTOR, '.inventory-tile-section-stock-number') # stock #
        details_links = driver.find_elements(By.LINK_TEXT, 'See More') # links
                        
        for index, car in enumerate(car_desc):
            model = car.text[:-9].split() # convert to a list
            year = years[index].text[:4].split() # convert to a list
            make = years[index].text[5:].split() # convert to a list
            #xx = (car_trim[index].text).split(" ", 1)
                       
            #if len(xx) >1 and xx[1] == 'SPORT': # this dealer doesn't display Mazda Sport properly, has it backwards
            #        model = model , " ",  xx[1] , " " + xx[0]
            #        model = [''.join(model)] # merge the model into one list element
            #else:
            #    model = model, '  ', (car_trim[index].text).split(" ", 1)[0]
            #    model = [''.join(model)] # merge the model into one list element
            
            car_details = year + make + model
            price = re.sub("[^0-9]", "", prices[index].text) #remove text and keep the numeric part
            if len(price) == 0: # if the price is "Call for price" or something non-numeric, set the price to 0
                price = '0'
                zero += 1
            price = price.split() # convert to a list
            stock_num = (stock[index].text[7:]).split() # get the stock # for each car and convert to a list
            link = (details_links[index].get_attribute('href'))
            #print (index,":", car_details, price, stock_num, link)
            #car_info.append(dealer_id + car_details + price + stock_num + link)
            count +=1
        print ("Running count: ", count)
            
        try:
            driver.find_element(By.CSS_SELECTOR, '.right-arrow-svg').click() # click on Right arrow to get to the next page unless we're at the last page, then it won't be there
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".page-main-h1"))) # wait for USED VEHICLES to appear
            sleep (2)
        except:
            pages_remaining = False # right arrow isn't displayed, last page reached
       
    print ("Total cars processed: ", count, " Total unpriced cars: ", zero)
    car_info = sorted(car_info)
    for index, i in enumerate(car_info):
        print (index, ":", i)
        
    print ("Saving data in a spreadsheet....", file_out)
    CreateDealerSheet(data_out, car_info, date_time)
    print (dealer, "Total cars: " , count)
    data_out.save_file(file_out)
       
    driver.quit() # Close the browser and end the session
    