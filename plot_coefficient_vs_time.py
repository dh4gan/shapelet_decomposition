# Written 11/4/14 by Duncan Forgan
# Simple plotting script for coefficent objects
# Reads in multiple coefficient files and plots a selected coefficient vs file

import coefficients as c
import numpy as np
import matplotlib.pyplot as plt
from os.path import isfile

prefix = raw_input("What is the image file prefix? ")
initial = input("What is the initial filenumber? ")
final = input("What is the final filenumber? ")

# Read in coefficients files

coeff_list = []
filenumbers = []
nfiles = 0

for i in range(initial,final+1):
    
    coeff_file = "coefficients_"+prefix+"."+str(i)

    if(isfile(coeff_file)):
        print "Reading file ",coeff_file    
        nfiles +=1
        filenumbers.append(i)
        # Define image and coefficient objects
        inputcoeff = c.coefficients(1.0,4.0)

        # Load coefficients
        inputcoeff.read_from_file(coeff_file)    
        coeff_list.append(inputcoeff)

print "File Read Complete"
print "There are ",nfiles,"files"

# Give the user some information about the coefficients files (maximum order)
n1max = coeff_list[0].n1
n2max = coeff_list[0].n2

print "Maximum dimension of the coefficients is (",n1max,",",n2max,")"

n1plot = input("Which value of the first dimension to plot? ")
n2plot = input("Which value of the second dimension to plot? ")


# Generate array of coefficient values for (n1,n2) in all files

yvalues = []

for coeff in coeff_list:
    yvalues.append(coeff.coeff[n1plot,n2plot])
    
values = np.asarray(yvalues)

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel("Image No.")
ax.set_ylabel("Coefficient")
ax.plot(filenumbers,yvalues)
plt.show()
