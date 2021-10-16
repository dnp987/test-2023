'''
Created on May 4, 2021
Created to handle Mazda make and model so that it becomes: Make: Mazda, Model: Mazda3 or Mazda5 or Mazda6
@author: Home
'''
def mazda_fix(make, model):
    if (make == "Mazda3" or make == "MAZDA3"): # fix up the make and model
        make = "Mazda"
        model.insert(0,"Mazda3")
    if (make == "Mazda5" or make == "MAZDA5"):
        make = "Mazda"
        model.insert(0,"Mazda5")
    if (make == "Mazda6" or make == "MAZDA6"):
        make = "Mazda"
        model.insert(0,"Mazda6")
        
    return make, model