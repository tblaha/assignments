from numpy import *
import matplotlib.pyplot as plt
import os

path="./data/"
dir = os.listdir(path)

print "\n***Welcome to the Mandelbrot fractal plotter***"
print "\nplease select a settings file of your choice:"

i=0
for filename in dir:
    print "{0}) {1}".format(i,filename)
    i += 1

while True:
    try:
        choice = str(dir[int(raw_input("make your choice: "))])
        break
    except IndexError:
        print "This was not a number or the number was out of range, try again!"

data = {'niter':50.,'radius':2.,'xmin':-2.,'xmax':1.,'ymin':-1.5,'ymax':1.5,'npixels':500.}
file = genfromtxt(path+choice,dtype="string",delimiter=";")
for line in file:
    if line[-1]:
        data[line[0]]=float(line[-1])



#***********************************#
c = ones((int(data['npixels']),int(data['npixels'])),dtype=complex)

A = arange(data['xmin'],data['xmax'],(data['xmax']-data['xmin'])/(data['npixels']))
B = arange(data['ymin'],data['ymax'],(data['ymax']-data['ymin'])/(data['npixels']))

for a in range(int(data['npixels'])):
    for b in range(int(data['npixels'])):
        c[a,b]=  A[a] + B[b] * 1j

def iterate(c, z = 0 + 0j, i = 0):
    if i > data['niter']:
        return abs(z)
    if not i % 10:
        print i
    zplus1=z*z + c
    i +=1
    return iterate(c, where(abs(zplus1) < data['radius']*1.01, zplus1, data['radius']) ,i)

plt.imshow(abs(iterate(c)),plt.get_cmap('seismic'))
plt.show()
