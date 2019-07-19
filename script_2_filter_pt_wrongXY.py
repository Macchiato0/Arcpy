#DRG create 695785 location on gis, this script calculate the distance between GPS coordinate and map coordinates
#find the points with coordinates different with their input gps XY provided by field survey

import math

#data colection
cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Service Point",["OID@","SHAPE@","LATITUDE","LONGITUDE"]

raw_list=[i for i in cursor]

#get XY of pt (geometry) in degree on map                             
def get_XY_degree(pt):
    lat=pt.projectAs(arcpy.SpatialReference(4269)).firstPoint.Y
    lon=pt.projectAs(arcpy.SpatialReference(4269)).firstPoint.X
    coor=(lat,lon)
    return coor
#try get_XY                             
(raw_list[0] [2],raw_list[0] [3])
get_XY_degree(raw_list[0] [1])

#function to calculate distance between GPS and map coordinates
def distance_degree(pt1,pt2):
    result=math.sqrt((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)
    return result
                             
#create 2 list for pt1,pt2 (pt1:gps coordinates, pt2:map coordinates)
raw_pt1_geom=[i[1] for i in raw_list]
pt1_coor=map(get_XY_degree,raw_pt1_geom)
yy=[[1,2,3],[2,3,4],[7,8,9],[1,3,5]]
[(i[0],i[1]) for i in yy]
pt2_coor=[(i[2],i[3]) for i in raw_list]
                             
dist=map(distance_degree,pt1_coor,pt2_coor)
                             

#364320 feet=1 decimal degree
#convert decimal degree to feet
dist_feet=[364320*i for i in dist]
oid=[i[0] for i in raw_list]
tu=lambda a,b : (a,b)                              
oid_dist_feet=map(tu, oid,dist_feet)
oid_dist_feet[2]
                             
#dist over 250 feet
#filter the pt with questionable delta distance(delta distance=GPS_XY-MAP_XY)
dist_over_250= [i for i in oid_dist_feet if i[1]>250]
len(dist_over_250)   40130                         
dist_over_500= [i for i in oid_dist_feet if i[1]>500]  
len(dist_over_500)   35858                             
dist_over_723km= [i for i in oid_dist_feet if i[1]>2.4016e+6]  
len(dist_over_723km)   30790                          
                             

                           
                             
                             
