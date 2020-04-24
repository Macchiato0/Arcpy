#move the disconnected service points to the correct tlm
'''
def move_sp(it):
    select_id='OBJECTID='+str(it)
    select_tlm = arcpy.da.SearchCursor(r"Customers & Transformers\Service Point", ["TLM"], select_id)
    for row in select_tlm:
        tlm=str(row[0])
    sel="TLM=" + "'"+tlm+"'"
    select_section=arcpy.da.SearchCursor(r"Customers & Transformers\Secondary Transformers",["SHAPE@"], sel)
    for i in select_section:
        location = i[0]
        pnt=location.centroid
        coordinate=pnt.X+10,pnt.Y+10
    update_pt = arcpy.da.UpdateCursor(r"Customers & Transformers\Service Point", ["SHAPE@"])
    for ro in update_pt:
        try:
            ro[0] = coordinate
            update_pt.updateRow(ro)
        except:
            pass
    return it


if __name__=="__main__":
   print 'this is old version. Move a point based on its TLM number'
'''
def move_sp(a):
    workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    
    where="OBJECTID={}".format(a)
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["TLM"],where)
    for row in cursor:
        tlm=str(row[0])
        
    where="TLM='{}'".format(tlm)
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.Transformer',["SHAPE@"],where)
    for row in cursor:
        pt=row[0]
        
    where="OBJECTID={}".format(a)
    cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        row[0]=pt
        cursor.updateRow(row)
        
    edit.stopOperation()

    
cursor=arcpy.da.SearchCursor("Service Point selection",["OID@"])
for i in cursor:
    move_sp(i[0])
        
