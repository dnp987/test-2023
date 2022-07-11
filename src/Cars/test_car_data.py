'''
Created on Jul. 6, 2022

@author: dpenn
'''
from Cars.car_data import CarData
if __name__ == '__main__':
    def print_car_data(data):
        print(data.dealer_id, " " , data.year, " ", data.make, " ", data.model, " " , data.price," " , data.stock_num, " ", data.link) 
    
    TestData = []
    
    used_car1 = CarData("   ID1", "1997", "  Ford  ", "    Taurus    ", "   $17,999    ", "   abc123   ", "   https://google.com    ")
    used_car2 = CarData("   ID2 ", "2017", "  GM  ", "    Impala    ", "   please call    ", "   def456   ", "   https://google.com    ")
    used_car3 = CarData(" ABC123 ", "1996", "Toyota", "Corola", "$13,299 ", "defkas789sds", "https://toyota.ca")
    used_car3.dealer_id = " DEF456 "       
    
    TestData.append(used_car1)
    TestData.append(used_car2)
    TestData.append(used_car3)
    
    for count, obj in enumerate(TestData):
        print_car_data(obj)
