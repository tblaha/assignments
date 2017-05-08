import numpy as np
import sys

cnts={'R':287.05,'g':9.81665,'ft-m':0.3048,'kts-m/s':0.51444,'Re':6371000.,'gamma':1.4}
isa={'name':['Troposhere','Tropopause','Stratosphere 1','Stratosphere 2','Stratopause','Mesosphere 1','Mesosphere 2', 'Mesopause'],# From table
     'h':[0.,11000.,20000.,32000.,47000.,51000.,71000.,84852.],# From table
     'a':[-0.0065,0,0.001,0.0028,0,-0.0028,-0.002,None], # From table
     'T':[273.15+15.], ## Will be filled up
     'p':[101325.], ## will be filled
     'rho':[1.225]}

#menu parameters
menu={'id':     ['main',
                 'isa',
                 'geopot',
                 'geopot_sub',
                 'speeds',
                 'speeds_sub',
                 'speeds_sub2'],
      'heading':['Welcome to the Main Menu! Select an action or type "quit" anytime to exit:',
                 'ISA calculator --- Select altitude unit:',
                 'Altitude Converter --- Select input value',
                 'Altitude Converter Sub Menu --- Select input unit',
                 'Speed converter --- Select input speed unit',
                 'Speed converter --- Select input altitude unit',
                 'Speed converter --- Select output speed unit'],
      'items':  [['  --> 1. Plain ISA calculations (0-85km)','  --> 2. Altimeter (altitude from static pressure)','  --> 3. Geopotential vs Geometric converter','  --> 4. Speed Converter (TAS,CAS,Mach)'],
                 ['  --> 1. Enter an altitude in meters','  --> 2. Enter an altitude in feet','  --> 3. Enter an altitude in FL'],
                 ['  --> 1. Enter a geometric altitude', '  --> 2. Enter a geopotential altitude'],
                 ['  --> 1. Enter an altitude in meters','  --> 2. Enter an altitude in feet','  --> 3. Enter an altitude in FL'],
                 ['  --> 1. TAS','  --> 2. CAS','  --> 3. Mach'],
                 ['  --> 1. m'  ,'  --> 2. ft' ,'  --> 3. FL'],
                 ['  --> 1. TAS','  --> 2. CAS','  --> 3. Mach']],
      'action': [['isa_calculate','altimeter','geopot','speeds'], # action and switch depend on the choice made. Thus, length of switch and action list must equal length of items list
                 [''],
                 [''],
                 [''],
                 [''],
                 [''],
                 ['']],
      'switch': [[''],
                 ['m','ft','FL'],
                 ['p','m'], ##geoPotential, geoMetric
                 ['m','ft','FL'],
                 ['TAS','CAS','M'],
                 ['m','ft','FL'],
                 ['TAS','CAS','M']],
      }

### Menu constructer and user choice finder #########################################################################
# Takes  : The "id"-string of the menu as specified in the "menu" dictionary                                        #
# Does   : Present the menu to the user, ask for choice. Exits the program if the user types "quit"                 #
# Returns: a list [i,c] where "i" is the position of the menu in the dictionary and "c" the choice made by the user #
#          (counting from 0)                                                                                        #
#####################################################################################################################
def make_menu(id):
    i=0
    while id != menu['id'][i]: # Find position of the requested menu in the menu dictionary
        i=i+1

    print "\n\n" + menu['heading'][i] + "\n" # Print heading

    noi=len(menu['items'][i]) # get amount of choices presented to user (_n_umber _o_f _i_tems)
    for item in menu['items'][i]: # show all choices
        print item
    print

    while True: # Politely ask for choice or quit the program on quit
        try:
            raw_choice=raw_input('Make your choice [default 1]: ')
            if raw_choice.lower() == 'quit':
                sys.exit()
            choice=int(raw_choice or 1)
            if choice<0 or choice>noi:
                print 'The choice is not available! Try again!'
                continue
            break
        except ValueError:
            print 'Please enter an integer! Try again!'

    return [i,choice-1] ## "-1" because the lists count from 0, not 1 (as the user does)




### Temperature computation #########################################################################################
# Takes  : Altitude (m) (float)                                                                                     #
# Does   : Nothing                                                                                                  #
# Returns: The temperature as float                                                                                 #
#####################################################################################################################
def temperature(alt):
    i=0
    while alt>isa['h'][i+1]: ## Get the layer we're in
        i+=1
    return (alt-isa['h'][i])*isa['a'][i]+isa['T'][i] # compute temp by multiplying difference in _alt_ and _base height_ by _lapse rate_ and adding to _base temp_

