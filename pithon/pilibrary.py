from sys import stdout
from time import sleep
from random import randint
from os import system

t=5

with open('pi','r') as pifile:
    pi = pifile.read()
    pi = pi.replace('\n','')

def score(n,user):
    i=0
    done=False
    while i<min(n,len(user)):
        if user[i]!=pi[i]:
            break
        i+=1
    return i

def show(n):
    global pi
    global t
    for i in range(t,0,-1):
        stdout.write("\r{0} {1}".format(i,pi[0:n]))
        stdout.flush()
        sleep(1)
    stdout.write("\r\r\r\r {0} \n".format("3." + (n-2) * "*"))
    system('clear')

