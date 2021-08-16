import os
from pystream.shared.vertex import pyvertex

from pystream.format.read_flowline_shapefile import read_flowline_shapefile
from pystream.format.read_mesh_shapefile import read_mesh_shapefile
from pystream.format.read_flowline_geojson import read_flowline_geojson
from pystream.format.export_flowline_to_shapefile import export_flowline_to_shapefile

from pystream.algorithm.intersect.intersect_flowline_with_mesh import intersect_flowline_with_mesh

from pystream.algorithm.simplification.remove_returning_flowline import remove_returning_flowline
from pystream.algorithm.simplification.remove_duplicate_flowline import remove_duplicate_flowline
from pystream.algorithm.simplification.remove_duplicate_edge import remove_duplicate_edge
from pystream.algorithm.direction.correct_flowline_direction import correct_flowline_direction
from pystream.algorithm.loop.remove_flowline_loop import remove_flowline_loop
from pystream.algorithm.split.find_flowline_vertex import find_flowline_vertex
from pystream.algorithm.split.find_flowline_confluence import find_flowline_confluence
from pystream.algorithm.split.split_flowline import split_flowline
from pystream.algorithm.split.split_flowline_to_edge import split_flowline_to_edge
from pystream.format.export_vertex_to_shapefile import export_vertex_to_shapefile
from pystream.algorithm.merge.merge_flowline import merge_flowline

from pystream.algorithm.index.define_stream_order import define_stream_order
from pystream.algorithm.index.define_stream_segment_index import define_stream_segment_index

def intersect_flowline_with_mesh_with_postprocess_op(oModel_in):

    iFlag_projected = 0

    iMesh_type = oModel_in.iMesh_type

    sWorkspace_output = oModel_in.sWorkspace_output  

    sFilename_flowlinw_raw = oModel_in.sFilename_flowlinw_raw


    aFlowline, pSpatialRef_flowline = read_flowline_shapefile(sFilename_flowlinw_raw)
    

    sFilename_flowline = oModel_in.sFilename_flowline_segment_order_before_intersect

    sFilename_mesh=oModel_in.sFilename_mesh
    aMesh, pSpatialRef_mesh = read_mesh_shapefile(sFilename_mesh)
    sFilename_flowline_intersect = oModel_in.sFilename_flowline_intersect

    
    aCell, aCell_intersect, aFlowline_intersect_all = intersect_flowline_with_mesh(iMesh_type, sFilename_mesh, sFilename_flowline, sFilename_flowline_intersect)


    point= dict()
    
    point['x'] = oModel_in.dx_outlet
    point['y'] = oModel_in.dy_outlet
    pVertex_outlet=pyvertex(point)
    
    aFlowline, aFlowline_no_parallel, lCellID_outlet = remove_returning_flowline(iMesh_type, aCell_intersect, pVertex_outlet)
    sFilename_out = 'flowline_simplified_after_intersect.shp'
    sFilename_out = os.path.join(sWorkspace_output, sFilename_out)  


    if iMesh_type ==4:
        pSpatialRef=  pSpatialRef_mesh
        pass
    else:
        pSpatialRef = pSpatialRef_flowline
        pass

    export_flowline_to_shapefile(iFlag_projected, aFlowline, pSpatialRef, sFilename_out)
    
    pVertex_outlet=aFlowline[0].pVertex_end
    aVertex = find_flowline_vertex(aFlowline)
    
    sFilename_out = 'flowline_vertex_without_confluence_after_intersect.shp'
    sFilename_out = os.path.join(sWorkspace_output, sFilename_out)
    export_vertex_to_shapefile(iFlag_projected, aVertex, pSpatialRef, sFilename_out)
    
    aFlowline = split_flowline(aFlowline, aVertex)
    sFilename_out = 'flowline_split_by_point_after_intersect.shp'
    sFilename_out = os.path.join(sWorkspace_output, sFilename_out)
    export_flowline_to_shapefile(iFlag_projected, aFlowline, pSpatialRef, sFilename_out)
    aFlowline= correct_flowline_direction(aFlowline,  pVertex_outlet )


    
    aFlowline = remove_flowline_loop(  aFlowline )    
    sFilename_out = 'flowline_remove_loop_after_intersect.shp'
    sFilename_out = os.path.join(sWorkspace_output, sFilename_out)
    export_flowline_to_shapefile(iFlag_projected, aFlowline, pSpatialRef, sFilename_out)


    aFlowline, aEdge = split_flowline_to_edge(aFlowline)
    #aEdge = remove_duplicate_edge(aEdge)
    aFlowline = remove_duplicate_flowline(aFlowline)

    aVertex, lIndex_outlet, aIndex_headwater,aIndex_middle, aIndex_confluence, aConnectivity\
        = find_flowline_confluence(aFlowline,  pVertex_outlet)

    aFlowline = merge_flowline( aFlowline,aVertex, pVertex_outlet, aIndex_headwater,aIndex_middle, aIndex_confluence  )  
    aFlowline, aStream_segment = define_stream_segment_index(aFlowline)
    aFlowline, aStream_order = define_stream_order(aFlowline)
    
    sFilename_out = 'flowline_final.shp'
    sFilename_out = os.path.join(sWorkspace_output, sFilename_out)
    export_flowline_to_shapefile(iFlag_projected, aFlowline, pSpatialRef, sFilename_out)

    return aCell, aCell_intersect, aFlowline, lCellID_outlet








