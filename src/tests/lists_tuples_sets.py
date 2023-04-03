a = ['apple', 'orange', 'banana', 'grape']
print (a.count('apple'))
print (a.index('apple'))
a.append('pear')
print (a, len(a))
a.reverse()
print (a, len(a))
a.sort()
print (a, len(a))
a.pop()
print (a, len(a))
b = a
print (b)
b[1] ="red"
print (b)

t = (1234, 5678, 'hello')
print (t[0])
#t[1] = 777
print (t)

set1 = {'apple', 'orange', 'banana'}
print (set1)
print ('grape' in set1)