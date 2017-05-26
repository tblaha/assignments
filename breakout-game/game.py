import numpy as np
from math import *
import pygame as pg                           # Import the package only when needed, so it is not loaded when animate() is not even called

pg.init()                                     # Initialise pygame (has no visual effect)
pg.font.init()                                # Initialise the font stuff for labels
myfont = pg.font.SysFont('monospace', 16)     # define a monospace font

def worldtoscreen(worldcoordinates):
    xworld,yworld=worldreso
    xscreen,yscreen=screenreso
    xworldcoord,yworldcoord=worldcoordinates
    xscreencoord=int(xworldcoord/xworld*xscreen+0.5)
    yscreencoord=yscreen-int(yworldcoord/yworld*yscreen + 0.5)
    screencoordinates=(xscreencoord,yscreencoord)
    return screencoordinates

black=(0,0,0)
white=(255,255,255)

screenreso=(600,600)
worldreso=(1000.,1000.)
xscreen,yscreen=screenreso                    # px  | screensizelution
xworld,yworld  =worldreso
xws = xworld/xscreen
yws = yworld/yscreen

screen=pg.display.set_mode(screenreso)        # I think this actually opens a window with the resolution defined at the end of this file 
scrrect=screen.get_rect()                     # this gets the screen rectangle. I understand a rect as the geometric basis for the screen surface that 
                                                ## can be used to read or assign values (like position and size)
perrow = 10
brickpixel  = int(float(xscreen)/perrow)
brickscale  = brickpixel/1544.
brickheight  = 539*brickscale
brick_orig  = pg.image.load("brick.png")

ballspeed = 4E2
ballscale = 0.8
ball_orig = pg.image.load("ball.gif")
ball_orig = pg.transform.rotozoom(ball_orig,0,ballscale)
P = np.array([500.,70.])
V = np.array([0., ballspeed])

boardspeed = 3E2
boardscale = 0.225
board_orig = pg.image.load("board.png")
board_orig = pg.transform.rotozoom(board_orig,0,boardscale)
P_board = np.array([500.,0.])
V_board = np.array([0.,0.])

fps=120.                                       # 1/s | will be used to limit the amount of frames drawn per second (so less CPU usage)

rows=4
bricks = [[],[],[],[]] # 4 rows
brickbegin=0.9*yworld
for a in range(rows):
    if not (a+2)%2:
        for b in range(perrow):
            brick     = pg.transform.rotozoom(brick_orig,0,brickscale)
            brickrect = brick.get_rect()
            coords    = (brickpixel*xws*b,brickbegin-brickheight*yws*a)
            bricks[a].append([brickrect,1])
            bricks[a][b][0].topleft=worldtoscreen(coords)
    else:
        for b in range(perrow+1):
            brick     = pg.transform.rotozoom(brick_orig,0,brickscale)
            brickrect = brick.get_rect()
            coords    = (brickpixel*xws*b-brickpixel*xws/2.,brickbegin-brickheight*yws*a)
            bricks[a].append([brickrect,1])
            bricks[a][b][0].topleft=worldtoscreen(coords)
        
score=0

clock = pg.time.Clock()                       # initialise the clock (will be used to monitor/limit fps)

k=0
dt=1/fps
while True:
    pg.draw.rect(screen,black,scrrect)
    
    P_board += dt * V_board
    P += dt * V

    ball     = pg.transform.rotozoom(ball_orig,0,ballscale)
    ballrect = ball.get_rect()
    
    ballrect.center=worldtoscreen(P)
    screen.blit(ball,ballrect)
    
    
    boardrect = board_orig.get_rect()
    
    boardrect.midbottom=worldtoscreen(P_board)
    screen.blit(board_orig,boardrect)
    
    if k > 0:
        k -=1
    if ballrect.colliderect(boardrect) and k <= 0:
        k=10 # 0^2 + 1^2 = ballspeed^2
        V[0] = -ballspeed * (boardrect.topleft[0]+boardrect.width*0.5-worldtoscreen(P)[0])/(boardrect.width*0.7)
        V[1] = sqrt(ballspeed**2 - V[0]**2)
        
    changed=0
    for a in range(len(bricks)):
        for b in range(len(bricks[a])):
            if bricks[a][b][1]:
                screen.blit(brick,bricks[a][b][0])                      # blit it to the screen (note: this doesnt update the screen yet)
                if ballrect.colliderect(bricks[a][b][0]):
                    bricks[a][b][1]=0
                    score += 1
                    anglecenter   = atan2(P[1]-yworld+bricks[a][b][0].center[1]*yws,P[0]-bricks[a][b][0].center[0]*xws)
                    determinant   = atan(539./1544.)
                    if not changed:
                        if  anglecenter >= -pi+determinant and anglecenter <=-determinant:
                            changed=1 # came from bot
                            V[1] *= -1
                        elif anglecenter >=-determinant and anglecenter <= determinant:
                            changed=1 # came from right
                            V[0] *= -1
                        elif anglecenter >= determinant and anglecenter <=pi-determinant:
                            changed=1 # came from top
                            V[1] *= -1
                        else:
                            changed=1 # came from left
                            V[0] *= -1
    
    pg.event.pump()
    currentkeys = pg.key.get_pressed()
    if currentkeys[pg.K_RIGHT] and P_board[0] <= xworld >= 0:
        V_board[0] = boardspeed
    elif currentkeys[pg.K_LEFT] and P_board[0] >= 0:
        V_board[0] = -boardspeed
    else:
        V_board[0] = 0
    for event in pg.event.get():
        if event.type==pg.QUIT or currentkeys[pg.K_ESCAPE]:
            exit()
    
    if P[0] < 0. or P[0] > xworld:
        V[0] *= -1
    if P[1] > yworld:
        V[1] *= -1
    if P[1] < 0:
        print "You lose!"
        break
        
    #--------------------# note: this has no effect on the actual simulation timing (so if realtime or not)
    #----timing stuff----#       because pg.time.get_ticks() is an absolute measure of the time passed.
    #--------------------#       --> this just reduces CPU load
    currentfps=clock.get_fps()                                 # 1/s | gets fps by averaging last 10 calls to clock.tick()
    clock.tick(fps)                                            # limit fps. Not sure how this works precisely, but it seems to...
    
    #label = myfont.render('text', antialising, color)
    label = myfont.render("score: {0} -- fps: {1:0.0f}".format(score,currentfps), False, white)
    screen.blit(label, (xscreen*0.01,yscreen*0.01))
    
    pg.display.flip()
    
pg.quit() # close the window
