'''
Created on Jul. 6, 2022

@author: dpenn
'''
from Cars.car_data import CarData
if __name__ == '__main__':
    def print_car_data(data):
        print(data.dealer_id, " " , data.year, " ", data.make, " ", data.model, " " , data.price," " , data.stock_num, " ", data.link) 
    
    TestData = []
    
    used_car1 = CarData("   ID1", 1997, "  Ford  ", "    Taurus    ", "   $17,999    ", "   abc123   ", "   https://google.com    ")
    print_car_data(used_car1)
    
    used_car2 = CarData("   ID2 ", 2017, "  GM  ", "    Impala    ", "   $21,359    ", "   def456   ", "   https://google.com    ")
    print_car_data(used_car2)
    
    TestData.append(used_car1)
    TestData.append(used_car2)
    
    for obj in TestData:
        print_car_data(obj)
