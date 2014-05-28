# Written 7/2/14 by D Forgan 
# This script reads in a simple ASCII file containing
#  a 2D image to test blurring

import image as im
import numpy as np

inputfile = raw_input("What is the input filename? ")

# Read in image

print 'Reading in image ',inputfile

inputimage = im.image(np.zeros((1,1)),0.0,0.0,0.0,0.0)
inputimage.load_image(inputfile)

print inputimage.nx, inputimage.ny

inputimage.plot_image()

blurredimage = inputimage.clone()

blurredimage.gaussian_blur(15.0)
blurredimage.plot_image()

