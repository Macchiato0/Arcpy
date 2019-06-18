#make a list of last point for lines
#service points
cursor=arcpy.da.SearchCursor("Service Point selection",["OID@","SHAPE@","TLM"])
pt_list=[]
oid_list=[]
TLM_list=[]
for row in cursor:
    pt_list.append(row[1])
    oid_list.append(row[0])
    TLM_list.append(row[2])
    
#make a list of first point for lines
#transformers

