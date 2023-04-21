'''
@author: DNP Enterprises Inc.
Updated 21Apr2023
'''
from datetime import datetime
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Quotes.Excel_utils2 import Excel_utils2
from Cars.browser_start import browser_start
from Cars.close_out import close_out

if __name__ == '__main__':
    file_in = 'C:/Users/dpenn/Desktop/Cars/CarData.xlsx'
    data_in = Excel_utils2(file_in, 'Chrysler', 'in')
    file_out = data_in.sht.cell(4,7).value
    dealer = data_in.sht.cell(4,1).value
    url = data_in.sht.cell(4,2).value
    dealer_id = (data_in.sht.cell(4,3).value).split() # convert to a list for use later
    date_time = datetime.now().strftime('%Y %B %d %I %M %p') # get the date and time
    data_out = Excel_utils2(' ', date_time, 'out') # set the spreadsheet tab to the dealer name
    
    #headless = False
    headless = True
    driver = browser_start(url, headless)
    
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.viewing-range'))) # wait for the total number of cars to appear
    print (driver.title)
    car_totals = driver.find_element(By.CSS_SELECTOR, 'p.viewing-range').text
    num_cars = car_totals.split('of')[1]
    num_cars = int(re.sub("[^0-9]", "", num_cars)) #remove text, keep the numeric part
    cars_per_page = int((car_totals.split(" ")[1]).split("-")[1])
    num_pages = num_cars // cars_per_page
    if (num_cars % cars_per_page):
        num_pages += 1

    print ("Number of cars found on site: " , num_cars) 
    zero = 0
    count = 0
    car_info = []
    
    for page in range(1, (num_pages+1)):
        next_url = url + "&pg=" + str(page)
        print ("Processing page: " , next_url)
        driver.get(next_url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.viewing-range'))) # wait for the total number of cars to appear
        
        car_details = driver.find_elements(By.CSS_SELECTOR, '.vehicle-card__details')
        car_prices = driver.find_elements(By.CSS_SELECTOR, '[convertus-data-id="srp__dealer-price"]')
        details_links = driver.find_elements(By.CSS_SELECTOR, '.vehicle-card__image-wrap [href]')
        
        for index, car in enumerate(car_details):
            car_text = car.find_elements(By.CSS_SELECTOR, '.vehicle-card__title')
            link = (details_links[index].get_attribute('href')).split()
            car_desc = car_text[0].text
            car_desc = (car_desc +" ").split()[:4] # keep the year, make, and model, remove the rest
            year = car_desc[0].split() # convert the year to a list
            make = car_desc[1].split() # convert make to a list
            model = car_desc[2:] # model is already a list
            model = [' '.join(model)] # merge the model into one list element
            car_desc = year + make + model
            
            price = car_prices[index].text
            price = price.strip('\n') # remove carriage return from price
            price= re.sub("[^0-9]", "", price) #remove text, keep the numeric part
            price = price.split() # convert to a list
            if len(price) == 0: #if there's no price, set it to 0
                price = "0"
                zero += 1

            count += 1
            stock_num = ('n/a').split() # stock # not available on this site
            print (index, " : ", dealer_id + car_desc + price + stock_num + link)
            car_info.append(dealer_id + car_desc + price + stock_num + link)
    close_out(driver, dealer, count, zero, num_cars, data_out, file_out, date_time, car_info)
