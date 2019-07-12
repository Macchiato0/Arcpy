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


#find sections for every point in the point lists

for i in range(len(shp_tm)):
    sec=find_16section(shp_tm[i])
    tlm_tm.append(sec)
