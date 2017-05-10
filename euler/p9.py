from math import *

triplets=[]

for a in range(1,500):
    for b in range(a,500):
        c_round=int(sqrt(a*a+b*b)+0.5)
        if c_round*c_round == a*a+b*b:
            triplets.append([a,b,c_round])

for d in triplets:
    if d[0]+d[1]+d[2] == 1000:
        print d[0]*d[1]*d[2]
