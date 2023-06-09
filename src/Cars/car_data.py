'''
Created on Jul. 6, 2022

@author: dpenn
'''
import re
class CarData():
# Remove all leading and trailing spaces from text data, and remove $ and comma from price
    def __init__(self, dealer_id, year, make, model, price, stock_num, link):
        self.dealer_id = (dealer_id.strip()).split()
        self.year = year.split()
        self.make = (make.strip()).split()
        self.model = (model.strip()).split()
        self.price = (re.sub("[$,]", "", price)).strip()
        if (not self.price.isdigit()): # if the price is "Please call" or something non-numeric, set the price to 0
            self.price = '0'.split()
        else:
            self.price = self.price.split()
        self.stock_num = (stock_num.strip()).split()
        self.link = (link.strip()).split()
