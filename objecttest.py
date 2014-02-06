# Simple test script (Duncan Forgan, 6/2/14)

import image as im
import shapelet as sh

import numpy as np
import matplotlib.pyplot as plt

from sys import exit

coeff = [0,1]


n1 = 27
n2 = 27

# Set up image dimensions
nx = 10
ny = 10

# distance per pixel

xmin = -100.0
xmax = 100.0

ymin = xmin
ymax = xmax

xscale = (xmax-xmin)/nx
yscale = (ymax-ymin)/ny

x = np.linspace(ymin,ymax,num=nx)
y = np.linspace(xmin,xmax,num=ny)

array = np.zeros((nx,ny))

testimage = im.image(array)

# Calculate maximum and minimum resolvable scales for this image

minscale = 1 # Pixel 
maxscale = np.amax([nx,ny])

beta = 1.0/np.sqrt(minscale*maxscale)
#beta = 1.0
nmax = maxscale/minscale-1 

shape = sh.shapelet(n1,n2,beta)

print shape

shape.add_to_image(testimage)

# Plot this shapelet

fig1 = plt.figure()
ax = fig1.add_subplot(111)

ax.imshow(testimage.array.T,origin = 'lower')

plt.show()


