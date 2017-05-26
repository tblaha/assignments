sumofsquares=0
sum1=0
for a in range(1,101):
    sumofsquares += a*a
    sum1 += a

squareofsum = sum1*sum1
print squareofsum-sumofsquares
