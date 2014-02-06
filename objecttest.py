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

# set up image scale

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

# Now generate shapelets with random coefficients to find by decomposition 

nmax = 10
n1max = nmax/2
n2max = nmax/2
coeff = np.zeros((n1max,n2max))

print 'Adding shapelets '

for ni in range(n1max):
    for nj in range(n2max):
        
        shape = sh.shapelet(ni,nj,beta)
        print shape
        coeff[ni,nj] = 10.0*np.random.random()
        shape.add_to_image(testimage,coeff[ni,nj])


# Plot this image

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.pcolormesh(testimage.x, testimage.y, testimage.array.T)
plt.show()


# Now do decomposition

decomposed = np.zeros((n1max,n2max))

print 'Decomposing Image'
for ni in range(n1max):
    for nj in range(n2max):
        shape = sh.shapelet(ni,nj,beta)
        print shape
        decomposed[ni,nj] = shape.decompose_image(testimage)
        
        
print decomposed
print coeff


