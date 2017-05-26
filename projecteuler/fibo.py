i=0
def fibo(n):
    global i
    i=i+1
    if n==2:
        return 1+fibo(n-1)
    if n==1:
        return 1
    return fibo(n-1)+fibo(n-2)

n=35

print fibo(n)
print i
