#move the select sp to the audit area
x,y=483320.823,432750.750 
def move_sp_audit(oid):
    where="OBJECTID={}".format(oid)
    cursor=arcpy.da.UpdateCursor(r"Customers & Transformers\Service Point",["SHAPE@XY"],where)
    for row in cursor:
        row[0]=func(tlm)
        cursor.updateRow(row)
    
    
