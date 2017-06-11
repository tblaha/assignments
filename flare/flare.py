from numpy import *
import matplotlib.pyplot as plt
import os
import sys

avgsec=1. # s | seconds to look in past and future for the roling avg stuff

def analyse(data):
    outdata=[[],[],[]] # 0: time, 1:xpos, 2:fwdstick
    
    for dataline in data:
        if dataline[8]>-100. and dataline[8]<500.: # if in range of the runway
            time=dataline[0]
            outdata[0].append(time)
            outdata[1].append(dataline[8])
            
            currentvalues=[]
            k=0
            while k<len(data): # mvg avg
                if time-avgsec < data[k][0] and time+avgsec > data[k][0]:
                    currentvalues.append(data[k][11])
                k+=1
            movingavg=sum(currentvalues)/len(currentvalues)
            outdata[2].append(movingavg)

    aoutdata = array(outdata) # convert to numpy array

    flaretime=aoutdata[0][argmin(aoutdata[2])]
    flarepos =aoutdata[1][argmin(aoutdata[2])]
    
    return aoutdata,flaretime,flarepos

if len(sys.argv) == 4 and sys.argv[1]=="-silent":
    print "\nThis may take a while..."
    datapath   = sys.argv[2]
    files      = os.listdir(datapath)
    numoffiles = len(files)
    outlst=[]
    k=0
    for filename in files:
        data=genfromtxt("{0}/{1}".format(datapath,filename))
        aoutdata,flaretime,flarepos=analyse(data)
        outlst.append("Filename, {0}\n".format(filename))
        outlst.append("flaretime, {0}\n".format(flaretime))
        outlst.append("flarepos, {0}\n\n".format(flarepos))
        k+=1
        print "{0}/{1} files analysed".format(k,numoffiles)
    with open(sys.argv[3],"w") as outfile:
        outfile.write("[-],[s],[m]\n\n")
        for line in outlst:
            outfile.write(line)
elif len(sys.argv) == 2:
    filename=sys.argv[1]
    print "Analysing file {0}...".format(filename)
            
    data=genfromtxt("{0}".format(filename))
    aoutdata,flaretime,flarepos=analyse(data)
    print "\n*** Flare occured at {0}s and x={1}m ***".format(flaretime,flarepos)

    plt.plot(aoutdata[1],aoutdata[2])
    plt.show()
else: # print usage information
    print "Usage: {0} <filename | -silent> [datapath] [outfile]".format(sys.argv[0])
    print "\n   <filename> specifies a single file to be analysed and plotted. [datapath] and [outfile] have no effect with this option."
    print   "   <-silent> analyses all files in the [datapath] directory and prints the results to [outfile], which are both required arguments."
    sys.exit()
