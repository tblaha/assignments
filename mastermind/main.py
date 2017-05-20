
from random import *
from library import *


code=sample(range(1,k+1),n)
#code=[4,3,5,2]
#print code

i=0
ingame=True
while ingame:
    user=raw_input("Enter your guess: ")
    userint=[]
    for char in user:
        userint.append(int(char))
    numrightpos=rightpos(code,userint)[0]
    lstrightpos=rightpos(code,userint)[1]
    if numrightpos==n:
        print "You win!"
        break
    if numrightpos:
        print "You have {0} numbers in the correct place. ".format(numrightpos),
    numoccurs=occurs(code,userint,lstrightpos)
    if numoccurs:
        print "You have guessed {0} number(s) correct, but its(their) placement is wrong. ".format(numoccurs)
    else:
        print
    if not numoccurs and not numrightpos:
        print "You have nothing correct..."
    i+=1
    if i >=10:
        print "You lost!"
        ingame=False
