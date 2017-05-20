import pygame
import numpy as np
from math import *
from matplotlib import pyplot as plt

#pygame.init()
#worldreso=(1.,0.75)
#reso=(600,450)
#screen=pygame.display.set_mode(reso)

#def convert(worldcoordinates):
    #xworld,yworld=worldreso
    #xscreen,yscreen=reso
    #xworldcoord,yworldcoord=worldcoordinates[0],worldcoordinates[1]
    #xscreencoord=round(xworldcoord/xworld*xscreen)
    #yscreencoord=round(yworldcoord/yworld*yscreen)
    #screencoordinates=np.array([xscreencoord,yscreencoord])
    #return screencoordinates

#pygame.quit()


def getrho(P):
    i=0
    while P[1] >= atmos['alt'][i+1]:
        i += 1
    return (atmos['rho'][i]-atmos['rho'][i+1])/(atmos['alt'][i]-atmos['alt'][i+1]) * (P[1]-atmos['alt'][i]) + atmos['rho'][i]

def getme(V,m,P):
    if m>m_dry and P[1]<alt_fire:
        me=m*g0/ve +throttle*(v_target-V[1])
        return min(me,me_max)
    else:
        return 0.

def getT(V,m,P):
    T= - V/sqrt(np.dot(V,V)) * getme(V,m,P) * ve
    if (v_target-V[1]):
        return T
    else:
        return 0.

def getD(V,P):
    D=-V*sqrt(np.dot(V,V))*0.5*getrho(P)*CdS
    return D

def makeplots():
    plt.close('all')
    fig = plt.figure()

    sc = fig.add_subplot(2,3,1)
    sc.plot(results['Px'],results['Py'])
    sc.set_title('Trajectory')

    sc = fig.add_subplot(2,3,2)
    sc.plot(results['Py'],results['Vy'])
    sc.set_title('Vertical speed over alt')
    plt.gca().invert_xaxis()

    sc = fig.add_subplot(2,3,3)
    sc.plot(results['Py'],results['Vx'])
    sc.set_title('Horizontal speed over alt')
    plt.gca().invert_xaxis()

    sc = fig.add_subplot(2,3,4)
    sc.plot(results['Py'],results['gamma'])
    sc.set_title('Angle over alt')
    plt.gca().invert_xaxis()

    sc = fig.add_subplot(2,3,5)
    sc.plot(results['Py'],results['me'])
    sc.set_title('Exhaust mass flow over alt')
    plt.gca().invert_xaxis()

    sc = fig.add_subplot(2,3,6)
    sc.plot(results['Py'],results['mfuel'])
    sc.set_title('Fuel mass over alt')
    plt.gca().invert_xaxis()

    fig.tight_layout()
    plt.show()

atmos={'alt':[],'temp':[],'rho':[],'a':[]}
with open('data/mars.txt','r') as atmosfile:
    lines=atmosfile.readlines()
    for line in lines:
        line.replace('\n','')
        if line[0] != '*' and not line.strip()=="":
            words = line.split(" ")
            atmos['alt'].append(float(words[0])*1000)
            atmos['temp'].append(float(words[1]))
            atmos['rho'].append(float(words[2]))
            atmos['a'].append(float(words[3]))
    

# params:
alt_off=0.3 #m
v_target=-2. #m/s
throttle=0.05
m_fuel=90. #kg
alt_fire=1900. #m

#constants
g0=3.711 # m/s^2

#vehicle constants
me_max=5. #kg/s
ve=4400. # m/s
CdS=4.92 # m^2
m_dry=699. #kg

#simulation and initial conditions
ts=0.01 #s
t=0.0 #s
gamma=radians(-20.) #rads
V_init=262. #m/s
P=np.array([0.,20000.]) # m

m = m_dry + m_fuel #kg
V=np.array([np.cos(gamma),np.sin(gamma)])*V_init # m/s as 2d vector
t=0.

results={'t':[],'mfuel':[],'me':[],'Px':[],'Py':[],'V':[],'Vx':[],'Vy':[],'gamma':[]}
condition = True
while condition:
    F=getD(V,P)+getT(V,m,P)+np.array([0.,-1.])*g0*m
    #F=getD(V,P)+np.array([0.,-1.])*g0*m
    #print getme(V,m,P),getT(V,m,P)
    
    gamma=degrees(-(atan2(V[0],V[1])-np.pi/2))
    a=F/m
    me = getme(V,m,P)
    m -= me*ts
    V += a*ts
    P += V*ts
    t += ts
        
    #print F,a
    if not int(t*100)%10:
        results['me']   .append(me)
        results['t']    .append(t)
        results['mfuel'].append(m-m_dry)
        results['Px']   .append(P[0])
        results['Py']   .append(P[1])
        results['V']   .append((V[0]**2+V[1]**2)**0.5)
        results['Vx']   .append(V[0])
        results['Vy']   .append(V[1])
        results['gamma']   .append(gamma)
    
    if P[1] <= alt_off:
        condition=False

makeplots()
