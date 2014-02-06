# Simple test script (Duncan Forgan, 6/2/14)

import image as im
import shapelet as sh

import numpy as np
import matplotlib.pyplot as plt

from sys import exit

coeff = [0,1]

n1 = 1
n2 = 0

# Set up image dimensions
nx = 100
ny = 100

# distance per pixel

xmin = -100.0
xmax = 100.0

ymin = xmin
ymax = xmax

array = np.zeros((nx,ny))

testimage = im.image(array, xmin,xmax,ymin,ymax)

# Calculate maximum and minimum resolvable scales for this image

minscale = 1 # Pixel 
maxscale = np.amax([nx,ny])

beta = np.sqrt(minscale*maxscale)
#beta = 1.0
nmax = maxscale/minscale-1 

shape = sh.shapelet(n1,n2,beta)

shape.add_to_image(testimage,10)

shape2 = sh.shapelet(n2,n1,beta)
shape2.add_to_image(testimage,2.0)

# Plot this shapelet

fig1 = plt.figure()
ax = fig1.add_subplot(111)

ax.pcolormesh(testimage.x, testimage.y, testimage.array.T)

plt.show()

# Decompose to find the coefficient

decomposed = shape.decompose_image(testimage)
decomposed2 = shape2.decompose_image(testimage)

print shape, decomposed
print shape2, decomposed2

