from abc import ABCMeta, abstractmethod
import numpy as np
from osgeo import gdal, osr, ogr
from pyflowline.classes.vertex import pyvertex
from pyflowline.classes.edge import pyedge
from pyflowline.classes.cell import pycell
from pyflowline.algorithms.auxiliary.gdal_functions import calculate_polygon_area

class pylatlon(pycell):
    #lIndex=0 
    nFlowline=0
    dLength=0.0
    dArea=0.0
    dX_center_meter=0.0
    dY_center_meter=0.0
    dLongitude_center_degree=0.0
    dLatitude_center_degree=0.0
    aEdge=None
    aVertex=None
    aFlowline=None

    pVertex_center = None

    lCellID  = -1
    aNeighbor=None #the global ID of all neighbors
    nNeighbor=-1

    def __init__(self, dLon, dLat, aEdge, aVertex):    
        nEdge = len(aEdge)
        if nEdge != 4:
            pass
        else:
            
                
            self.aEdge = aEdge
            self.aVertex = aVertex #the first one and last one are the same
            self.nEdge = 4
            self.nVertex = 4                 

            self.dLongitude_center_degree = dLon
            self.dLatitude_center_degree = dLat

            pVertex = dict()        
            pVertex['dLongitude_degree'] =self.dLongitude_center_degree
            pVertex['dLatitude_degree'] =self.dLatitude_center_degree           
            self.pVertex_center = pyvertex(pVertex)

            self.lCellID_downstream_burned=-1
            self.iStream_order_burned=-1
            self.iStream_segment_burned=-1
            self.dElevation=-9999.0

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
        lons=list()
        lats=list()
        
        for i in range(self.nVertex):
            
            lons.append( self.aVertex[i].dLongitude_degree )
            lats.append( self.aVertex[i].dLatitude_degree )


        self.dArea = calculate_polygon_area( lons ,lats)

        
        return self.dArea

    def calculate_edge_length(self):
        dArea = self.dArea
        dLength_edge = np.sqrt(   dArea   )
        self.dLength = dLength_edge
        return dLength_edge

    def share_edge(self, other):
        iFlag_share = 0
        for pEdge in self.aEdge:
            for pEdge2 in other.aEdge:
                if pEdge.is_overlap(pEdge2) ==1 :
                    iFlag_share =1 
                    break


        return iFlag_share
