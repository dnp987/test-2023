'''
Created on Jul. 6, 2022

@author: dpenn
'''
import re
class CarData:
# Remove all leading and trailing spaces from text data, and remove $ and comma from price
    def __init__(self, dealer_id, year, make, model, price, stock_num, link):
        self.dealer_id = dealer_id.strip()
        self.year = year
        self.make = make.strip()
        self.model = model.strip()
        self.price = (re.sub("[$,]", "", price)).strip()
        self.stock_num = stock_num.strip()
        self.link = link.strip()
