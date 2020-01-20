def tlm_move(a):
    workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    
    where="TLM='{}'".format(a)
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\sand_box.gdb\tlm091602',["SHAPE@"],where)
    for row in cursor:
        tlm_geo=row[0]        
        
    where="TLM='{}'".format(a)
    cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.Transformer',["SHAPE@"],where)
    for row in cursor:
        row[0]=tlm_geo
        cursor.updateRow(row)
        
    edit.stopOperation()


cursor=arcpy.da.SearchCursor('tlm091602',["TLM"])
for i in cursor:
    tlm_move(i[0])    
