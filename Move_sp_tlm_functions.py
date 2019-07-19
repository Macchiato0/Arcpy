#move the select sp to the audit area

def get_tlm_location(tlm_oid):
    where="OBJECTID={}".format(tlm_oid)
    cursor=arcpy.da.UpdateCursor(r"Customers & Transformers\Secondary Transformers",["SHAPE@XY"],where)
    for row in cursor:
        result=row[0]
    return result

def move_sp_tlm(oid,tlm_oid):
    try:
        coor=get_tlm_location(tlm_oid)
        print coor
        where="OBJECTID={}".format(oid)
        cursor=arcpy.da.UpdateCursor(r"Customers & Transformers\Service Point",["SHAPE@XY"],where)
        for row in cursor:
            row[0]=coor
            cursor.updateRow(row)
    except:
        pass
        


 
    
    
