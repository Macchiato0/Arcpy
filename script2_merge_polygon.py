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

subid=list(set([str(i[0]) for i in cursor]))

#extract polygons belongs to every substations
#["SUBSTATION","HDQ","SHAPE@"]

fields=["SHAPE@","SUBSTATION","HDQ","SUBSTATIONID"]
dataset=r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist_GO\ELECDIST.Boundary_Feeder_GO'
fields_2=["SHAPE@","SUBSTATION_NAME","WORKHEADQUARTERS","SUBSTATIONID"]
for i in subid:
    where="SUBSTATIONID={}".format(i)
    cursor=arcpy.da.SearchCursor(dataset,fields,where)
    rows=[i for i in cursor]
    plgongs=[i[0] for i in rows]
    if len(plgongs)>0: 
        sub_poly=reduce(lambda a,b : a.union(b),plgongs)
        sub_name=rows[0][1]
        w_head=rows[0][2]
        sub_id=rows[0][3]        
        cursor = arcpy.da.InsertCursor(r'E:\Data\yfan\sand_box.gdb\Substation_Boundary',fields_2) 
        cursor.insertRow([sub_poly,sub_name,w_head,sub_id])
    #else:
        #print i
'''    
test the output
cursor = arcpy.da.InsertCursor(r'E:\Data\yfan\sand_box.gdb\ELECDIST_Dissolve',["SHAPE@"]) 
cursor.insertRow([pg1])


 r'E:\Data\yfan\sand_box.gdb\Substation_Boundary'


#test sec_oh



cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\sand_box.gdb\ELECDIST_Dissolve',["*"])
for i in cursor:
    print i
cursor=arcpy.da.SearchCursor('Substation Boundary',["*"])
for i in cursor:
    print i    
arcpy.DeleteRows_management('Substation Boundary')
'''
