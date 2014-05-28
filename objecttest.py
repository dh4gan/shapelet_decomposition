# Simple test script (Duncan Forgan, 6/2/14)

import image as im
import shapelet as sh
import coefficients as c

import numpy as np


# Set up image dimensions
nx = 50
ny = 50

# set up image scale

xmin = -10.0
xmax = 10.0

ymin = xmin
ymax = xmax

array = np.zeros((nx,ny))

testimage = im.image(array, xmin,xmax,ymin,ymax)

# Calculate maximum and minimum resolvable scales for this image

minscale = np.amin([testimage.xscale,testimage.yscale]) # Pixel 
maxscale = np.amax([xmax-xmin,ymax-ymin])

beta = np.sqrt(minscale*maxscale)
#beta = 1.0
nmax = maxscale/minscale-1 

print "minscale, maxscale, beta: ",minscale, maxscale, beta
print "nmax: ",nmax

# Now generate shapelets with random coefficients to find by decomposition 

nmax = 10
n1max = nmax/2
n2max = nmax/2
coeff = np.zeros((n1max,n2max))

print 'Adding shapelets '

for ni in range(n1max):
    for nj in range(n2max):
        
        shape = sh.shapelet(ni,nj,beta)        
        offx = 1.0
        offy= 2.0
        coeff[ni,nj] = pow(10.0,-ni*nj)*np.random.random()
        print shape, 'Coefficient: ',coeff[ni,nj]
        shape.add_to_image(testimage,coeff=coeff[ni,nj],offsetx=offx,offsety=offy)


# What is the total flux and centroid of the image

testfluxtot = testimage.total_flux()
testx, testy = testimage.centroid()

print 'Test image: ',testfluxtot, testx, testy

# Now do decomposition

decomposed = c.coefficients(nmax,beta)

decomposed.get_from_image(testimage)
print decomposed

decompimage = im.image(np.zeros((testimage.nx,testimage.ny)),testimage.xmin,testimage.xmax,testimage.ymin,testimage.ymax)
residualimage = im.image(testimage.array,testimage.xmin,testimage.xmax,testimage.ymin,testimage.ymax)

decomposed.make_image_from_coefficients(decompimage)

# Check image total flux and centroid

decompfluxtot = decompimage.total_flux()
decx, decy = decompimage.centroid()

print 'Reconstructed image: ',decompfluxtot, decx, decy

# Compare these with estimates from coefficients
print 'Calculating total flux, centroid from coefficients'

coeff_fluxtot = decomposed.total_flux()
coeff_x, coeff_y = decomposed.centroid()

print 'From coefficients: ', coeff_fluxtot, coeff_x, coeff_y

testimage.plot_image()
decompimage.plot_image()

residualimage.subtract(decompimage)

residualimage.plot_image()



