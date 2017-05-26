import pygame as pg
import numpy as np
from math import *
import random as rd

screensize=(600,600)
worldreso=(1.,1.)
radius=7
damping=1-1E-5

def worldtoscreen(worldcoordinates):
    xworld,yworld=worldreso
    xscreen,yscreen=screensize
    xworldcoord,yworldcoord=worldcoordinates
    xscreencoord=int(xworldcoord/xworld*xscreen+0.5)
    yscreencoord=yscreen-int(yworldcoord/yworld*yscreen + 0.5)
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
    
    #scale=0.025                                   # -   | used as a scale for the lander sprites
    #nextsample=0.0                                # s   | will hold the time since pg.init() for when the next frame that has to be drawn
    fps=400.                                       # 1/s | will be used to limit the amount of frames drawn per second (so less CPU usage)
    #step=1./(timefactor*fps)                      # s   | time interval between drawing two frames
    #currentfps=0.                                 # 1/s | will hold the actual fps count
    
    screen=pg.display.set_mode(screensize)        # I think this actually opens a window with the resolution defined at the end of this file 
    scrrect=screen.get_rect()                     # this gets the screen rectangle. I understand a rect as the geometric basis for the screen surface that 
                                                  ## can be used to read or assign values (like position and size)
    black=(0,0,0)
    white=(255,255,255)
    
    #noflame_orig = pg.image.load("sprites/lander_noflame.png") # load the landersprites as objects
    #flame_orig   = pg.image.load("sprites/lander_flame.png")
    
    clock = pg.time.Clock()                       # initialise the clock (will be used to monitor/limit fps)
    
    nump=20
    basemass=50
    G=5E-3
    ps={'m':[],'V':[],'p':[]}
    for a in range(nump): # setting up initial conditions
        ps['m'].append(rd.random())
        ps['V'].append(np.array([rd.random(),rd.random()]) * 0.3)
        ps['p'].append(np.array([rd.random(),rd.random()]))
    #print ps['V']
    
    xscreen,yscreen=screensize                    # px  | screensizelution
    
    dt=1/fps
    while True:
        pg.draw.rect(screen,black,scrrect)
        for a in range(nump):
            if a >= nump:
                break
            for b in range(nump):
                if b != a:
                    ps['V'][a] += G*ps['m'][b]/(np.dot(ps['p'][b]-ps['p'][a],ps['p'][b]-ps['p'][a])**1.5) * (ps['p'][b]-ps['p'][a]) * dt
                    ps['V'][a] *= damping
                    if np.dot(ps['p'][a]-ps['p'][b],ps['p'][a]-ps['p'][b]) < 0.001:
                        print "deleted:", a,b
                        if ps['m'][b] > ps['m'][a]:
                            ps['m'][b] += ps['m'][a]
                            del ps['m'][a]
                            del ps['V'][a]
                            del ps['p'][a]
                        else:
                            ps['m'][a] += ps['m'][b]
                            del ps['m'][b]
                            del ps['V'][b]
                            del ps['p'][b]
                        nump -= 1
                        break
            if a >= nump:
                break
            ps['p'][a] += ps['V'][a] * dt
            if ps['p'][a][0] < 0. or ps['p'][a][0] > 1.:
                ps['V'][a][0] *= -1
            if ps['p'][a][1] < 0. or ps['p'][a][1] > 1.:
                ps['V'][a][1] *= -1
            pg.draw.circle(screen, white, worldtoscreen(ps['p'][a]), int((ps['m'][a])**(1/3.)*radius))
        #break
        #print ps['V']
        #print ps
        #flamerect = flame.get_rect()                                               # again, get the current position and size of the surface rect()
        
        #flamerect.center=marstoscreen((results['Px'][i],results['Py'][i]))         # modify position of the rect() by converting mars coordinates
                                                                                    ## (actual distances) to screen coordinates (see bottom of file)
        
        #screen.blit(flame,flamerect)                                               # blit it to the screen (note: this doesnt update the screen yet)
        
    
        
        #--------------------# note: this has no effect on the actual simulation timing (so if realtime or not)
        #----timing stuff----#       because pg.time.get_ticks() is an absolute measure of the time passed.
        #--------------------#       --> this just reduces CPU load
        currentfps=clock.get_fps()                                 # 1/s | gets fps by averaging last 10 calls to clock.tick()
        clock.tick(fps)                                            # limit fps. Not sure how this works precisely, but it seems to...
        
        #label = myfont.render('text', antialising, color)
        label = myfont.render("fps: {0:0.0f}".format(currentfps), False, white)
        screen.blit(label, (xscreen*0.01,yscreen*0.01))
        
        #------------------------------------------------------------------------------------------#
        #----finally update the screen with all changes made in the iteration of the while loop----#
        #------- that was: reset the screen (by coloring a rect() in black)  ----------------------#
        #-------           draw the lander in its current state and position ----------------------#
        #-------           draw the labels                                   ----------------------#
        #------------------------------------------------------------------------------------------#
        pg.display.flip()
        
    pg.quit() # close the window
    print ps['V']
    
animate()
