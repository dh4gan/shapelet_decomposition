import numpy as np


class image(object):
    '''Simple 2D image object for shapelet decomposition'''
    
    def __init__(self,array, xmin,xmax,ymin,ymax):
        '''Constructor for image'''
        self.array = array # 2D numpy array
        self.nx = array.shape[0] # number of x pixels
        self.ny = array.shape[1] # number of y pixels
        
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        
        self.xscale = (self.xmax-self.xmin)/self.nx        
        self.yscale = (self.ymax-self.ymin)/self.ny
        
        self.x = np.linspace(self.xmin,self.xmax,num=self.nx)
        self.y = np.linspace(self.ymin,self.ymax,num=self.ny)
        
        self.find_centre_pixel()                
        self.find_centre()
                                        
    def __str__(self):
        '''Prints out image coefficients'''
        
        s = "Image (%i x %i), centre: (%i,%i)" %(self.nx,self.ny,self.xc,self.yc)
        return s    
        
    def find_centre_pixel(self):        
        self.xc = self.nx/2 - 1
        self.yc = self.ny/2 - 1

    def find_centre(self):
        self.xcentre = self.xmin + self.xc*self.xscale
        self.ycentre = self.ymin + self.yc*self.yscale 