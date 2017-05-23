import numpy as np
from math import *

#constants
g0 = 3.711   # m/s^2  | mean sea level gravity on mars
R  = 191.84  # J/kg/K | gas constant

#vehicle constants
me_max = 5.    # kg/s | Maximum engine mass flow
ve     = 4400. # m/s  | Relative exhaust velocity 
CdS    = 4.92  # m^2  | Frontal area times drag coefficient (see getD(V,P))
m_dry  = 699.  # kg   | S/C dry mass

#Initialisation
t=0.0 # s | current simulation time

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

def animate():
    #----------------------------------------------#
    #-----initialisation stuff and definitions-----#
    #----------------------------------------------#
    import pygame as pg                           # Import the package only when needed, so it is not loaded when animate() is not even called
    pg.init()                                     # Initialise pygame (has no visual effect)
    pg.font.init()                                # Initialise the font stuff for labels
    myfont = pg.font.SysFont('monospace', 11)     # define a monospace font
    
    scale=0.025                                   # -   | used as a scale for the lander sprites
    nextsample=0.0                                # s   | will hold the time since pg.init() for when the next frame that has to be drawn
    fps=24                                        # 1/s | will be used to limit the amount of frames drawn per second (so less CPU usage)
    step=1./(timefactor*fps)                      # s   | time interval between drawing two frames
    currentfps=0.                                 # 1/s | will hold the actual fps count
    
    screen=pg.display.set_mode(screenreso)        # I think this actually opens a window with the resolution defined at the end of this file
    xscreen,yscreen=screenreso                    # px  | screenresolution
    scrrect=screen.get_rect()                     # this gets the screen rectangle. I understand a rect as the geometric basis for the screen surface that 
                                                  # can be used to read or assign values (like position and size)
    black=(0,0,0)
    
    noflame_orig = pg.image.load("sprites/lander_noflame.png") # load the landersprites as objects
    flame_orig   = pg.image.load("sprites/lander_flame.png")
    
    clock = pg.time.Clock()                       # initialise the clock (will be used to monitor/limit fps)
    
    while True:
        simtime = 0.001*pg.time.get_ticks()*timefactor         # s | time since pg.init() was called, streched with the timefactor
        if simtime >= results['t'][-1]:                        # if exceeds mission time
            raw_input("Press Enter!")                             # --> freeze the screen
            break
        
        if simtime >= nextsample:                              # if next sample should be drawn
            nextsample += step                                    # --> reset nextsample
            i=0
            while results['t'][i]<=simtime:                    # get relevant position in results dict
                i+=1
                
            #-----------------------#
            #----animation stuff----#
            #-----------------------#
            pg.draw.rect(screen,black,scrrect)                                             # clear the screen every frame
            
            if results['me'][i]:                                                           # ---if engine active---
                                                                                              # --> draw the flame sprite
                flame     = pg.transform.rotozoom(flame_orig,90+results['gamma'][i],scale) # import the sprite as an oriented and scaled surface that needs 
                                                                                           # to be projected ("blitted") onto the screen surface guided by  
                                                                                           # a rect() that holds its position.
                
                flamerect = flame.get_rect()                                               # again, get the current position and size of the surface rect()
                
                flamerect.center=marstoscreen((results['Px'][i],results['Py'][i]))         # modify position of the rect() by converting mars coordinates
                                                                                           # (actual distances) to screen coordinates (see bottom of file)
                
                screen.blit(flame,flamerect)                                               # blit it to the screen (note: this doesnt update the screen yet)
                
            else:                                                                          # ---same for no-flame sprite if not firing thrusters--- #
                noflame     = pg.transform.rotozoom(noflame_orig,90+results['gamma'][i],scale)
                
                noflamerect = noflame.get_rect()
                noflamerect.center=marstoscreen((results['Px'][i],results['Py'][i]))
                
                screen.blit(noflame,noflamerect)
            
            #-------------------#
            #----label stuff----#
            #-------------------#
            # label = myfont.render('text', antialising, color)
            label = myfont.render('Alt: {0:07.1f} m    | Horiz. Pos.: {1:05.0f} m | Vert. Speed: {2:04.0f} m/s | Horiz. Speed: {3:03.0f} m/s'.format(results['Py'][i],results['Px'][i],results['Vy'][i],results['Vx'][i]), False, (255, 255, 255))
            label2= myfont.render('Angle: {0:05.1f} deg  | Mass Flow: {1:0.2f} kg/s | Fuel mass: {2:05.2f} kg   | Sim. time: {3:02.0f} s'.format(-results['gamma'][i],results['me'][i],results['mfuel'][i],results['t'][i]), False, (255, 255, 255))
            fpslabel= myfont.render('fps: {0:.2f}'.format(currentfps), False, (255, 255, 255))
            screen.blit(label, (xscreen*0.01,yscreen*0.96))   # blit them to the screen guided by a very simple rect()
            screen.blit(label2,(xscreen*0.01,yscreen*0.98))   # rect() in these cases is just tuple indicating the position of the left upper corner
            screen.blit(fpslabel,(xscreen*0.01,yscreen*0.01))

            #--------------------# note: this has no effect on the actual simulation timing (so if realtime or not)
            #----timing stuff----#       because pg.time.get_ticks() is an absolute measure of the time passed.
            #--------------------#       --> this just reduces CPU load
            currentfps=clock.get_fps()                                 # 1/s | gets fps by averaging last 10 calls to clock.tick()
            clock.tick(fps)                                            # limit fps. Not sure how this works precisely, but it seems to...
            
            #------------------------------------------------------------------------------------------#
            #----finally update the screen with all changes made in the iteration of the while loop----#
            #------- that was: reset the screen (by coloring a rect() in black)  ----------------------#
            #-------           draw the lander in its current state and position ----------------------#
            #-------           draw the labels                                   ----------------------#
            #------------------------------------------------------------------------------------------#
            pg.display.flip()
        
    pg.quit() # close the window

    
