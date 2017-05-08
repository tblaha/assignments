import numpy as np

#standard sea level properties ( might be overridden later)
slp={'p':101325.,'rho':1.225,'T':273.15+15.}
cnts={'R':287.05,'g':9.81,'a':-0.0065,'ts_upper':11000.,'isa_upper':85000.,'ft-m':0.3048}
h=0.0

# Compute the Temperature at altitude alt (in meters)
def temperature(alt):
    global slp
    global cnts
    if alt>cnts['ts_upper']:
        return cnts['ts_upper']*cnts['a']+slp['T'] # compute Tropopause temp, if necessary
    else:
        return slp['T']+cnts['a']*alt

# Compute the density at altitude alt (in meters)
def density(alt):
    global slp
    global cnts
    if alt > cnts['ts_upper']:
        cnts['tp_T']=cnts['ts_upper']*cnts['a']+slp['T'] # compute Tropopause temp, if necessary
        return slp['rho']*np.exp((-cnts['g'])/(cnts['tp_T']*cnts['R']) * (alt-cnts['ts_upper']))
    else:
        return slp['rho']*((slp['T']+cnts['a']*alt)/slp['T'])**((-cnts['g'])/(cnts['a']*cnts['R'])-1)

# Compute the pressure at altitude alt (in meters)
def pressure(alt):
    global slp
    global cnts
    if alt > cnts['ts_upper']:
        cnts['tp_T']=cnts['ts_upper']*cnts['a']+slp['T'] # compute Tropopause temp, if necessary
        return slp['p']*np.exp((-cnts['g'])/(cnts['tp_T']*cnts['R']) * (alt-cnts['ts_upper']))
    else:
        return slp['p']*((slp['T']+cnts['a']*alt)/slp['T'])**((-cnts['g'])/(cnts['a']*cnts['R']))


def input():
    global slp
    global cnts
    global h
    print "Standard sea level conditions:"
    while True:
        try:
            slp['p']=float(raw_input("Pressure in Pa [default:101325]: ") or slp['p'])
            break
        except ValueError:
            print "this was not a number. Try again"
            continue
    while True:
        try:
            slp['rho']=float(raw_input("Density in kg/m^3 [default:1.225]: ") or slp['rho'])
            break
        except ValueError:
            print "this was not a number. Try again"
            continue
    while True:
        try:
            slp['T']=float(raw_input("Temperature in K [default:288.15]: ") or slp['T'])
            break
        except ValueError:
            print "this was not a number. Try again"
            continue
    print "All sea level parameters set!"
    while True:
        try:
            h=cnts['ft-m']*float(raw_input("Geopotential altitude in ft: "))
            if h>cnts['isa_upper'] or h<0:
                print "ISA cannot be used at this altitude (Range:0 - 85000m). Try again"
            break
        except ValueError:
            print "this was not a number. Try again"
            continue

input()
print "At altitude %dm, the following ISA properties result"         % h
print "Temperature is %.2f K"  % temperature(h)
print "Pressure is %d Pa"      % pressure(h)
print "Density is %.4f kg/m^3" % density(h)