### Density and Pressure computation ################################################################################
# Takes  : Altitude (m) (float), propertiy selector string (either 'rho' or 'p')                                    #
# Does   : Nothing                                                                                                  #
# Returns: The density of pressure as float                                                                         #
#####################################################################################################################
def pressure_density(alt,selector):
    i=0
    while alt>isa['h'][i+1]: ## Get the layer we're in
        i=i+1
    if selector == 'rho':
        adjuster=-1
    else:
        adjuster=0

    if isa['a'][i]:                                                                                                       # Formulae varies for isotherm and non-isotherm
        return isa[selector][i]*((temperature(alt))/isa['T'][i])**((-cnts['g'])/(isa['a'][i]*cnts['R'])+adjuster) # Using base Temp of layer. Adjuster needed for density only
    else:
        return isa[selector][i]*np.exp((-cnts['g'])/(isa['T'][i]*cnts['R']) * (alt-isa['h'][i]))                              # Using base Temp of layer which is uniform throuout


### Perform ISA calculations ########################################################################################
# Takes  : Nothing                                                                                                  #
# Does   : Ask the user for input altitude and prints the results (T,p,rho,percentages p/p0,rho/rho0) after calling #
#          the temperature/density/pressure functions                                                               #
# Returns: A list [T,p,rho] for the altitude                                                                        #
#####################################################################################################################
def isa_calculate():
    outlist=make_menu('isa')                        ## Grab the users choice for altitude unit
    switch=menu['switch'][outlist[0]][outlist[1]]

    while True:                                     ## Evaluate that choice by the switch parameter as found by 'make_menu'
        try:
            if   switch == 'm':                                                                       # Adjusting to meters _on the spot_
                alt=float(raw_input("Geopotential altitude in m: "))
            elif switch == 'ft':
                alt=cnts['ft-m']*float(raw_input("Geopotential altitude in ft: "))
            elif switch == 'FL':
                alt=cnts['ft-m']*100*float(raw_input("Geopotential altitude in FL: "))

            if alt>isa['h'][7] or alt<0:                                                                # If not in range of ISA data, let user continue trying
                print "ISA cannot be used at this altitude (Range:0 - %dm). Try again" % isa['h'][7]
                continue

            break
        except ValueError:                            # If not an integer: let user continue trying
            print "this was not a number. Try again"
            continue

    T  =temperature(alt) ## Compute the states
    p  =pressure_density(alt,'p')
    rho=pressure_density(alt,'rho')

    print "\n\n*** At altitude of %.4g m, the following ISA properties result: ***\n"  % alt

    print "Temperature is %.4g K or %.4g C"                                      % (T,T-273.15)
    print "Pressure is %.4g Pa"                                                  % p
    print "Density is %.4g kg/m^3"                                               % rho

    print "\n*** Relative to sea level, that is: ***\n"

    print "Pressure: %.4g %%"                                                     % (100.*p/isa['p'][0])
    print "Density : %.4g %%\n\n"                                                 % (100.*rho/isa['rho'][0])

    return [T,p,rho]   # return the list with the properties

### Altimeter #######################################################################################################
# Takes  : Nothing                                                                                                  #
# Does   : Ask the user for input pressure and prints the resulting altitude (in m, ft, FL) -- no menu in this one  #
# Returns: The altitude in m                                                                                        #
#####################################################################################################################
def altimeter():
    global cnts,isa,menu

    print "\n*** Altimeter ***\n"

    while True:
        try:
            p=float(raw_input("Pressure in Pa: "))

            if p<isa['p'][7] or p>101325:                                                                # If not in range of ISA data, let user continue trying
                print "ISA cannot be used at this pressure (Range:101325 - %d Pa). Try again" % isa['p'][7]
                continue

            break
        except ValueError:                            # If not an integer: let user continue trying
            print "This was not a number. Try again"
            continue

    i=0
    while p<isa['p'][i+1]: # get layer in ISA based on input pressure. Works because pressure is a monotone decreasing function of alt
        i=i+1

    if isa['a'][i]:
        alt=isa['h'][i]+isa['T'][i]/isa['a'][i] * ((p/isa['p'][i])**(-(isa['a'][i]*cnts['R'])/cnts['g']) - 1) # gradient
    else:
        alt=isa['h'][i]-cnts['R']*isa['T'][i]/cnts['g'] * np.log(p/isa['p'][i]) # isothermal

    print "\n*** The pressure %.4g Pa corresponds to : ***\n"            % p

    print "Geopotential:"
    print "  %.4g m"                                                  % alt
    print "  %.4g ft"                                                 % (alt/cnts['ft-m'])
    print "  FL%d \n\n"                                                   % (alt/(cnts['ft-m'] * 100)) # FIX THIS, ROUNDING IS WRONG AND NO LEADING ZERO(S)

    return alt  # return the altitude in m

