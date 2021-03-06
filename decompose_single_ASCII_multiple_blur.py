# Written 28/5/14 by D Forgan 
# This script reads in a single 2D image
# in simple ASCII format for shapelet decomposition
# with multiple blurring choices

import image as im
import coefficients as c
import numpy as np

inputfile = raw_input("What is the input filename? ")
nmax = input("What is the maximum order of decomposition? ")
sigmamin = input("Define minimum blur in physical units: ")
sigmamax = input("Define minimum blur in physical units: ")
nsigma = input("How many blurring evaluations? ")


# Read in image
print 'Reading in image from file',inputfile

initialimage = im.image(np.zeros((1,1)),0.0,0.0,0.0,0.0)
initialimage.load_image(inputfile)

dsigma = (sigmamax - sigmamin)/float(nsigma)

for i in range(nsigma):
    
    sigma = sigmamin + i*dsigma
    print 'Carrying out decomposition for sigma ', sigma
    inputimage = initialimage.clone()
        
    inputimage.gaussian_blur(sigma)
    # Write this blurred image to file
    blur_file = 'blur_'+str(sigma)+'_'+inputfile
    inputimage.write_to_file(blur_file)
    
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
    
    coeff_file = 'coefficients_blur_'+str(sigma)+'_'+inputfile    
    coeff.write_to_file(coeff_file)
    
    # Reconstruct image from shapelet coefficients
    
    image_reconstructed = im.image(np.zeros((inputimage.nx, inputimage.ny)),inputimage.xmin, inputimage.xmax,inputimage.ymin, inputimage.ymax)
    coeff.make_image_from_coefficients(image_reconstructed)
    
    # Write this image to file
    reconstruct_file = 'reconstructed_blur_'+str(sigma)+'_'+inputfile
    image_reconstructed.write_to_file(reconstruct_file)
    
    # Calculate residual image
    residual = im.image(inputimage.array,inputimage.xmin, inputimage.xmax,inputimage.ymin, inputimage.ymax)
    residual.subtract(image_reconstructed)
    
    # Write this image to file
    residual_file = 'residual_blur_'+str(sigma)+'_'+inputfile
    residual.write_to_file(residual_file)

print "Run complete"

