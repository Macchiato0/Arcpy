DRG create 695785 location on gis

cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Service Point",["OID@","SHAPE@","LATITUDE","LONGITUDE"]

raw_list=[i for i in cursor]

