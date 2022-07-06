'''
Created on Jul. 6, 2022

@author: dpenn
'''
from Cars.car_data import CarData
if __name__ == '__main__':
    used_car = CarData("   ID1", 1997, "  Ford  ", "    Taurus    ", "   $17,999    ", "   abc123   ", "   https://google.com    ")
    print(used_car.dealer_id)
    print(used_car.year)
    print(used_car.make)
    print(used_car.model)
    print (used_car.price)
    print(used_car.stock_num)
    print(used_car.link)
