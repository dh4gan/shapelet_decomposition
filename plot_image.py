# Written 11/4/14 by Duncan Forgan
# Simple plotting script for image objects
# Reads in image from file and plots it

import image as im
import numpy as np

filename = raw_input("What is the image filename? ")

inputimage = im.image(np.zeros((1,1)),0.0,0.0,0.0,0.0)
inputimage.load_image(filename)


inputimage.plot_image()