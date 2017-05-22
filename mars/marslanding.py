import numpy as np
from math import *





def worldtoscreen(worldcoordinates):
    xworld,yworld=worldreso
    xscreen,yscreen=screenreso
    xworldcoord,yworldcoord=worldcoordinates
    xscreencoord=int(xworldcoord/xworld*xscreen+0.5)
    yscreencoord=yscreen-int(yworldcoord/yworld*yscreen + 0.5)
    screencoordinates=(xscreencoord,yscreencoord)
    return screencoordinates

def marstoscreen(marscoordinates):
    xworld,yworld=worldreso
    xscreen,yscreen=screenreso
    xmarscoord,ymarscoord=marscoordinates
    xscreencoord=int(xmarscoord/xworld*xscreen+0.5) + int(margin*xscreen+0.5)
    xscreencoord=int((margin*xworld/(1+2*margin) + xmarscoord)* xscreen/xworld + 0.5)
    yscreencoord=int(yscreen-(margin*yworld/(1+2*margin) + ymarscoord)* yscreen/yworld + 0.5)
    screencoordinates=(xscreencoord,yscreencoord)
    return screencoordinates

def getrho(P):
    i=0
    while P[1] >= atmos['alt'][i+1]:
        i += 1
    return (atmos['rho'][i]-atmos['rho'][i+1])/(atmos['alt'][i]-atmos['alt'][i+1]) * (P[1]-atmos['alt'][i]) + atmos['rho'][i]

def getme(V,m,P):
    if m>m_dry and P[1]<alt_fire and P[1]>alt_off:
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
    from matplotlib import pyplot as plt
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
    sc.plot(results['t'],results['Py'])
    sc.set_title('Altitude over time')
    #plt.gca().invert_xaxis()

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

def animate():
    import pygame as pg
    pg.init()
    pg.font.init()
    myfont = pg.font.SysFont('monospace', 11)
    
    scale=0.03
    nextsample=0.0
    timefactor=5.
    fps=24
    step=1./(timefactor*fps)
    
    xscreen,yscreen=screenreso
    screen=pg.display.set_mode(screenreso)
    scrrect=screen.get_rect()
    black=(0,0,0)
    
    noflame_orig = pg.image.load("sprites/lander_noflame.png")
    flame_orig   = pg.image.load("sprites/lander_flame.png")
    
    clock = pg.time.Clock()
    
    while True:
        simtime = 0.001*pg.time.get_ticks() # abs time in ms since init was called
        if simtime*timefactor >= results['t'][-1]:
            raw_input("Press Enter!")
            break
        
        if simtime*timefactor >= nextsample:
            print simtime
            nextsample += step
            i=0
            while results['t'][i]<=simtime*timefactor:
                i+=1
            pg.draw.rect(screen,black,scrrect)
            
            if results['me'][i]:        
                flame     = pg.transform.rotozoom(flame_orig,90+results['gamma'][i],scale)
                flamerect = flame.get_rect()
            
                flamerect.center=marstoscreen((results['Px'][i],results['Py'][i]))
                screen.blit(flame,flamerect)
            else:
                noflame     = pg.transform.rotozoom(noflame_orig,90+results['gamma'][i],scale)
                noflamerect = noflame.get_rect()
            
                noflamerect.center=marstoscreen((results['Px'][i],results['Py'][i]))
                screen.blit(noflame,noflamerect)
            
            currentfps=clock.get_fps()
            label = myfont.render('Alt: {0:07.1f} m    | Horiz. Pos.: {1:05.0f} m | Vert. Speed: {2:04.0f} m/s | Horiz. Speed: {3:03.0f} m/s'.format(results['Py'][i],results['Px'][i],results['Vy'][i],results['Vx'][i]), False, (255, 255, 255))
            label2= myfont.render('Angle: {0:05.1f} deg  | Mass Flow: {1:0.2f} kg/s | Fuel mass: {2:05.2f} kg   | Sim. time: {3:02.0f} s'.format(-results['gamma'][i],results['me'][i],results['mfuel'][i],results['t'][i]), False, (255, 255, 255))
            fpslabel= myfont.render('fps: {0:.2f}'.format(currentfps), False, (255, 255, 255))
            screen.blit(label, (xscreen*0.01,yscreen*0.96))
            screen.blit(label2,(xscreen*0.01,yscreen*0.98))
            screen.blit(fpslabel,(xscreen*0.01,yscreen*0.01))
            
            pg.display.flip()
            clock.tick(fps)                  # limit fps
        
    pg.quit()
    
    
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


#-------------------------------------------------------------------
# Begin of program
#-------------------------------------------------------------------


# params:
alt_off=0.3 #m
v_target=-2. #m/s
throttle=0.05
m_fuel=67. #kg
alt_fire=1750. #m

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
        results['V']    .append((V[0]**2+V[1]**2)**0.5)
        results['Vx']   .append(V[0])
        results['Vy']   .append(V[1])
        results['gamma'].append(gamma)
    
    if P[1] <= 0:
        print "Touchdown at {0} m/s vertical speed, {1} m/s horizontal speed, angle {2} deg and {3} kg of fuel left after {4} s have passed".format(results['Vy'][-1],results['Vx'][-1], results['gamma'][-1], results['mfuel'][-1],results['t'][-1])
        condition=False

makeplots()
margin=0.1
worldreso=((1+2*margin)*results['Px'][-1],(1+2*margin)*results['Py'][0])
screenreso=(650,int(results['Py'][0]/results['Px'][-1] * 650. + 0.5))
#animate()
