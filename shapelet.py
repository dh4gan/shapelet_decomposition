# Written by Duncan Forgan, 6/2/14
# Simple object handles individual shapelet basis functions
# Calculates basis functions and allows them to be written to an image

import numpy as np
from scipy.misc import factorial

pi = 3.1415926

class shapelet(object):
    '''2D shapelet object for image decomposition'''
    
    def __init__(self, n1,n2,beta):
        '''Constructor for shapelet'''
        self.n1 = n1
        self.n2 = n2
        self.beta = beta
        self.beta1 = 1.0/beta
        
    def __str__(self):
        '''Prints out shapelet coefficients'''
        
        s = "Shapelet (n1 = %i, n2 = %i, beta = %.2f)" %(self.n1, self.n2, self.beta)
        return s    
        
    def calc_Hermite(self,x,n):
        '''Calculates Hermite Polynomial, given value of x and n'''
                
        coeff = np.zeros(n+1)        
        coeff[-1] = 1
        answer = np.polynomial.hermite.hermval(x,coeff)        
        return answer        
    
    def calc_basis_function(self,x,n):
        '''Calculates the basis function in dimension 1'''
        
        hermite = self.calc_Hermite(x,n)        
        basis = np.power(np.power(2,n)*np.sqrt(pi)*factorial(n),-0.5)*np.exp(-x*x/2)*hermite
        
        return basis    
        
    def calc_shapelet_function(self,x1,x2):
        basis1 = self.calc_basis_function(x1*self.beta1, self.n1)
        basis2 = self.calc_basis_function(x2*self.beta1, self.n2)
        
        answer = self.beta1*basis1*basis2
        
        return answer
    
    
    def add_to_image(self, image, coeff, offsetx=0.0, offsety=0.0):
        '''Adds the basis function to an image
        Can be added with or without an offset in x and y'''
        
        print 'Adding ',self, ' to image, offset: ',offsetx, offsety
        
        for i in range(image.nx):
            x1 = image.xmin + i*image.xscale + offsetx
            
            for j in range(image.ny):
                x2 = image.ymin + j*image.yscale + offsety
                                    
                image.array[i,j] = image.array[i,j] + coeff*self.calc_shapelet_function(x1, x2)
            
        
        
    def decompose_image(self,image):
        '''Finds the shapelet coefficient of an image'''
        
        shape_coeff = 0.0
        for i in range(image.nx):
            x1 = image.xmin + i*image.xscale
            
            for j in range(image.ny):
                x2 = image.ymin + j*image.yscale
                shape_coeff = shape_coeff+ image.array[i,j]*self.calc_shapelet_function(x1, x2)
                
                
        return shape_coeff
            
        
        