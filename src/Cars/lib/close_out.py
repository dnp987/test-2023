'''
Created on Apr 11, 2023

@author: dpenn
'''
from Cars.CreateDealerSheet2 import CreateDealerSheet

def close_out(driver, dealer, count, zero, num_cars, data_out, file_out, date_time, car_info):
    if (count != num_cars):
        print ("Processing error. Number of cars expected: ", num_cars, " Number of cars found: " , count, " Data sheet not created.")
    else:
        print ("Total cars processed: ", count, " Total unpriced cars: ", zero)
        
        car_info = sorted(car_info)
        for index, car in enumerate(car_info):
            print (index, ":", car)
            
        print ("Saving data in a spreadsheet....", file_out)
        CreateDealerSheet(data_out, car_info, date_time)
        print (dealer, "Total cars: " , count)
        data_out.save_file(file_out)
        
    driver.quit() # Close the browser and end the session