### Geopotential vs Geometrical converter ###########################################################################
# Takes  : Nothing                                                                                                  #
# Does   : Ask user for input dimension. Then ask him/her for input unit. So 2 menus for this one. Then prints results #
# Returns: Nothing (yet)                                                                                            #
#####################################################################################################################
def geopot():
    outlist=make_menu('geopot')
    switch=menu['switch'][outlist[0]][outlist[1]]
    if switch =='p':
        fr='Geopotential'
        to='Geometric'
    else:
        fr='Geometric'
        to='Geopotential'

    print "\n\nConverting %s Altitude to %s Altitude!\n" % (fr,to) ## Summarize choise!

    outlist2=make_menu('geopot_sub') # make the sub menu asking for the input unit
    switch2=menu['switch'][outlist2[0]][outlist2[1]]

    while True: ## User enters "from"-altitude
        try:
            if   switch2 == 'm':                                                                       # Adjusting to meters _on the spot_
                alt=float(raw_input("Altitude in m: "))
            elif switch2 == 'ft':
                alt=cnts['ft-m']*float(raw_input("Altitude in ft: "))
            elif switch2 == 'FL':
                alt=cnts['ft-m']*100*float(raw_input("Altitude in FL: "))

            break
        except ValueError:                            # If not an integer: let user continue trying
            print "this was not a number. Try again"
            continue

    if switch == 'p':
        geometric=alt*(cnts['Re']/(cnts['Re']+alt))
        print "\n\n*** The geopotential altitude of %.4gm corresponds to geometric altitudes of: ***\n" % alt

        print "  %.4g m"                                                  % geometric
        print "  %.4g ft"                                                 % (geometric/cnts['ft-m'])
        print "  FL%03d \n\n"                                             % (geometric/(cnts['ft-m'] * 100)) # FIX THIS, ROUNDING IS WRONG
    elif switch == 'm':
        geopot=alt*(cnts['Re']/(cnts['Re']-alt))
        print "\n\n*** The geopotential altitude of %.4g corresponds to geometric altitudes of: ***\n" % alt

        print "  %.4g m"                                                  % geopot
        print "  %.4g ft"                                                 % (geopot/cnts['ft-m'])
        print "  FL%03d \n\n"                                               % (geopot/(cnts['ft-m'] * 100)) # FIX THIS, ROUNDING IS WRONG

### Speed converter #################################################################################################
# Takes  : Nothing                                                                                                  #
# Does   : Ask user for input dimensions. Then ask him/her for input unit.                                          #
# Returns: Nothing (yet)                                                                                            #
#####################################################################################################################
def speeds():
    outlist=make_menu('speeds')
    switch=menu['switch'][outlist[0]][outlist[1]]
    outlist2=make_menu('speeds_sub')
    switch2=menu['switch'][outlist2[0]][outlist2[1]]

    while True: ## User enters "from"-speed
        try:
            if   switch != 'M':
                speed=float(raw_input("Input speed in " + switch + " (kts): "))
            else:
                speed=float(raw_input("Input speed in " + switch + ": "))
            if   switch2 == 'm':                                                                       # Adjusting to meters _on the spot_
                alt=float(raw_input("Geopotential altitude in m: "))
            elif switch2 == 'ft':
                alt=cnts['ft-m']*float(raw_input("Geopotential altitude in ft: "))
            elif switch2 == 'FL':
                alt=cnts['ft-m']*100*float(raw_input("Geopotential altitude in FL: "))
            break
        except ValueError:                            # If not an integer: let user continue trying
            print "this was not a number. Try again"
            continue

    ## convert to TAS first
    if switch == "TAS":
        tas=speed
    elif switch == "CAS":
        tas=np.sqrt(isa['rho'][0]/pressure_density(alt,'rho')) * speed
    elif switch == "M":
        tas=speed*np.sqrt(cnts['gamma']*cnts['R']*temperature(alt))/cnts['kts-m/s']

    ## now convert to out unit
    cas=np.sqrt(pressure_density(alt,'rho')/isa['rho'][0])*tas
    m=tas*cnts['kts-m/s']/np.sqrt(cnts['gamma']*cnts['R']*temperature(alt))

    ## output all the stuff
    geometric=alt*(cnts['Re']/(cnts['Re']+alt))
    print "\n\n*** The airspeed entered corresponds to the following airspeeds: ***\n"

    print "  %.4g kts TAS"                                                  % tas
    print "  %.4g kts CAS"                                                  % cas
    print "  %.4g Mach \n\n"                                                % m


################################# let the fun begin #######################################

## populate isa dictionary with proper pressures. densities and temperatures
for alt in isa['h']:
    if alt: ## exclude sea level
        isa['T'].append(temperature(alt)) ## note that this works because the logic is such that the base alt of a layer is taken care of by the previous layer. If the sea level values are set, there is always all values of the previous layer to compute the next.
        isa['p'].append(pressure_density(alt,'p'))
        isa['rho'].append(pressure_density(alt,'rho'))


while True:
    print "\n\n*** International Standard Atmosphere (ISA) calculations (and more) ***\n"

    out=make_menu('main')
    function=menu['action'][out[0]][out[1]] ## This gives the correct "action". See "menu"-directory
    globals()[function]()                   ## execute associated function giving the outlist with "menu"-list position that takes care of all the rest of that option.

    dummy=raw_input("Proceed with next query: Press Enter:")
    print

