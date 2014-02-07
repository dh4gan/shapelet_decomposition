# Written 7/2/14 by D Forgan
# A collection of functions designed to make shapelet decomposition quick

import image as im
import shapelet as sh
import numpy as np
import matplotlib.pyplot as plt

def load_image(inputfile):
    '''This creates an image object from a simple ASCII file'''
    
    f = open(inputfile,'r')
    
    header = f.readline()
    headernums = header.split()
    
    xmin = float(headernums[2])
    xmax = float(headernums[3])
    ymin = float(headernums[4])
    ymax = float(headernums[5])
    
    array = np.genfromtxt(inputfile,skiprows=1)
    
    thisimage = im.image(array, xmin,xmax,ymin,ymax)
    
    return thisimage

def plot_image(inputfile):
    '''plots an image (TODO)'''

def get_shapelet_coefficients(image, nmax, beta):
    '''Takes an image and returns the shapelet coefficients up to a maximum n'''
    
    # Now do decomposition
    n1max = np.int(nmax/2)
    n2max = n1max
    decomposed = np.zeros((n1max,n2max))

    print 'Decomposing Image '
    print 'Maximum Order: ',nmax
    print 'Scale Factor: ',beta
    for ni in range(n1max):
        for nj in range(n2max):
            shape = sh.shapelet(ni,nj,beta)
            print shape            
            decomposed[ni,nj] = shape.decompose_image(image)
                
    return decomposed

def make_shapelet_gallery(image, nmax, beta):
    '''Makes a gallery of shapelets in a single image (TODO)'''


def make_image_from_coefficients(image, coeff,nmax,beta):
    
    print 'Reconstructing image from shapelet_coefficients'
    image.array[:,:] = 0.0
    
    n1max = np.int(nmax/2)
    n2max = n1max
    
    for ni in range(n1max):
        for nj in range(n2max):
            shape=sh.shapelet(ni,nj,beta)
            shape.add_to_image(image,coeff[ni,nj])

    