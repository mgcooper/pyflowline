from abc import ABCMeta, abstractmethod
import numpy as np

from osgeo import gdal, osr, ogr
from pystream.shared.vertex import pyvertex
from pystream.shared.edge import pyedge
from pystream.shared.cell import pycell
from pystream.add_unique_vertex import add_unique_vertex

class pyhexagon(pycell):
    lIndex=0    
    nFlowline=0
    dLength=0.0
    dArea=0.0
    dX_center=0.0
    dY_center=0.0
    aEdge=None
    aVertex=None
    aFlowline=None

    def __init__(self, aEdge, aVertex):    

        nEdge = len(aEdge)
        if nEdge != 6:
            pass
        else:
            
                
            self.aEdge = aEdge
            self.aVertex = aVertex #the first one and last one are the same
            self.nEdge = 6
            self.nVertex = 6

            dx=0.0
            dy=0.0
            for i in range(6):
                dx = dx + aVertex[i].dx
                dy = dy + aVertex[i].dy
                pass

            self.dX_center = dx/6.0
            self.dY_center = dy/6.0

            pass
        pass
    
    def has_this_edge(self, pEdge_in):
        iFlag_found = 0
        for pEdge in self.aEdge:
            if pEdge.is_overlap(pEdge_in):
                iFlag_found =1 
                break
            else:
                pass
        
        
        return iFlag_found
    def which_edge_cross_this_vertex(self, pVertex_in):
        iFlag_found = 0
        pEdge_out = None
        for pEdge in self.aEdge:
            if( pEdge.check_vertex_on_edge(pVertex_in) ==1 ):
                iFlag_found =1
                pEdge_out = pEdge
                break

            else:
                pass

        return iFlag_found, pEdge_out
    
    def calculate_cell_area(self):
        dLength_edge = self.dLength

        #dLength_edge = np.sqrt(  2.0 * dArea / (3.0* np.sqrt(3.0))  )
        dArea = dLength_edge * dLength_edge * (3.0* np.sqrt(3.0)) /2.0

        self.dArea = dArea
        return dArea
    def calculate_edge_length(self):
        dArea = self.dArea
        dLength_edge = np.sqrt(  2.0 * dArea / (3.0* np.sqrt(3.0))  )
        self.dLength = dLength_edge
        return dLength_edge

