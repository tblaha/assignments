'''
@author: tblaha, davidoort
'''

from math import *

n=600851475143
primes=[2]
i=0

def trivial(m):
    factors=[]
    divisor=2
    while m>1:
        if 0==m%divisor:
            m /= divisor
            factors.append(divisor)
            divisor -= 1
        divisor+=1
    print factors
    print divisor

def primegen(m): ## This (efficiently) generates primes up to the square root of the number to be factorized. Any more is not needed since if there is a prime larger than the sqrt (there can be one, at most), then the number can written as the product of it and a prime lower that the sqrt. This will be dealt with later.
    global primes
    for i in range(2,int(sqrt(sqrt(m)))+2): # davidoort's algorithm generates primes until the sqrt of sqrt the input value. therefore this is O(sqrt(n))
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
        r=int(sqrt(m))/prime + 1
        for j in range(1,r):
            list_non_primes.append(j*prime)

    list_non_primes.sort() # sorting is needed for next step (iterating and inverting). No idea why this is fast as hell, but I like it :D assuming O(logn)

    i=0
    while i<len(list_non_primes): # Inverting the sorted non-prime list to obtain the primes.
        if list_non_primes[i]>primes[len(primes)-1] and (list_non_primes[i]-list_non_primes[i-1]) == 2:
            primes.append(list_non_primes[i]-1)
        i += 1

k=0
factors=[]
def factor(m): # using a recursive function to do the actual factorisation (only finding primes lower than sqrt(n) obviously, since the prime list supplied only goes until sqrt(n)). Counting k to keep track of the steps (if only 1, then highest prime is larger than sqrt(n))
    global primes,k,factors
    for prime in primes:
        if m%prime==0:
            factors.append(prime)
            k+=1
            factor(m/prime)
            break
    return factors

def allfactors(factors,m): ## finds all factors from the list of all factors below sqrt(n)product=1
    product=1
    for factor in factors:
        product *= factor
    if product != m:              # there is a prime larger than sqrt(n)
        divisor=1
        for factor in factors:
            divisor *= factor
        largest = m/divisor
        factors.append(largest)
    return factors

def largest(allfactors,m):
    global k
    if k == 0:                      # m is a prime itself
        largest = m
    else:                           # there are more than two prime factors (all lower sqrt(n)). taking the max
        largest = max(factors)
    return largest

def efficient(m):
    primegen(m)
    factorslist=factor(m)
    allfactorslist=allfactors(factorslist,m)
    largestfactor=largest(allfactorslist,m)

    print factorslist
    print largestfactor

efficient(n)
#trivial(n)
