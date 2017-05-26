from math import *

primes=[2]

def primegen(m): ## This (efficiently) generates primes up to the square root of the number to be factorized. Any more is not needed since if there is a prime larger than the sqrt (there can be one, at most), then the number can written as the product of it and a prime lower that the sqrt. This will be dealt with later.
    global primes
    for i in range(2,int(sqrt(m))+1): # davidoort's algorithm generates primes until the sqrt of sqrt the input value. therefore this is O(sqrt(n))
        count=0                             # this is only done until sqrt(sqrt n) because the sieve of eratosthenes only needs sqrt(n) input primes.
        for prime in primes:
            if i%prime == 0:
                break
            else:
                count += 1
        if count == len(primes):
            primes.append(i)

    list_non_primes=[]                      # Sieve of eratosthenes: generate a list of non primes by multiplying every prime until sqrt(sqrt(n)) by range(1,sqrt(n)/prime). This way obtain all non primes until sqrt(n).
    for prime in primes:
        r=int(m)/prime + 1 ## no idea why +3, but that seems to work all the time...
        for j in range(1,r):
            list_non_primes.append(j*prime)

    list_non_primes.sort() # sorting is needed for next step (iterating and inverting). No idea why this is fast as hell, but I like it :D assuming O(logn)

    i=0
    while i<len(list_non_primes): # Inverting the sorted non-prime list to obtain the primes.
        if list_non_primes[i]>primes[len(primes)-1] and (list_non_primes[i]-list_non_primes[i-1]) == 2:
            primes.append(list_non_primes[i]-1)
        i += 1

    print sum(primes)
    #print list_non_primes

primegen(2000000)


