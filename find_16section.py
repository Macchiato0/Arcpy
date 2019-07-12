#create lists for selected tlm points lables and geometry

cursor=arcpy.da.SearchCursor("Secondary Transformers selection",["OID@","SHAPE@"])

oid_tm,shp_tm,tlm_tm=[],[],[]

for row in cursor:
    oid_tm.append(row[0])
    shp_tm.append(row[1])


#find what section contains each point (transformer)

def find_16section(pt):
    cursor=arcpy.da.SearchCursor(r"CE Landbase\Sixteenth Section",["SIXTEENTHSECTIONNAME","SHAPE@"])
    for row in cursor:
        if row[1].contains(pt):
            return row[0]
    arcpy.ClearWorkspaceCache_management()
    arcpy.Delete_management("in_memory")

#find sections for every point in the point lists

newlist=map(lambda pt:find_section(pt),shp_tm)

#find all the tlm of a section

def find_removed(oid):
    position=oid_index(oid) 
    section=str(newlist[position])
    where="TLM LIKE '{}%'".format(section)
    cursor=arcpy.da.SearchCursor(r'Customers & Transformers\Secondary Transformers',["TLM","CONSTRUCTIONSTATUS","FEEDERID"],where)
    list_tlm=[row for row in cursor]
    return list_tlm
