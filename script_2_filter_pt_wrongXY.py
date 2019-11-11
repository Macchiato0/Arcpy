#DRG create 695785 location on gis, this script calculate the distance between GPS coordinate and map coordinates
#find the points with coordinates different with their input gps XY provided by field survey

import math

#data colection
where="LATITUDE is not null and LONGITUDE is not null"
cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@","SHAPE@","LATITUDE","LONGITUDE"],where)

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
                             
#pt1_coor[:100]
#pt2_coor[:100]
[i for i in pt2_coor if i is None]
#len(dist)
#dist[:100]
#dist_feet[:100]
#oid[:100]
#len(oid)

#364320 feet=1 decimal degree
#convert decimal degree to feet
dist_feet=[364320*i for i in dist]
oid=[i[0] for i in raw_list]
tu=lambda a,b : (a,b)                              
oid_dist_feet=map(tu, oid,dist_feet)
oid_lat_long=map(tu,oid_dist_feet,pt2_coor)
disp=lambda x : (x[0][0],x[0][1],x[1])
oid_dist_ll=map(disp,oid_lat_long)

#oid_lat_long[:10]
#oid_dist_ll[2]
#dist_over_723km[:100]
#[i[0] for i in dist_over_10000]

#dist over 250 feet
#filter the pt with questionable delta distance(delta distance=GPS_XY-MAP_XY)
dist_over_250= [i for i in oid_dist_feet if 500>i[1]>250]
len(dist_over_250)  5763                         
dist_over_500= [i for i in oid_dist_feet if 1000>i[1]>500]  
len(dist_over_500)   3268     
dist_over_1000= [i for i in oid_dist_feet if 2.4016e+6>i[1]>1000]  
len(dist_over_1000) 3384


dist_over_723km= [i for i in oid_dist_ll if i[1]>2.4016e+6]  
len(dist_over_723km)   56170                          
                             
for i in dist_over_723km[50000:]:
    print i[0],i[2][0],i[2][1]
    
    
                           
                             
                             
