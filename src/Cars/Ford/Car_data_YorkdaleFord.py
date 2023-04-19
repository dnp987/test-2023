'''
@author: DNP Enterprises Inc.
'''
from datetime import datetime
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Quotes.Excel_utils2 import Excel_utils2
from Cars.CreateDealerSheet2 import CreateDealerSheet
from Cars.browser_start import browser_start
from Cars.Scroll_Browser import Scroll_Browser
from Cars.close_out import close_out

if __name__ == '__main__':
    file_in = 'C:/Users/dpenn/Desktop/Cars/CarData.xlsx'
    data_in = Excel_utils2(file_in, 'Ford', 'in')
    file_out = data_in.sht.cell(6,7).value
    dealer = data_in.sht.cell(6,1).value
    base_url = data_in.sht.cell(6,2).value
    dealer_id = (data_in.sht.cell(6,3).value).split() # convert to a list for use later
    date_time = datetime.now().strftime('%Y %B %d %I %M %p') # get the date and time
    data_out = Excel_utils2(' ', date_time, 'out') # set the spreadsheet tab to the dealer name

    #headless = True
    headless = False
    driver = browser_start(base_url, headless) # run browser in headless mode
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.text-4xl'))) # wait for USED VEHICLES to appear
    print (driver.title)
    num_cars = int(driver.find_elements(By.CSS_SELECTOR, 'span.text-3xl')[0].text)
    
    #if headless: # believe it or not, there's a difference in how # of cars is found headless vs non-headless
    #    num_cars = int(driver.find_elements(By.CSS_SELECTOR, '.total-value')[0].text)
    #else:
    #    num_cars = int(driver.find_elements(By.CSS_SELECTOR, '.total-value')[1].text)
    
    print ("Number of cars found on site: " , num_cars)
    count = 0
    zero = 0
    car_info = []
    
    scroll_pause_time = 5 # scroll all the way down until all pages are loaded
    pages_remaining = True
    while pages_remaining:
        Scroll_Browser(driver, scroll_pause_time)
        try:
            driver.find_element(By.CSS_SELECTOR, '.lbx-load-more-btn-div').click() # click on the more button till it's gone, then all the cars are displayed
            #driver.find_element(By.XPATH, '//*[@id="inventory"]/div/div[2]/div[2]/div/button').click() # this also works
        except:
            pages_remaining = False
                
    makes = driver.find_elements(By.CSS_SELECTOR, 'span.value__make') # make
    models = driver.find_elements(By.CSS_SELECTOR, 'span.value__model') # model
    trims = driver.find_elements(By.CSS_SELECTOR, 'span.value__trim') # trim
    years = driver.find_elements(By.CSS_SELECTOR, 'span.value__year') # trim) # year
    prices = driver.find_elements(By.CSS_SELECTOR, '.price__second') # prices
    stocks = driver.find_elements(By.CSS_SELECTOR, '.value__stock>a') # stock #
    details_links = driver.find_elements(By.CSS_SELECTOR, '.buttons__content>a') # links
                
    for index, (make, model, trim, year, price, stock, links) in enumerate(zip(makes, models, trims, years, prices, stocks, details_links)):
        model_trim = model.text + " " + trim.text
        model_trim = [' '.join(model_trim)] # merge into one list element
        make = [''.join(make.text)]
        year = [''.join(year.text)]
        car_details = year + make + model_trim
        
        price = re.sub("[^0-9]", "", price.text) #remove text and keep the numeric part
        if len(price) == 0: # if the price is "Call for price" or something non-numeric, set the price to 0
            price = '0'
            zero += 1
        price = price.split() # convert to a list
        
        stock_num = (stock.text[8:]).split() # get the stock # for each car and convert to a list
        link = (links.get_attribute('href')).split()
        
        print (index,":", car_details, price, stock_num, link)
        car_info.append(dealer_id + car_details + price + stock_num + link)
        count +=1
        
    close_out(driver, dealer, count, zero, num_cars, data_out, file_out, date_time, car_info)
