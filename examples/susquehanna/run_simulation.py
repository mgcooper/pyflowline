import os, sys
from pathlib import Path
from os.path import realpath
import argparse
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time Pyflowline simulation started.')

from pyflowline.classes.pycase import flowlinecase
from pyflowline.pyflowline_read_model_configuration_file import pyflowline_read_model_configuration_file


sDate='20220630'


dataPath = str(Path(__file__).parents[2]) # data is located two dir's up
iFlag_option = 1
sWorkspace_data = realpath( dataPath +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  str(Path(sWorkspace_data)  /  'output')
sWorkspace_output=  '/compyfs/liao313/04model/pyflowline/susquehanna'
#an example configuration file is provided with the repository, but you need to update this file based on your own case study
aMesh_type = ['hexagon', 'square','latlon','mpas']
aResolution_meter = [5000, 10000, 50000]
iCase_index = 1
sPath = str( Path().resolve() )
sSlurm = 'short'



aExtent_full = [-78.5,-75.5, 39.2,42.5]

aExtent_meander = [-76.5,-76.2, 41.6,41.9] #meander
aExtent_braided = [-77.3,-76.5, 40.2,41.0] #braided
aExtent_confluence = [-77.3,-76.5, 40.2,41.0] #confluence
aExtent_outlet = [-76.0,-76.5, 39.5,40.0] #outlet
aExtent_dam = [-75.75,-76.15, 42.1,42.5] #dam  


for iMesh_type in range(1, 5):
    sMesh_type = aMesh_type[iMesh_type-1]
    if sMesh_type=='hexagon':
        sFilename_configuration_in = realpath( sPath +  '/example/susquehanna/pyflowline_susquehanna_hexagon.json' )
    else:
        if sMesh_type=='square':
            sFilename_configuration_in = realpath( sPath +  '/example/susquehanna/pyflowline_susquehanna_square.json' )
        else:
            if sMesh_type=='latlon':
                sFilename_configuration_in = realpath( sPath +  '/example/susquehanna/pyflowline_susquehanna_latlon.json' )
            else:
                sFilename_configuration_in = realpath( sPath +  '/example/susquehanna/pyflowline_susquehanna_mpas.json' )
   
   
        oPyflowline = pyflowline_read_model_configuration_file(sFilename_configuration_in, \
            iCase_index_in=iCase_index, dResolution_meter_in=dResolution_meter, sDate_in=sDate)
        
    if os.path.isfile(sFilename_configuration_in):
        pass
    else:
        print('This configuration does not exist: ', sFilename_configuration_in )
    
    if iMesh_type != 4:
        for iResolution in range(1, 4):    
            dResolution_meter = aResolution_meter[iResolution-1]

            oPyflowline = pyflowline_read_model_configuration_file(sFilename_configuration_in, \
            iCase_index_in=iCase_index, dResolution_meter_in=dResolution_meter, sDate_in=sDate)

            #oPyflowline.create_hpc_job(sSlurm_in =sSlurm )  
            print(iCase_index)            
            
            sFilename =  'filtered_flowline.png'
            #oPyflowline.plot(sFilename, sVariable_in = 'flowline_filter', aExtent_in =aExtent_full  )
            sFilename =  'conceptual_flowline_with_mesh.png'
            #if iMesh_type == 3:
            #oPyflowline.plot(sFilename,  iFlag_title=1 ,sVariable_in = 'overlap', aExtent_in =aExtent_full )  
                #pass
            #sFilename =  'meander.png'
            #oPyflowline.plot(sFilename, iFlag_title=0, sVariable_in = 'overlap', aExtent_in =aExtent_meander )       
            #sFilename =  'braided.png'
            #oPyflowline.plot(sFilename, iFlag_title=0, sVariable_in = 'overlap', aExtent_in =aExtent_braided )    
            #sFilename =  'confluence.png'
            #oPyflowline.plot(sFilename, iFlag_title=0, sVariable_in = 'overlap', aExtent_in =aExtent_confluence )    
            #sFilename =  'outlet.png'
            #oPyflowline.plot(sFilename, iFlag_title=0, sVariable_in = 'overlap', aExtent_in =aExtent_outlet )         
            sFilename =  'area_of_difference.png'
            #oPyflowline.plot( sFilename,sVariable_in = 'aof', aExtent_in =aExtent_full)
            if (iMesh_type==2 ) and (iResolution==1):
                sFilename_dem_flowline ='/qfs/people/liao313/data/hexwatershed/susquehanna/vector/swat/swat5k.shp'
                sFilename_in = 'compare.png'
                #oPyflowline.compare_with_raster_dem_method(sFilename_dem_flowline,sFilename_in,aExtent_in=aExtent_confluence )
                pass

            iCase_index= iCase_index+1
           
    else:
        oPyflowline = pyflowline_read_model_configuration_file(sFilename_configuration_in, \
            iCase_index_in=iCase_index, dResolution_meter_in=dResolution_meter, sDate_in=sDate)

        oPyflowline.create_hpc_job(sSlurm_in =sSlurm )   
        print(iCase_index)

        sFilename =  'filtered_flowline.png'
        #oPyflowline.plot(sFilename, sVariable_in = 'flowline_filter', aExtent_in =aExtent_full  )
        sFilename =  'conceptual_flowline_with_mesh.png'
        #oPyflowline.plot(sFilename, sVariable_in = 'overlap', aExtent_in =aExtent_full )  
        sFilename =  'meander.png'
        #oPyflowline.plot(sFilename, iFlag_title=0, sVariable_in = 'overlap', aExtent_in =aExtent_meander )       
        sFilename =  'braided.png'
        #oPyflowline.plot(sFilename, iFlag_title=0, sVariable_in = 'overlap', aExtent_in =aExtent_braided )    
        sFilename =  'confluence.png'
        #oPyflowline.plot(sFilename, iFlag_title=0, sVariable_in = 'overlap', aExtent_in =aExtent_confluence )    
        sFilename =  'outlet.png'
        #oPyflowline.plot(sFilename, iFlag_title=0, sVariable_in = 'overlap', aExtent_in =aExtent_outlet )      
        sFilename =  'area_of_difference.png'
        oPyflowline.plot( sFilename,sVariable_in = 'aof', aExtent_in =aExtent_full)

print('Finished')

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time Pyflowline simulation finished.')
