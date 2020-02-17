cursor=arcpy.da.SearchCursor(r"Devices\Primary Devices\Isolator",["OID@"])

oid_isolator=[row[0] for row in cursor]

fields=["OID@","HIGHSIDETAP1","HIGHSIDETAP2","HIGHSIDETAP3","HIGHSIDETAP4","HIGHSIDETAP5","LOWSIDETAP1","LOWSIDETAP2","LOWSIDETAP3","LOWSIDETAP4","LOWSIDETAP5"]

iso_unit=[]
iso_oid=[]
for i in oid_isolator:
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.TRANSFORMERUNIT',fields,"TRANSFORMEROBJECTID={}".format(i))
    num=[row for row in cursor]
    for j in num:
        tap=j[1:]
        tap_2=[v for v in tap if v<2] 
        tap_16=[v for v in tap if v>16]
        tap_null=[v for v in tap if v is None]
        n=len(tap_2)+len(tap_16)+len(tap_null)
        if n> 0:
            iso_oid.append(i)
            iso_unit.append([i,j])
    
