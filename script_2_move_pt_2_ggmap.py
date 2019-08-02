def get_XY_meter(pt):
    lat=pt.projectAs(arcpy.SpatialReference(102123)).firstPoint.Y
    lon=pt.projectAs(arcpy.SpatialReference(102123)).firstPoint.X
    coor=(lon,lat)
    return coor    

def move_oid(oid):
    workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    cursor=arcpy.da.SearchCursor('T7_31_2019_coordinates Events',["X","Y"],'Name={}'.format(oid))
    for row in cursor:
        pt=arcpy.Point(row[0],row[1]) 
    where="OBJECTID={}".format(oid)
    cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        row[0]=pt
        cursor.updateRow(row)
    edit.stopOperation()  



cursor=arcpy.da.SearchCursor("Service Point selection",["OID@"])

oid_list=[int(i[0]) for i in cursor]


for i in oid_list:
    move_oid(i)
