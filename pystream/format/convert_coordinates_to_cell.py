import os
import json
from pystream.shared.square import pysquare
from pystream.shared.edge import pyedge
from osgeo import ogr, osr, gdal, gdalconst
import numpy as np

from shapely.geometry import Point, LineString, MultiLineString
from shapely.wkt import loads

from pystream.shared.vertex import pyvertex
from pystream.shared.flowline import pyflowline
from pystream.shared.hexagon import pyhexagon
from pystream.shared.square import pysquare
from pystream.shared.latlon import pylatlon
from pystream.shared.mpas import pympas
from pystream.shared.tin import pytin

def convert_gcs_coordinates_to_cell(iMesh_type, aCoordinates_gcs):
    npoint = len(aCoordinates_gcs)    
    aVertex=list()              
    aEdge=list()    
    for i in range(npoint):
        x = aCoordinates_gcs[i][0]
        y = aCoordinates_gcs[i][1]
        dummy = dict()
        dummy['lon'] = x
        dummy['lat'] = y
        pVertex = pyvertex(dummy)
        aVertex.append(pVertex)
    for j in range(npoint-1):
        pEdge = pyedge( aVertex[j], aVertex[j+1] )
        aEdge.append(pEdge)

    if iMesh_type ==1: #hexagon
        

        pHexagon = pyhexagon( aEdge, aVertex)
        return pHexagon
    else:
        if iMesh_type ==2: #sqaure
            pSquare = pysquare( aEdge, aVertex)
            return pSquare
        else:
            if iMesh_type ==3: #latlon
                pLatlon = pylatlon( aEdge, aVertex)
                return pLatlon
            else:
                if iMesh_type ==4: #mpas       
                    pMpas = pympas( aEdge, aVertex)
                    return pMpas
                else:
                    if iMesh_type ==5: #tin
                        pTin = pytin( aEdge, aVertex)
                        return pTin
                        pass
                    else:
                        print('What mesh type are you using?')
                        return None

def convert_pcs_coordinates_to_cell(iMesh_type, aCoordinates_pcs):
    npoint = len(aCoordinates_pcs)    
    aVertex=list()              
    aEdge=list()    
    for i in range(npoint):
        x = aCoordinates_pcs[i][0]
        y = aCoordinates_pcs[i][1]
        dummy = dict()
        dummy['x'] = x
        dummy['y'] = y
        pVertex = pyvertex(dummy)
        aVertex.append(pVertex)
    for j in range(npoint-1):
        pEdge = pyedge( aVertex[j], aVertex[j+1] )
        aEdge.append(pEdge)

    if iMesh_type ==1: #hexagon     

        pHexagon = pyhexagon( aEdge, aVertex)
        return pHexagon
    else:
        if iMesh_type ==2: #sqaure
            pSquare = pysquare( aEdge, aVertex)
            return pSquare
        else:
            if iMesh_type ==3: #latlon
                pLatlon = pylatlon( aEdge, aVertex)
                return pLatlon
            else:
                if iMesh_type ==4: #mpas   

                    pMpas = pympas( aEdge, aVertex)
                    return pMpas
                else:
                    if iMesh_type ==5: #tin
                        pTin = pytin( aEdge, aVertex)
                        return pTin
                        pass
                    else:
                        print('What mesh type are you using?')
                        return None
