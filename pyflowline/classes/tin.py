import json
from json import JSONEncoder
import numpy as np

from pyflowline.classes.vertex import pyvertex
from pyflowline.classes.edge import pyedge
from pyflowline.classes.cell import pycell
from pyflowline.classes.flowline import pyflowline

class TINClassEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, list):
            pass  
        if isinstance(obj, pyvertex):
            return json.loads(obj.tojson()) 
        if isinstance(obj, pyedge):
            return obj.lEdgeID        
        if isinstance(obj, pyflowline):
            return obj.lFlowlineID
        if isinstance(obj, pytin):
            return obj.lCellID     
        return JSONEncoder.default(self, obj)

class pytin(pycell):   
    """tin class

    Args:
        pycell (_type_): _description_

    Returns:
        _type_: _description_
    """

    nFlowline=0
    nVertex =0 
    nEdge=0
    dLength=0.0
    dArea=0.0
    dX_center_meter=0.0
    dY_center_meter=0.0
    aEdge=None
    aVertex=None
    aFlowline=None
    lCellID  = -1
    aNeighbor=None #the global ID of all neighbors
    nNeighbor_land_virtual = -1
    aNeighbor_land_virtual = None
    nNeighbor=-1

    aNeighbor_distance = None
    pBound=None

    def __init__(self, aEdge,aVertex, dLon, dLat):       
        nEdge = len(aEdge)
        if nEdge !=3:
            pass
        else:           
            self.aEdge = aEdge
            self.aVertex = aVertex #the first one and last one are the same
            self.nEdge = len(aEdge)
            self.nVertex = len(aVertex) - 1
            self.dLongitude_center = dLon
            self.dLatitude_center = dLat
            pVertex = dict()        
            pVertex['lon'] =self.dLongitude_center
            pVertex['lat'] =self.dLatitude_center           
            self.pVertex_center = pyvertex(pVertex)
            self.calculate_cell_bound() #bound for rtree 
            pass
        pass    
    def calculate_cell_bound(self):
        dLat_min = 90
        dLat_max = -90
        dLon_min = 180
        dLon_max = -180
        for i in range(self.nVertex):
            dLon_max = np.max( [dLon_max, self.aVertex[i].dLongitude_degree] )
            dLon_min = np.min( [dLon_min, self.aVertex[i].dLongitude_degree] )
            dLat_max = np.max( [dLat_max, self.aVertex[i].dLatitude_degree] )
            dLat_min = np.min( [dLat_min, self.aVertex[i].dLatitude_degree] )
        
        self.pBound = (dLon_min, dLat_min, dLon_max, dLat_max)
        return self.pBound
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
            iFlag, dummy ,diff = pEdge.check_vertex_on_edge(pVertex_in)
            if( iFlag ==1 ):
                iFlag_found =1
                pEdge_out = pEdge
                break
            else:
                pass

        return iFlag_found, pEdge_out
    
    def calculate_cell_area(self):           
        #self.dArea = 0.0
        return self.dArea

    def calculate_edge_length(self):        
        self.dLength_edge =0.0
        return self.dLength_edge
    
    def share_edge(self, other):
        iFlag_share = 0
        for pEdge in self.aEdge:
            for pEdge2 in other.aEdge:
                if pEdge.is_overlap(pEdge2) ==1 :
                    iFlag_share = 1 
                    break

        return iFlag_share

    def tojson(self):
        """
        Convert a tin object to a json string

        Returns:
            json str: A json string
        """
        aSkip = ['aEdge', \
                'aFlowline']
        obj = self.__dict__.copy()
        for sKey in aSkip:
            obj.pop(sKey, None)
        sJson = json.dumps(obj, \
            sort_keys=True, \
            indent = 4, \
            ensure_ascii=True, \
            cls=TINClassEncoder)
        return sJson
