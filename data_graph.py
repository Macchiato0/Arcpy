DRG create 695785 location on gis
import math
cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Service Point",["OID@","SHAPE@","LATITUDE","LONGITUDE"]

raw_list=[i for i in cursor]

def get_XY_degree(pt):
    lat=pt.projectAs(arcpy.SpatialReference(4269)).firstPoint.Y
    lon=pt.projectAs(arcpy.SpatialReference(4269)).firstPoint.X
    coor=(lat,lon)
    return coor
                             
(raw_list[0] [2],raw_list[0] [3])
get_XY_degree(raw_list[0] [1])
                             
def distance_degree(pt1,pt2):
    result=math.sqrt((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)
    return result
                             
#create 2 list for pt1,pt2

                           
                             
                             
