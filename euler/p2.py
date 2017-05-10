a=[1,1]
n=0
while True:
    n=a[-1]+a[-2]
    if n >= 4000000:
        break
    a.append(a[-1]+a[-2])

summ=0
for fibo in a:
    if fibo%2==0:
        summ += fibo

print a
