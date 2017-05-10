n=1000
summ=0
for a in range(1,n):
    if a%3 == 0 or a%5 == 0:
        summ += a

print summ
