'''
Created on Jul 17, 2020

@author: Home
'''
import re
 
a = 'abc def ghi xyz'
print (len(a), a)
print (a[0:3])
b = a.split()
print (len(b), b)
for index, i in enumerate(a):
    print (index, ":", i)
for index, i in enumerate(b):
    print (index, ":", i)
    
print (b[1:3])

x = ['2019', 'Mazda', '3', 'GX']

print (x)
print (x[2:4])