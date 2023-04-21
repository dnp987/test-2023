'''
Created on Jun 4, 2020

@author: Home
'''
# -*- coding: utf-8 -*-
import re
from builtins import len

a = "abc   def ghi   x yz"
print (a, len(a))
a = a.split(" ", 1)
for i in a:
    print (i)
    
x = "$12,345"
y = x.strip("$")
a = "$1,234"
b = "1234"
c = "abc0"
print (x, "testing x for no spaces: " , not x.isspace())
print (x, "testing x is numeric: ", x, " ", x.isnumeric())
print (y, "testing y is numeric: ", y, " ", y.isnumeric())
print (a, "testing a is alpha:", a, " ", a.isalpha())
print (a, "testing a is digits:", a, " ", a.isdigit())
print (a, "testing a is digits:", a, " ", a.isnumeric())
print (b, "testing b is digits: ", b, " ", b.isdigit())

print(x, "remove characters from x: ", re.sub("[^0-9]", "", x))
print(x, "remove digits from x: ", re.sub("[0-9]", "", x))
print(a, "remove $ from a: ", re.sub("[$,]", "", a))
print(a, "remove digits from a: ", re.sub("[^$,]", "", a))

w = "Contact us for price"
v = re.sub("[^0-9]", "", w)
print (w, v, len(v))

x = 2
y = 3
print (x, y, "Floor divide, rounded down", x//y)
print (x, y, "Modulus, remainder of division", x%y)
z = y//x
if (y%x):
    z +=1
print (z)

print (type (a))
print (type (x))

z = "0"
if int(z) == 0:
    print ("z is 0")
    
print (ascii('»')) #get the ascii of '»' right arrow for next page
print ('\xbb')
print (ascii('«')) #get the ascii of '«' left arrow for previous page
print ('\xab')
stop = 4
for i in range(2, (stop+1)):
    print (i)

'''
# this code finds all of the css properites of an element

properties = driver.execute_script('return window.getComputedStyle(arguments[0], null);', element)
for temp in properties:
        print(temp, " : ", element.value_of_css_property(temp)
'''