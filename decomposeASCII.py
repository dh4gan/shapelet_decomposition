# Written 7/2/14 by D Forgan 
# This script reads in a simple ASCII file containing
# a 2D image for shapelet decomposition 

import image as im
import coefficients as c
import numpy as np


inputfile = raw_input("What is the input filename? ")

# Read in image

print 'Reading in image ',inputfile

inputimage = im.image(np.zeros((1,1)),0.0,0.0,0.0,0.0)

inputimage.load_image(inputfile)

print inputimage.nx, inputimage.ny
# Calculate maximum and minimum resolvable scales for this image

minscale = 1 # Pixel 
maxscale = np.amax([inputimage.nx,inputimage.ny])

beta = np.sqrt(minscale*maxscale)
nmax = maxscale/minscale-1

print 'The preferred parameters are:'
print 'beta=',beta
print 'Maximum Order = ',nmax

nchoice = input("What maximum order is to be used (0=calculated maximum)? ") 

if(nchoice!=0):
    nmax = nchoice
    
print 'Using maximum order of ',nmax

imagemax = np.amax(inputimage.array)

print 'Maximum Value is ', imagemax

# Plot this image
inputimage.plot_image()

# Now do decomposition
coeff = c.coefficients(nmax,beta)
coeff.get_from_image(inputimage)

print coeff

# Create new image from decomposed coefficients

decompimage = im.image(np.zeros((inputimage.nx, inputimage.ny)),inputimage.xmin, inputimage.xmax,inputimage.ymin, inputimage.ymax)

coeff.make_image_from_coefficients(decompimage)

# Plot this image

decompimage.plot_image()

# Plot the coefficients
coeff.plot_coefficients('coefficients.ps','ps')


# Find the residual
residual = im.image(inputimage.array,inputimage.xmin, inputimage.xmax,inputimage.ymin, inputimage.ymax)
residual.subtract(decompimage)

residualmax = np.amax(residual.array)
residualmin = np.amin(residual.array)

print residualmin, residualmax

residual.plot_image()


# Write the image to file

decompimage.write_to_file(inputfile+'decomposed_'+str(nmax)+'.dat')


