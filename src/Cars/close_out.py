'''
Created on Apr 11, 2023

@author: dpenn
'''
from Cars.CreateDealerSheet2 import CreateDealerSheet

def close_out(driver, dealer, count, num_cars, data_out, file_out, date_time, car_info):
    if (count != num_cars):
        print ("Processing error. Number of cars expected: ", num_cars, " Number of cars found: " , count, " Data sheet not created.")
    else:
        print ("Saving data in a spreadsheet....", file_out)
        CreateDealerSheet(data_out, car_info, date_time)
        print (dealer, "Total cars: " , count)
        data_out.save_file(file_out)
        
    driver.quit() # Close the browser and end the session