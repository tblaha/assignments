import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def marsinit(filename):
    marstable = np.loadtxt(filename,skiprows=2)
    return marstable

def marsatm(h,marstable):
    for i in range(0,len(marstable)):
        if h==1000*marstable[i][0]:
            return marstable[i][1:4]
        elif h>1000*marstable[i][0] and h<1000*marstable[i+1][0]:
            k =  (h - 1000*marstable[i][0])/(1000*marstable[i+1][0]-1000*marstable[i][0])
            a = (1-k) * marstable[i][1] + k *marstable[i+1][1]
            b = (1-k) * marstable[i][2] + k *marstable[i+1][2]
            c = (1-k) * marstable[i][3] + k *marstable[i+1][3]
            return a,b,c
      
mt = marsinit("./data/mars.txt")
speed = 262.

times = []
heights = []
R = 191.84
vref = -2.
throttle_factor = 0.05        
cs = 4.92
ve = 4400.
dry_mass = 699.
fluid_mass = 70. #assumption
m = dry_mass + fluid_mass
cutoff = 0.3
alt_thrustle = 1770. #assumption
v_start = 262. #initital speed
H= np.array([0.,20000.]) # array of heights
angle = math.radians(-20.) #gamma angle       
V=np.array([np.cos(angle),np.sin(angle)])*v_start #array of velocity components
results = {}
results={'time':[],'mfuel':[],'me':[],'Hx':[],'Hy':[],'V':[],'Vx':[],'Vy':[],'angle':[]} 
dt = 0.01
time = 0.    
vy = 0.
vx = 0.
m_limit= 5.
g0=np.array([0.,-3.711]) 
while H[1]>0:
    temperature,density, speed = marsatm(H[1],mt)
    pressure  = density * temperature * R
    Fdrag = -0.5*cs*density*V*math.sqrt(np.dot(V,V))
    Fgrav = m*g0
    angle=math.degrees(-(math.atan2(V[0],V[1])-np.pi/2))
    if m>dry_mass and H[1]<=alt_thrustle and H[1]>cutoff:
        me = -m*g0[1]/ve +throttle_factor*(vref-V[1])
        me = min(me,m_limit)
    else:
        me = 0
    m -= me*dt   
    Fthrust = -me*ve*V/(math.sqrt(np.dot(V,V))) #sqrt(dot(V,V)) is the absolute value, so the magnitude
    F = Fdrag + Fgrav + Fthrust
    a=F/m
    V += a*dt                                        
    H += V*dt
    times.append(time)
    time += dt;                                        
    results['me'].append(me)
    results['time'].append(time)
    results['mfuel'].append(m-dry_mass)
    results['Hx'].append(H[0])
    results['Hy'].append(H[1])
    results['V'].append((V[0]**2+V[1]**2)**0.5)
    results['Vx'].append(V[0])
    results['Vy'].append(V[1])
    results['angle'].append(angle)

print results['Vy'][-1]
#fig = plt.figure()
#fig.subplots_adjust(bottom=0.2)
#ax1 = fig.add_subplot(211)
#ax2 = ax1.twinx()
#line1 = ax1.plot(heights,'bo-',label='Alt')
#line2 = ax2.plot(times,'yo-',label='Time')
#ax1.set_ylim(0,10)
#ax2.set_ylim(0,10)
#red_patch = mpatches.Patch(color='red', label='Alt vs Time')
#plt.legend(handles=[red_patch])
