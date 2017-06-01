from numpy import *



W = [array([-1.,1.,1.,1.]),array([5.,-7.,-1.,-3.]),array([5.,2.,5.,-4.])]
O = []

i=0
while i < len(W):
    y = W[i]
    for a in range(i):
        y -= dot(W[i],O[a])/dot(O[a],O[a]) * O[a]
    O.append(y)
    i+=1

print O
