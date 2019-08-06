'''
This script will merge multple polygons into one polygo
reduce the list of polygons to one polygon
lis = [ pg1 , pg2, pg3, pg4]
reduce(lambda a,b : a.union(b),lis)

union (other)
'''

import arcpy
from functools import reduce

#extract substation ID

cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist_GO\ELECDIST.Boundary_Substation_GO',["SUBSTATIONID"])

subid=[str(i[0]) for i in cursor]

#extract polygons belongs to every substations
#["SUBSTATION","HDQ","SHAPE@"]

for i in subid:
    where="SUBSTATIONID={}".format(i)
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist_GO\ELECDIST.Boundary_Feeder_GO',["SHAPE@"])
    plgongs=[i[0] for i in cursor]
    sub_poly=reduce(lambda a,b : a.union(b),plgongs)
'''    
cursor = arcpy.da.InsertCursor(r'E:\Data\yfan\sand_box.gdb\ELECDIST_Dissolve',["SHAPE@"]) 
cursor.insertRow([pg1])





#test sec_oh



cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\sand_box.gdb\ELECDIST_Dissolve',["*"])
for i in cursor:
    print i
'''
