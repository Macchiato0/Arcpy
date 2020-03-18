cursor=arcpy.da.SearchCursor(r'Customers & Transformers\Service Point',["OID@"],"FEEDERID in ('042002')")
oid=[i[0] for i in cursor]

def move_a2b(a,b):
    workspace = r'E:\Data\yfan\temp.sde'
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    where="OBJECTID={}".format(b)
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        pt=row[0]

    where="OBJECTID={}".format(a)
    cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\temp.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:

        row[0]=pt
        cursor.updateRow(row)  
    edit.stopOperation()


for i in oid:
    move_a2b(i,i)
