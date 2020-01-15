def temp_move(a):#sp move
    workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    
    where="ServicePoint_DEVICELOCATION={}".format(a)
    cursor=arcpy.da.SearchCursor('sp032002',["SHAPE@"],where)
    for row in cursor:
        sp_geo=row[0]        
        
    where="DEVICELOCATION={}".format(a)
    cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        row[0]=sp_geo
        cursor.updateRow(row)
        
    edit.stopOperation()
    
    
cursor=arcpy.da.SearchCursor('sp032002',["ServicePoint_DEVICELOCATION"])
for i in cursor:
    temp_move(i[0])    

    