atmos={'alt':[],'temp':[],'rho':[],'a':[],'p':[]}
with open('data/mars.txt','r') as atmosfile:
    lines=atmosfile.readlines()
    for line in lines:
        line.replace('\n','')
        if line[0] != '*' and not line.strip()=="":
            words = line.split()
            atmos['alt'].append(float(words[0])*1000)             # m      | altitude over sea level
            atmos['temp'].append(float(words[1]))                 # K      | temperature
            atmos['rho'].append(float(words[2]))                  # kg/m^3 | density
            atmos['a'].append(float(words[3]))                    # m/s    | speed of sound
            atmos['p'].append(float(words[2])*R*float(words[1]))  # N/m^2  | pressure (computed, not read from file)


#-------------------------------------------------------------------
# Begin of program
#-------------------------------------------------------------------

# params:
ts       = 0.01  # s   | time step per frame in simulation
m_fuel   = 70.   # kg  | initial fuel on board
alt_fire = 1770. # m   | Altitude to fire thrusters
alt_off  = 0.3   # m   | Thruster cut-off altitude
v_target = -2.   # m/s | Target velocity (see getme(V,m,P))
throttle = 0.05  # -   | factor in throttling law (see getme(V,m,P))

# Initial conditions
gamma  = radians(-20.)         # rads | angle of S/C with horizontal
V_init = 262.                  # m/s  | initial speed
P      = np.array([0.,20000.]) # m    | Position vector

m      = m_dry + m_fuel                                 # kg  | Total mass 
V      = np.array([np.cos(gamma),np.sin(gamma)])*V_init # m/s | Velocity vector



results={'t':[],'mfuel':[],'me':[],'Px':[],'Py':[],'V':[],'Vx':[],'Vy':[],'gamma':[]} # results dictionary, very important :)
condition = True
while condition:
    F=getD(V,P)+getT(V,m,P)+np.array([0.,-1.])*g0*m  # N     | vectorial sum of all forces
    
    gamma=degrees(-(atan2(V[0],V[1])-np.pi/2))       # deg   | compute current angle from velocity vector (for user output and animation, avoided for computation)
    a=F/m                                            # m/s^2 | acceleration vector
    me = getme(V,m,P)                                # kg/s  | propellant mass flow
    m -= me*ts                                       # kg    | new total mass
    V += a*ts                                        # m/s   | new velocity vector
    P += V*ts                                        # m     | new position vector
    t += ts                                          # s     | new time
        
    if not int(t*100)%10:                            # Append to results dict 10 times per second
        results['me']   .append(me)
        results['t']    .append(t)
        results['mfuel'].append(m-m_dry)
        results['Px']   .append(P[0])
        results['Py']   .append(P[1])
        results['V']    .append((V[0]**2+V[1]**2)**0.5)
        results['Vx']   .append(V[0])
        results['Vy']   .append(V[1])
        results['gamma'].append(gamma)
    
    if P[1] <= 0:                                    # Touchdown?
        print "\n***Simulation parameters***\n   {0:0.0f} m     firing altitude\n   {1} kg    fuel onboard".format(alt_fire,m_fuel)
        print "\n***Touchdown simulated to occur at***\n  {0:0.2f} m/s   vertical speed\n   {1:0.2f} m/s   horizontal speed\n  {2:0.1f} deg   angle with the horizontal\n   {3:0.2f} kg    of fuel left\n   {4:0.0f}  s     elapsed".format(results['Vy'][-1],results['Vx'][-1], results['gamma'][-1], results['mfuel'][-1],results['t'][-1])
        condition=False

margin=0.1                                                               # -  | margin fraction in animation window
xscreenwidth=650                                                         # px | static width of screen
worldreso=((1+2*margin)*results['Px'][-1],(1+2*margin)*results['Py'][0]) # m  | dynamic world coordinate system 
screenreso=(650,int(results['Py'][0]/results['Px'][-1] * 650. + 0.5))    # px | dynamic screen coordinates

#
#                Screen:
#             
#|-------------------------------------|
#|       World coordinate box          |
#|      with margins all around        |
#|  Py|--------------------------|     |
#| max|                          |     |
#|    |    Mars coordinate box   |     |
#|    |      where the s/c       |     |
#|    |     will be animated     |     |
#|    |                          |     |
#|    |                          |     |
#|  0m|--------------------------|     |
#|    0m                       Px_max  |
#|    -space for labels and stuff-     |
#|-------------------------------------|
#

timefactor=3.                                 # -   | stretching time 
print "\n***Close plot window to start animation of the results with timefactor {0:0.0f}***\n".format(timefactor)
makeplots()
animate()

