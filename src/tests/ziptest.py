'''
Created on Mar 31, 2023

@author: dpenn
'''

a = (1, 2, 3)
b = (4, 5, 6)
c = (7, 8, 9)

for index, (aa, bb,cc) in enumerate (zip(a, b, c)):
    print (index, aa, bb, cc)
    

x = 'x'
while (x == 'x'):
    print ("x is 'x'")
    x = x + 'x'
    continue
print ("x is no longer 'x'")
print (x)
