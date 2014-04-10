# Written 7/2/14 by D Forgan 
# This script reads in a series of 2D image
# in simple ASCII format for shapelet decomposition

import image as im
import coefficients as c
import numpy as np
from sys import path
path.append('/disk1/dhf/programs/python/filefinder')

import filefinder.localfiles as ff

nmax = input("What is the maximum order of decomposition? ")
prefix = raw_input("What is the input file prefix? ")

inputfileset = ff.find_local_input_fileset(prefix+'*')


for inputfile in inputfileset:
    # Read in image

    print 'Reading in image from file',inputfile

    inputimage = im.image(np.zeros((1,1)),0.0,0.0,0.0,0.0)

    inputimage.load_image(inputfile)

    
    # Calculate maximum and minimum resolvable scales for this image

    minscale = np.amin([inputimage.xscale,inputimage.yscale]) # Pixel 
    maxscale = np.amax([inputimage.xmax-inputimage.xmin,inputimage.ymax-inputimage.ymin])

    beta = np.sqrt(minscale*maxscale)
    #beta = 1.0
    image_nmax = maxscale/minscale-1 

    print 'The preferred parameters are:'
    print 'beta=',beta
    print 'Image Prediction for Maximum Order = ',image_nmax

    print 'Using maximum order of ',nmax

    # Do shapelet decomposition
    
    coeff = c.coefficients(nmax,beta)
    coeff.get_from_image(inputimage)
    
    # Write shapelet coefficients to file
    
    coeff_file = 'coefficients_'+inputfile    
    coeff.write_to_file(coeff_file)
    
    # Reconstruct image from shapelet coefficients
    
    image_reconstructed = im.image(np.zeros((inputimage.nx, inputimage.ny)),inputimage.xmin, inputimage.xmax,inputimage.ymin, inputimage.ymax)
    coeff.make_image_from_coefficients(image_reconstructed)
    
    # Write this image to file
    reconstruct_file = 'reconstructed_'+inputfile
    image_reconstructed.write_to_file(reconstruct_file)
    
    # Calculate residual image
    residual = im.image(inputimage.array,inputimage.xmin, inputimage.xmax,inputimage.ymin, inputimage.ymax)
    residual.subtract(image_reconstructed)
    
    # Write this image to file
    residual_file = 'residual_'+inputfile
    residual.write_to_file(residual_file)


print "Run complete"

