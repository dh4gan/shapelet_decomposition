import numpy as np
import matplotlib.pyplot as plt

class image(object):
    '''Simple 2D image object for shapelet decomposition'''
    
    def __init__(self,array, xmin,xmax,ymin,ymax):
        '''Constructor for image'''
        self.array = array # 2D numpy array
        self.nx = array.shape[0] # number of x pixels
        self.ny = array.shape[1] # number of y pixels
        
        self.xmin = xmin  # Image boundaries (x,y)
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        
        self.xscale = (self.xmax-self.xmin)/self.nx  # Pixel scales        
        self.yscale = (self.ymax-self.ymin)/self.ny
        
        self.x = np.linspace(self.xmin,self.xmax,num=self.nx) # x and y values
        self.y = np.linspace(self.ymin,self.ymax,num=self.ny)
        
        self.find_centre_pixel()                
        self.find_centre()
                                        
    def __str__(self):
        '''Prints out image coefficients'''
        
        s = "Image (%i x %i), centre: (%i,%i)" %(self.nx,self.ny,self.xc,self.yc)
        return s    
    
    def clone(self):
        '''Returns a copy of itself'''        
        return image(self.array,self.xmin,self.xmax,self.ymin,self.ymax)
        
    def find_centre_pixel(self):
        '''Finds centre pixel given nx,ny'''        
        self.ixcentre = self.nx/2 - 1  
        self.iycentre = self.ny/2 - 1

    def find_centre(self):
        '''Finds centre x,y, given centre pixels'''
        self.xcentre = self.xmin + self.ixcentre*self.xscale
        self.ycentre = self.ymin + self.iycentre*self.yscale 
        
    def centroid(self):
        '''Finds centroid x,y'''
        
        xcen = 0.0
        ycen = 0.0
        
        fluxtot = self.total_flux()
        
        for ix in range(self.nx):
            for iy in range(self.ny):
                x= self.xmin + ix*self.xscale
                y= self.ymin + iy*self.yscale
                
                xcen = xcen + x*self.array[ix,iy]
                ycen = ycen + y*self.array[ix,iy]
        
        xcen = xcen/fluxtot
        ycen = ycen/fluxtot
        
        return xcen,ycen
        
    def total_flux(self):
        '''Finds total flux in image'''
        
        fluxtot = 0.0
        for ix in range(self.nx):
            for iy in range(self.ny):
                fluxtot = fluxtot + self.array[ix,iy]
                                
        return fluxtot
    
    def subtract(self,other):
        '''Subtracts image other from image self'''   
        
        for ix in range(self.nx):
            for iy in range(self.ny):                                
                self.array[ix,iy] = self.array[ix,iy] - other.array[ix,iy]                                
        
    
    def gaussian_blur(self, sigma):
        '''Generates a gaussian blur on each pixel, with width sigma'''
        print "Applying Gaussian blur of standard deviation ", sigma
        # Convert sigma into pixels
        
        if(np.sum(self.array)==0.0):
            print "Image has no non-zero pixels: skipping blur command"
            return
        
        sigmapix = sigma/np.minimum(self.xscale,self.yscale)
        sigmapix = int(sigmapix)
        
        domain = 3*sigmapix # Region around each pixel to apply smoothing from        
        
        oldarray = np.copy(self.array) # Store unblurred image        
        self.array[:,:] = 0.0
                
        counter = 10
        for ix1 in range(self.nx):
            
            percent = 100.0*float(ix1)/float(self.nx)
            if(percent > counter):
                print counter, "% complete"
                counter +=10       
                 
            for iy1 in range(self.ny):
                
                # Select pixels within 6 sigma of ix1,iy1 - add contributions
                for ix in range(ix1-domain, ix1+domain):                    
                    for iy in range(iy1-domain, iy1+domain):
                        if(ix>0 and ix <self.nx and iy >0 and iy <self.ny): # if (ix,iy) pixel is inside image
                            x = ix - ix1
                            y = iy - iy1
                            gauss = np.exp(-(x^2+y^2)/(2.0*sigmapix*sigmapix))/(2.0*np.pi*sigmapix*sigmapix)  
                            #print ix,iy, x,y, gauss, oldarray[ix,iy]                          
                            self.array[ix1,iy1] += oldarray[ix,iy]*gauss
        
        # Normalise image so that it has the correct sum
        self.array[:,:] = self.array[:,:]*np.sum(oldarray)/np.sum(self.array)
        
        return            
                
    def load_image(self,inputfile):
        '''Loads an image from a simple ASCII file'''
    
        f = open(inputfile,'r')
    
        header = f.readline()
        headernums = header.split()
    
        self.xmin = float(headernums[2])
        self.xmax = float(headernums[3])
        self.ymin = float(headernums[4])
        self.ymax = float(headernums[5])
    
        self.array = np.genfromtxt(inputfile,skiprows=1)
        
        self.nx = self.array.shape[0]
        self.ny = self.array.shape[1]
        self.xscale = (self.xmax-self.xmin)/self.nx        
        self.yscale = (self.ymax-self.ymin)/self.ny
        
        self.x = np.linspace(self.xmin,self.xmax,num=self.nx)
        self.y = np.linspace(self.ymin,self.ymax,num=self.ny)
        
        self.find_centre_pixel()                
        self.find_centre()
                
    def plot_image(self):
        '''plots an image'''                        
        plt.pcolor(self.x, self.y, self.array.T, vmin = np.amin(self.array), vmax = np.amax(self.array))
        plt.colorbar()
        plt.show()
    
    def write_to_file(self,outputfile):
        ''' Writes image to a simple ASCII text format'''
        
        headers = [self.nx,self.ny,self.xmin,self.xmax,self.ymin,self.ymax]        
        
        line = ''
        
        for item in headers:
            line = line+str(item)+'\t'
              
        line = line +'\n'
        f = open(outputfile, 'w')
        f.write(line)
        f.close()
              
        f = open(outputfile, 'a')
        np.savetxt(f, self.array, fmt='%.4e', delimiter = '  ',newline='\n')
        
        
    
        
        