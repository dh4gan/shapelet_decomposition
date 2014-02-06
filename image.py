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
        self.find_centre()                
                                        
    def __str__(self):
        '''Prints out image coefficients'''
        
        s = "Image (%i x %i), centre: (%i,%i)" %(self.nx,self.ny,self.xc,self.yc)
        return s
    
    def load_image(self,array):
        self.array = array
        self.nx = array.shape[0]
        self.ny = array.shape[1]
        self.find_centre()
        
        
    def find_centre(self):        
        self.xc = self.nx/2 - 1
        self.yc = self.ny/2 - 1
        