DRG create 695785 location on gis
import math
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

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
raw_pt1_geom=[i[1] for i in raw_list]
pt1_coor=map(get_XY_degree,raw_pt1_geom)
yy=[[1,2,3],[2,3,4],[7,8,9],[1,3,5]]
[(i[0],i[1]) for i in yy]
pt2_coor=[(i[2],i[3]) for i in raw_list]
                             
dist=map(distance_degree,pt1_coor,pt2_coor)
                             

364320 feet a decimal degree
dist_feet=[364320*i for i in dist]
oid=[i[0] for i in raw_list]
tu=lambda a,b : (a,b)                              
oid_dist_feet=map(tu, oid,dist_feet)
oid_dist_feet[2]
                             
#dist over 250 feet
dist_over_250= [i for i in oid_dist_feet if i[1]>250]
len(dist_over_250)   40130                         
dist_over_500= [i for i in oid_dist_feet if i[1]>500]  
len(dist_over_500)   35858                             
dist_over_723km= [i for i in oid_dist_feet if i[1]>2.4016e+6]  
len(dist_over_723km)   30790                          
                             

                           
                             
                             
