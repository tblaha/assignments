array=[]

for a in range(1000,100,-1):
    for b in range(1000,100,-1):
        number=str(a*b)
        k=0
        for i in range(0,len(number)/2):
            if number[i]==number[-1-i]:
                k+=1
        if k == len(number)/2:
            array.append(int(number))

print max(array)
