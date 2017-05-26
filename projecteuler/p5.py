primes=[2,3,5,7,11,13,17,19]

start=1
for a in primes:
    start *= a

def check(n,start):
    k=0
    for b in range(4,21):
        if n%b == 0:
            k += 1
    if k == 17:
        print n
    else:
        check(n+start,start)

check(start,start)
