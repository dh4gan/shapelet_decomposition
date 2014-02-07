# Written 7/2/14 by D Forgan 
# This script reads in a simple ASCII file containing
# a 2D image for shapelet decomposition 

import image as im
import shapelet as sh
import shapelet_decomposition as decomp

import numpy as np
import matplotlib.pyplot as plt


inputfile = raw_input("What is the input filename? ")
nmax = input("What is the maximum order of shapelet to use? ")

# Read in image

inputimage = decomp.load_image(inputfile)

# Calculate maximum and minimum resolvable scales for this image

minscale = 1 # Pixel 
maxscale = np.amax([inputimage.nx,inputimage.ny])

beta = np.sqrt(minscale*maxscale)
#nmax = maxscale/minscale-1 

imagemax = np.amax(inputimage.array)

print 'Maximum Value is ', imagemax

# Plot this image

fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111)
plt.pcolormesh(inputimage.x, inputimage.y, inputimage.array.T, vmin = 0.0, vmax = imagemax)
plt.colorbar()

# Now do decomposition
coeff = decomp.get_shapelet_coefficients(inputimage,nmax,beta)

print coeff

# Create new image from decomposed coefficients

decompimage = inputimage

decomp.make_image_from_coefficients(decompimage, coeff,nmax,beta)

# Plot this image

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
plt.pcolormesh(decompimage.x, decompimage.y,decompimage.array.T, vmin = 0.0, vmax = imagemax)
plt.colorbar()
plt.show()

# Write the image to file

decompimage.write_to_file(inputfile+'decomposed_'+str(nmax)+'.dat')


