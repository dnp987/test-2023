from datetime import datetime
from time import sleep
import re
#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Quotes.Excel_utils2 import Excel_utils2
from Cars.CreateDealerSheet2 import CreateDealerSheet
from Cars.mazda_fix import mazda_fix
from Cars.browser_start import browser_start

if __name__ == '__main__':
    file_in = 'C:/Users/Home/Desktop/Cars/CarData.xlsx'
    data_in = Excel_utils2(file_in, 'GM', 'in')
    file_out = data_in.sht.cell(3,7).value
    dealer = data_in.sht.cell(3,1).value
    url = data_in.sht.cell(3,2).value
    dealer_id = (data_in.sht.cell(3,3).value).split() # convert to a list for use later
    date_time = datetime.now().strftime('%Y %B %d %I %M %p') # get the date and time
    data_out = Excel_utils2(' ', date_time, 'out') # set the spreadsheet tab to the dealer name
    driver = browser_start(url, True)
    #driver = browser_start(url, False)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1 span.stats"))) # wait for total cars in stock label to be displayed
    print (driver.title)
    num_cars = driver.find_element_by_css_selector("h1 span.stats").text
    num_cars = re.sub("[^0-9]", "", num_cars) #remove text and keep the numeric part
    num_cars = int(num_cars) # convert string to integer for later use
    print ("Number of cars found on site: " , num_cars)
   
    count = 0
    zero = 0
    car_info = []
    pages_remaining = True
    while pages_remaining:
        car_desc = driver.find_elements_by_css_selector("span.title-bottom")
        car_year = driver.find_elements_by_css_selector("span.title-top")
        car_prices = driver.find_elements_by_css_selector(".hit-price__value")
        stock = driver.find_elements_by_css_selector('div.stock-row')
        details_links = driver.find_elements_by_css_selector('a.hit-link')
        print (driver.find_element_by_css_selector("div.pagination-state").text)
       
        for index, car in enumerate(car_desc):
            car_name = (car.text +" ").split()[:5] # keep the year, make, and model, remove the rest
            make = car_name[0]
            model = car_name[1:]
            make, model = mazda_fix(make, model)            
            model = [' '.join(model)] # merge the model into one list element
            make = make.split() # convert make to a list
            year = (re.sub("[^0-9]", "", car_year[index].text)).split()
            car_desc = year + make + model
            price = re.sub("[$,]", "", car_prices[index].text) # remove $ and ',' from the price
            if (not price.isdigit()): # if the price is "Please call" or something non-numeric, set the price to 0
                price = '0'
                zero += 1
            price = price.split() # convert to a list
            stock_num = (stock[index].text[8:]).split() # get the stock # for each car and convert to a list
            link = (details_links[index].get_attribute('href')).split()
            print (index, ":", car_desc, price, stock_num, link)
            car_info.append(dealer_id + car_desc + price + stock_num + link) 
        count = count + index +1
        print ("Running count: ", count)
  
        if count == num_cars: # if the running count == the number of cars displayed, we've got all the pages
            break

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.go-to-page.stat-arrow-next"))) # wait for the Next link
        driver.find_element_by_css_selector("a.go-to-page.stat-arrow-next").click() # click on Next link
        sleep (6)

    print ("Total cars processed: ", count, " Total unpriced cars: ", zero)
                
    car_info = sorted(car_info)
    for index, i in enumerate(car_info):
        print (index, ":", i)
    
    print ("Saving data in a spreadsheet....", file_out)
    CreateDealerSheet(data_out, car_info, date_time)
    print (dealer, "Total cars: " , count)
    data_out.save_file(file_out)
       
    driver.quit() # Close the browser and end the session
