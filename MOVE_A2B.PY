#Function to move point A to point B, a an b are oid of points.
def MOVE_A2B(a,b):
    workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    where="OBJECTID={}".format(b)
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        pt=row[0]
    where="OBJECTID={}".format(a)
    cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        row[0]=pt
        cursor.updateRow(row)
    edit.stopOperation()
    #edit.stopEditing(True)
    #?? really not sure why I cannot stop editing here, otherwise there will be a warning.
