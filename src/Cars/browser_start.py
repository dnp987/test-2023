'''
Created on May 11, 2021

@author: Home
'''
from selenium import webdriver

def browser_start(url, headless = False):
    browser = "C:\\Selenium\\chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    
    if headless: # if we're running headless
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("headless")
        chrome_options.add_argument('window-size=1920x1080');
    else: # if running full browser, do it in incognito mode so that it doesn't save history
        #chrome_options.add_argument("--incognito")
        chrome_options.add_argument("incognito")
                
    driver = webdriver.Chrome(browser, options = chrome_options) # Open Chrome
    driver.maximize_window() # maximize the browser window
    driver.get(url) # Navigate to the test website
    
    return driver