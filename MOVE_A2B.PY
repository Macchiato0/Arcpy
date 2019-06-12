#Function to move point A to point B, a an b are oid of points.
def MOVE_A2B(a,b):
    try:
        where="OBJECTID={}".format(b)
        cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Service Point",["SHAPE@XY"],where)
        for row in cursor:
            coor=row[0]
        where="OBJECTID={}".format(a)
        cursor=arcpy.da.UpdateCursor(r"Customers & Transformers\Service Point",["SHAPE@XY"],where)
        for row in cursor:
            row[0]=coor
            cursor.updateRow(row)
    except:
        pass
