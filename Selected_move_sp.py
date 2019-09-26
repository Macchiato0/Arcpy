def move_a2b(a,b):
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
    
  
cursor=arcpy.da.SearchCursor("Service Point selection",["OID@"])
a_oid=[i[0] for i in cursor]
cursor=arcpy.da.SearchCursor("Service Point selection 2",["OID@"])
b_oid=[i[0] for i in cursor]

a_idx=0
for i in a_oid:
  if a_idx<len(b_oid):
     move_a2b(i,b_oid[a_idx])
     a_idx+=1
