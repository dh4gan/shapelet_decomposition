# Written 11/4/14 by Duncan Forgan
# Simple plotting script for image objects
# Reads in image from file and its shapelets and plots it

import image as im
import coefficients as c
import numpy as np

imagefile = raw_input("What is the image filename? ")
coeff_file = "coefficients_"+imagefile
n1 = input("What is the first index of the shapelet to subtract? ")
n2 = input("What is the second index of the shapelet to subtract? ")

n1 = int(n1)
n2 = int(n2)


# Define image and coefficient objects
inputimage = im.image(np.zeros((1,1)),0.0,0.0,0.0,0.0)
inputcoeff = c.coefficients(1.0,4.0)

# Load image
inputimage.load_image(imagefile)

# Load coefficients
inputcoeff.read_from_file(coeff_file)

# Define shapelet to subtract
shapelet = inputcoeff.create_shapelet(n1, n2)

#Subtract shapelet
shapelet.subtract_from_image(inputimage)

inputimage.plot_image()