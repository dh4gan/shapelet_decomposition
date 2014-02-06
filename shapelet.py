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
        
        s = "Shapelet (n1 = %i, n2 = %i, beta = %f)" %(self.n1, self.n2, self.beta)
        return s    
        
    def calc_Hermite1(self,x):
        '''Calculates Hermite Polynomial for x1 axis, given value of x and n'''
                
        coeff = np.zeros(self.n1+1)        
        coeff[-1] = 1
        answer = np.polynomial.hermite.hermval(x,coeff)        
        return answer
    
    def calc_Hermite2(self,x):
        '''Calculates Hermite Polynomial for x1 axis, given value of x and n'''
        coeff = np.zeros(self.n2+1)
        coeff[-1] = 1
        answer = np.polynomial.hermite.hermval(x,coeff)        
        return answer      
    
    def calc_basis_function1(self,x):
        '''Calculates the basis function in dimension 1'''
        
        hermite = self.calc_Hermite1(x)        
        basis = np.power(np.power(2,self.n1)*np.sqrt(pi)*factorial(self.n1),-0.5)*np.exp(-x*x/2)*hermite
        
        return basis
    
    def calc_basis_function2(self,x):
        '''Calculates the basis function in dimension 1'''
        
        hermite = self.calc_Hermite2(x)        
        basis = np.power(np.power(2,self.n2)*np.sqrt(pi)*factorial(self.n2),-0.5)*np.exp(-x*x/2)*hermite
        
        return basis
        
    def calc_shapelet_function(self,x1,x2):
        basis1 = self.calc_basis_function1(x1*self.beta1)
        basis2 = self.calc_basis_function2(x2*self.beta1)
        
        answer = self.beta1*basis1*basis2
        
        return answer
    
    
    def add_to_image(self, image):
        '''Adds the basis function to an image'''
        
        for i in range(image.nx):
            x1 = i - image.xc
            
            for j in range(image.ny):
                x2 = j-image.yc
              
                #print x1,x2, self.calc_basis_function(x1, x2)              
                image.array[i,j] = image.array[i,j] + self.calc_shapelet_function(x1, x2)
            
        
        
    def decompose_image(self,image):
        '''Finds the shapelet coefficient of an image'''
        
        shape_coeff = 0.0
        for i in range(image.nx):
            x1 = i - image.xc
            
            for j in range(image.ny):
                x2 = j-image.yc
                
                
                
        return shape_coeff
            
        
        