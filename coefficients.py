# Written by Duncan Forgan, 6/2/14
# This object handles the coefficients of a shapelet decomposition

import numpy as np
import shapelet as sh
import image as im
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from string import split

from scipy.misc import comb

pi = 3.1415926

class coefficients(object):
    '''2D shapelet coefficients object for image decomposition'''
    
    def __init__(self, nmax,beta):
        '''Constructor for shapelet coefficients'''
        self.nmax = nmax        
        self.n1 = np.int(nmax/2)
        self.n2 = np.int(nmax/2)
        self.beta = beta
        self.beta1 = 1.0/beta
        self.coeff = np.zeros((self.n1,self.n2))
        
    def __str__(self):
        '''Prints out shapelet coefficients'''
        
        s = "Shapelet Coefficients: \n "
        
        for ix in range(self.n1):
            for iy in range(self.n2):
                s = s + "  "+str(self.coeff[ix,iy])
            s = s + '\n'
            
        return s
    
    def create_shapelet(self,i1,i2):
        '''Returns a shapelet object for indices i1,i2'''
        
        shape= sh.shapelet(i1,i2,self.beta)
        shape.set_coefficient(self.coeff[i1,i2])
        
        return shape   
    
    def plot_coefficients(self, outputfile, outputformat):
        '''Uses matplotlib.pcolor to plot coefficients
        and save to file outputfile (format outputformat)'''
        
        fig1 = plt.figure()
        ax = fig1.add_subplot(111)
    
        ax.set_xlim(0,self.n1)
        ax.set_ylim(0,self.n2)
        ax.set_xlabel('$n_1$')
        ax.set_ylabel('$n_2$')    
    
        plt.pcolor(self.coeff,cmap='rainbow', vmin = np.amin(self.coeff), vmax = np.amax(self.coeff))
        plt.colorbar()
        plt.show()                
      
        
    def get_from_image(self,image):
        '''Derives shapelet coefficients from image'''                

        print 'Decomposing Image '
        print 'Maximum Order: ',self.nmax
        print 'Scale Factor: ',self.beta
        for ni in range(self.n1):
            for nj in range(self.n2):
                shape = self.create_shapelet(ni, nj)
                print shape            
                self.coeff[ni,nj] = shape.decompose_image(image)
    
    
    def centroid(self):
        '''Find the centroid x and y from these coefficients'''
        
        xcen = 0.0
        ycen = 0.0
        
        fluxtot = self.total_flux()
        
        for i1 in range(self.n1):            
            if i1%2==0: continue #consider odd i1
                            
            for i2 in range(self.n2):                    
                if i2%2!=0: continue # consider even i2
                                                                        
                xcen = xcen + np.power(i1+1,0.5)*np.power(2,0.5*(2-i1-i2))* np.power(comb(i1+1,(i1+1)/2)*comb(i2,i2/2),0.5)*self.coeff[i1,i2]
                    
                
        for i1 in range(self.n1):
            if i1%2!=0: continue #consider even i1   
                     
            for i2 in range(self.n2):
                if i2%2==0:continue # consider odd i2
                                                         
                ycen = ycen + np.power(i2+1,0.5)*np.power(2,0.5*(2-i2-i1))* np.power(comb(i2+1,(i2+1)/2)*comb(i1,i1/2),0.5)*self.coeff[i1,i2]
            
        xcen = xcen*np.sqrt(pi)*self.beta*self.beta/fluxtot                    
        ycen = ycen*np.sqrt(pi)*self.beta*self.beta/fluxtot
                
        return xcen,ycen
        
    def total_flux(self):
        '''Find the total flux from these coefficients'''
        fluxtot = 0.0
        
        for i1 in range(self.n1):
            if i1%2!=0: continue #skip odd i1
            
            for i2 in range(self.n2):
                if i2%2!=0: 
                    continue #skip odd i2                
                fluxtot = fluxtot + np.power(2,0.5*(2-i1-i2))*np.power(comb(i1,i1/2)*comb(i1,i2/2),0.5)*self.coeff[i1,i2]
                
        fluxtot = fluxtot*np.sqrt(pi)*self.beta
                                                           
        return fluxtot
        
    def rms_radius(self):
        '''Find the RMS radius from these coefficients'''
                
        rmsrad = 0.0
        fluxtot = self.total_flux()
        
        for i1 in range(self.n1):
            if i1%2!=0: continue #skip odd i1
            
            for i2 in range(self.n2):
                if i2%2!=0: 
                    continue #skip odd i2                
                rmsrad = rmsrad + np.power(2,0.5*(4-i1-i2))*(1+i1+i2)*np.power(comb(i1,i1/2)*comb(i1,i2/2),0.5)*self.coeff[i1,i2]
                
        rmsrad = rmsrad*np.sqrt(pi)*self.beta*self.beta*self.beta/fluxtot
                                                           
        return rmsrad      
                
    def make_image_from_coefficients(self,image):
        '''Takes shapelet coefficients and constructs an image'''
        
        print 'Reconstructing image from shapelet_coefficients'
        image.array[:,:] = 0.0            
    
        for ni in range(self.n1):
            for nj in range(self.n2):
                shape=self.create_shapelet(ni, nj)
                shape.add_to_image(image)     
                
    def make_gallery_from_coefficients(self,norm=False):
        '''Creates a gallery of shapelets according to their coefficients
        If Norm set to true, all shapelets plotted as if coefficients are unity'''
        
        xmin = 0.0
        xmax = self.n1*self.n2
        ymin = xmin
        ymax = xmax
        
        nx = 100
        ny = 100
        
        array = np.zeros((nx,ny))
        
        image = im.image(array, xmin,xmax,ymin,ymax)
        image.array[:,:] =0.0
        
        for ni in range(self.n1):
            for nj in range(self.n2):
                shape = self.create_shapelet(ni, nj)
                shape.add_to_image(image, offsetx = ni, offsety = nj)
                
        return image
    
    def write_to_file(self,outputfile):
        ''' Writes coefficients to a simple ASCII text format'''
        
        headers = [self.n1,self.n2,self.beta]        
        
        line = ''
        
        for item in headers:
            line = line+str(item)+'\t'
              
        line = line +'\n'
        f = open(outputfile, 'w')
        f.write(line)
        f.close()
              
        f = open(outputfile, 'a')
        np.savetxt(f, self.coeff, fmt='%.4e', delimiter = '  ',newline='\n')
        
    def read_from_file(self,inputfile):
        '''Reads coefficients from simple ASCII format'''
        
        f = open(inputfile,'r')
        line = f.readline()
        
        numbers = split(line)

        self.n1=int(numbers[0])
        self.n2 = int(numbers[1])
        self.beta = float(numbers[2])
        
        f.close()
        
        self.coeff = np.genfromtxt(inputfile, skiprows=1)
        
         
         
        
        
        