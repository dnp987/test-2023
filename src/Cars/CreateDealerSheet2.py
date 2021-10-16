'''
Created on Jul 3, 2020

@author: Home
'''
def CreateDealerSheet(SheetOut, car_info,date_time):
    for row_index, car_line in enumerate(car_info, start = 1):
        for col_index, car_item in enumerate(car_line, start = 1):
            SheetOut.set_cell(row_index, col_index, car_item, "Arial", False, 10 )
            
    #SheetOut.set_cell(row_index+2, 1, ("Prices as of: " + date_time), "Arial", False, 10)