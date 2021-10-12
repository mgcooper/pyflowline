from abc import ABCMeta, abstractmethod
import numpy as np

from pyearth.gis.location.calculate_distance_based_on_lon_lat import calculate_distance_based_on_lon_lat
class pyvertex(object):
    __metaclass__ = ABCMeta  
    lVertexID=-1
    dx=-9999
    dy=-9999
    dz=-9999
    dLongitude=0.0
    dLatitude=0.0
    dElevation=0.0
    lIndex=-1 #this index will be used for array
    def __init__(self, aParameter):
        if 'x' in aParameter:            
            self.dx             = float(aParameter['x'])
        
        if 'y' in aParameter:            
            self.dy             = float(aParameter['y'])
        
        if 'z' in aParameter:            
            self.dz             = float(aParameter['z'])
        
        #if 'lon' in aParameter:            
        self.dLongitude      = float(aParameter['lon'])
        
        #if 'lat' in aParameter:            
        self.dLatitude       = float(aParameter['lat'])

        
        return
    
    def __eq__(self, other):
        iFlag = -1
        
        c = self.calculate_distance(other)
        if( c < 0.001 ): #be careful
            iFlag = 1
        else:
            iFlag = 0       

        return iFlag

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def calculate_distance(self, other):
        
        x1 = self.dx
        y1 = self.dy
        z1 = self.dz
        lon1 = self.dLongitude
        lat1 = self.dLatitude
        
        x2 = other.dx
        y2 = other.dy
        z2 = other.dz
        lon2 = other.dLongitude
        lat2 = other.dLatitude

        #if x1!=-9999 and x2!=-9999:
        #    a = (x1-x2) * (x1-x2)
        #    b = (y1-y2) * (y1-y2)
        #    c = np.sqrt(a+b)
        #else:
        #    #use latitude longitude
        #    pass

        c= calculate_distance_based_on_lon_lat(lon1,  lat1, lon2, lat2)

        dDistance = c

        return dDistance

  

