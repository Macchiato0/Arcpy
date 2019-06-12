def move_sp_audit(sp1,sp2):
    try:
       cursor=arcpy.da.UpdateCursor(r"Customers & Transformers\Service Point",["SHAPE@XY"],where)
        coor=get_tlm_location(tlm_oid)
        print coor
        where="OBJECTID={}".format(oid)
        cursor=arcpy.da.UpdateCursor(r"Customers & Transformers\Service Point",["SHAPE@XY"],where)
        for row in cursor:
            row[0]=coor
            cursor.updateRow(row)
    except:
        pass
