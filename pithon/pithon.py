from math import *
import datetime
import time
from os import system
from pilibrary import *


with open('scores.txt','a') as scoresfile:
    abc=1
    
with open('scores.txt','r') as scoresfile:
    scores=scoresfile.readlines()
    scoreslist=[]
    for line in scores:
        if line != "\n":
            words=line.split(' | ')
            words[-1]=words[-1].replace('\n','')
            scoreslist.append(words)
scoreslist.sort(key=lambda x:x[1], reverse=True)


username=raw_input('Enter your name:')
try:
    scoreslist[0][1]
    print "The leader is currently '{0}' with a score of {1} set on {2}. Can you beat it?!".format(scoreslist[0][0],scoreslist[0][1],scoreslist[0][2])
    dummy=raw_input('Press Enter!')
except IndexError:
    scoreslist=[]
    
print "Here we check your currently level of skills!"
basepi=raw_input('Please enter as many digits of pi as you know:')

basescore=score(len(basepi),basepi)
print "Score: {0}".format(basescore-2)





#------------------------------
# Start of iterative process
#------------------------------


current=basescore
while True:
    show(current+1)
    user=raw_input("Enter what you have seen!")
    if not user or score(current+1,user) != current+1:
        break
    current += 1
    

i=0
for line in scoreslist: # get rank
    if current-2 > int(line[1]):
        if i==0:
            print "You got the new highscore!! Well done: {0}".format(current-2)
            break
        else:
            print "You are on position {0} of the leader board. Score: {1}".format(i+1,current-2)
            break
    i+=1
    
if not len(scoreslist):
    print "You did get the new highscore, but well, you're the first to ever play this game... Score: {0}".format(current-2)
    
if i==len(scoreslist) and i != 0:
    print "You're on the last place of the leader board........... Score: {0}".format(current-2)



with open('scores.txt','a') as scoresfile:
    scoresfile.write('{0} | {1} | {2}\n'.format(username,current-2,datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))


   
