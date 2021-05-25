#create a rectangle latitude/longitude based mesh
#we will use some GIS way to define it
#longitude left and latitude bottom and nrow and ncolumn and resolution is used to define the rectangle
#because it is mesh, it represent the edge instead of center
#we will use gdal api for most operations
import os, sys
from osgeo import ogr, osr, gdal, gdalconst


from hexwatershed.auxiliary.gdal_function import obtain_raster_metadata
from hexwatershed.auxiliary.gdal_function import reproject_coordinates

os.environ['PROJ_LIB'] = '/qfs/people/liao313/.conda/envs/gdalenv/share/proj'

def create_lat_lon_mesh(dLongitude_left, dLatitude_bot, dResolution, ncolumn, nrow, sFilename_output):

   
    if os.path.exists(sFilename_output): 
        #delete it if it exists
        os.remove(sFilename_output)
    #pDriver = ogr.GetDriverByName('Esri Shapefile')
    pDriver = ogr.GetDriverByName('GeoJSON')
    #geojson
    pDataset = pDriver.CreateDataSource(sFilename_output)
    pSrs = osr.SpatialReference()  
    pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon

    pLayer = pDataset.CreateLayer('cell', pSrs, ogr.wkbPolygon)
    # Add one attribute
    pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn = pLayer.GetLayerDefn()
    pFeature = ogr.Feature(pLayerDefn)

    

    xleft = dLongitude_left
    xspacing= dResolution
    ybottom = dLatitude_bot
    yspacing = dResolution

    lID =0 
    #.........
    #(x2,y2)-----(x3,y3)
    #   |           |
    #(x1,y1)-----(x4,y4)
    #...............
    for column in range(0, ncolumn):
        for row in range(0, nrow):
            #define a polygon here
            x1 = xleft + (column * xspacing)
            y1 = ybottom + (row * yspacing)

            x2 = xleft + (column * xspacing)
            y2 = ybottom + ((row + 1) * yspacing)

            x3 = xleft + ((column + 1) * xspacing)
            y3 = ybottom + ((row + 1) * yspacing)

            x4 = xleft + ((column + 1) * xspacing)
            y4 = ybottom + (row * yspacing)
           

            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(x1, y1)
            ring.AddPoint(x2, y2)
            ring.AddPoint(x3, y3)
            ring.AddPoint(x4, y4)
            ring.AddPoint(x1, y1)
            pPolygon = ogr.Geometry(ogr.wkbPolygon)
            pPolygon.AddGeometry(ring)

            pFeature.SetGeometry(pPolygon)
            pFeature.SetField("id", lID)
            pLayer.CreateFeature(pFeature)

            lID = lID + 1


            pass
    pDataset = pLayer = pFeature  = None      



    return

if __name__ == '__main__':


    #dLongitude_left= -124 
    #dLatitude_bot=41
    dResolution=0.5
    #dLongitude_right = -110
    #dLatitude_top = 53
    

    #we can use the dem extent to setup 
    sFilename_geotiff = '/qfs/people/liao313/data/hexwatershed/columbia_river_basin/raster/dem/crbdem.tif'
    dPixelWidth, dOriginX, dOriginY, nrow, ncolumn, pSpatialRef, pProjection = obtain_raster_metadata(sFilename_geotiff)
    
    spatial_reference_source = pSpatialRef
    spatial_reference_target = osr.SpatialReference()  
    spatial_reference_target.ImportFromEPSG(4326)

    dY_bot = dOriginY - (nrow+1) * dPixelWidth
    dLongitude_left,  dLatitude_bot= reproject_coordinates(dOriginX, dY_bot,spatial_reference_source,spatial_reference_target)

    dX_right = dOriginX + (ncolumn +1) * dPixelWidth
    

    dLongitude_right, dLatitude_top= reproject_coordinates(dX_right, dOriginY,spatial_reference_source,spatial_reference_target)


    ncolumn= int( (dLongitude_right - dLongitude_left) / dResolution )
    nrow= int( (dLatitude_top - dLatitude_bot) / dResolution )

    sResolution = '0.5'
    sFilename_output = 'MOSART_'+ sResolution + '.json'
    sWorkspace_out = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin'

    sFilename_output = os.path.join(sWorkspace_out, sFilename_output)

    create_lat_lon_mesh(dLongitude_left, dLatitude_bot, dResolution, ncolumn, nrow, sFilename_output)
