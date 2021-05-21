from abc import ABCMeta, abstractmethod
import json
from numpy.lib.function_base import average
import copy
from osgeo import gdal, osr, ogr
from pystream.shared.vertex import pyvertex
from pystream.shared.edge import pyedge

class pyflowline(object):
    __metaclass__ = ABCMeta 
    aEdge=None
    aVertex=None

    dLength=0.0

    lIndex=-1
    lIndex_upstream=-1
    lIndex_downstream=-1

    nEdge=0
    nVertex=0

    def __init__(self, aEdge):    
        self.aEdge = aEdge
        nEdge  = len(aEdge)
        self.nEdge = nEdge
        self.pVertex_start = aEdge[0].pVertex_start
        self.pVertex_end =  aEdge[ nEdge-1  ].pVertex_end

        nVertex = nEdge +1
        self.aVertex=list()
        for i in range(nEdge):
            self.aVertex.append( aEdge[i].pVertex_start )
            pass

        self.aVertex.append( aEdge[nEdge-1].pVertex_end )
        self.nVertex = nVertex

        return

    def calculate_length(self):
        dLength =0.0
        #loop though
        for edge in self.aEdge:
            edge.calculate_length()
            dLength = dLength + edge.dLength

        #assing
        self.dLength= dLength

        return dLength

    
    
    def check_upstream(self, other):
        iFlag_upstream =-1
        v0 = self.pVertex_start
        v1 = self.pVertex_end

        v2 = other.pVertex_start
        v3 = other.pVertex_end

        if v0 == v3:
            iFlag_upstream =1
        else:
            iFlag_upstream=0

        return iFlag_upstream

    def check_downstream(self, other):
        iFlag_downstream =-1
        v0 = self.pVertex_start
        v1 = self.pVertex_end

        v2 = other.pVertex_start
        v3 = other.pVertex_end

        if v1 == v2:
            iFlag_downstream =1
        else:
            iFlag_downstream=0

        return iFlag_downstream
    
    def reverse(self):
        '''
        reverse the direction of a flowline
        '''
        aVertex = self.aVertex 
        nVertex = self.nVertex
        aVertex_new = list()
        for i in range(nVertex-1,-1,-1) :
            aVertex_new.append( aVertex[i] )

        self.aVertex = aVertex_new
        nVertex  = len(aVertex)
        aEdge = list()
        for i in range(nVertex-1):
            pEdge = pyedge( self.aVertex[i], self.aVertex[i+1] )
            aEdge.append(pEdge)
            pass
        
        self.aEdge = aEdge
        nEdge = len(aEdge)
        self.pVertex_start = aEdge[0].pVertex_start
        self.pVertex_end =  aEdge[ nEdge-1  ].pVertex_end

    def merge_upstream(self, other):
        pFlowline_out = copy.deepcopy(other)    

        pVertex_start1 = other.pVertex_start
        pVertex_end1 = other.pVertex_end
        nVertex1 = other.nVertex
        nEdge1 = other.nEdge

        pVertex_start2 = self.pVertex_start
        pVertex_end2 = self.pVertex_end
        nVertex2 = self.nVertex
        nEdge2 = self.nEdge


        if pVertex_end1 == pVertex_start2:
            #this is the supposed operation because they should connect

            nVertex = nVertex1 + nVertex2 - 1
            nEdge = nVertex -1 
            aEdge = copy.deepcopy(other.aEdge )
            for i in range(nEdge2):
                aEdge.append( self.aEdge[i] )
                pass

            aVertex = copy.deepcopy(other.aVertex)
            for i in range(1, nVertex2):
                aVertex.append( self.aVertex[i] )
                pass

            pFlowline_out.aEdge = aEdge
            pFlowline_out.aVertex = aVertex
            pFlowline_out.nEdge = nEdge
            pFlowline_out.nVertex = nVertex
            pFlowline_out.dLength = self.dLength + other.dLength
            pFlowline_out.pVertex_start = pVertex_start1
            pFlowline_out.pVertex_end = pVertex_end2

            pass
        else:
            pass

        return pFlowline_out
        