def move_to_duplicate(sp1,sp2):
    try:
        where="OBJECTID={}".format(sp1)
        cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Service Point",["SHAPE@XY"],where)
        for row in cursor:
            coor=row[0]
        where="OBJECTID={}".format(sp2)
        cursor=arcpy.da.UpdateCursor(r"Customers & Transformers\Service Point",["SHAPE@XY"],where)
        for row in cursor:
            row[0]=coor
            cursor.updateRow(row)
    except:
        pass
