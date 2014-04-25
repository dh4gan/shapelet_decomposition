# Written 11/4/14 by Duncan Forgan
# Simple plotting script for image objects
# Reads in image from file and its shapelets and plots it

import image as im
import coefficients as c
import numpy as np

coeff_file = raw_input("What is the coefficients filename? ")

# Define image and coefficient objects
inputcoeff = c.coefficients(1.0,4.0)

# Load coefficients
inputcoeff.read_from_file(coeff_file)

inputcoeff.plot_coefficients(coeff_file+'.ps', 'ps')