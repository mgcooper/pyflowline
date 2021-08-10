from pystream.shared.edge import pyedge
from pystream.shared.flowline import pyflowline
from pystream.shared.link import pympaslink

def export_flowline_info_to_json(aCell_intersect_in, aFlowline_in, sFilename_json_out):
    
    #export the flowline topology to json

    ncell= len(aCell_intersect_in)
    nflowline= len(aFlowline_in)

    


    with open(sFilename_json_out, 'w', encoding='utf-8') as f:

        for i in range(1, nflowline+1):

            pFlowline = aFlowline_in[i-1]

            nVertex = pFlowline.nVertex
            nEdge = pFlowline.nEdge
            for j in range(1, nEdge+1):
             
                pEdge = pFlowline.aEdge[j-1]
                pVertex_start = pEdge.pVertex_start
                pVertex_end = pEdge.pVertex_end

                for k in range(ncell):
                    if aCell_intersect_in[k].pVertex_center == pVertex_start:
                        pMpas_start = aCell_intersect_in[k]
                        pass

                    if aCell_intersect_in[k].pVertex_center == pVertex_end:
                        pMpas_end = aCell_intersect_in[k]
                        pass

                pEdge_link = pyedge(pVertex_start, pVertex_end)  
                          
                
                pLink = pympaslink(pMpas_start, pMpas_end, pEdge_link)
                sJson = pLink.export_to_json()
            
                f.write(sJson)

        f.close()
    
    return

    
   