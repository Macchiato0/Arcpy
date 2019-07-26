cursor=arcpy.da.SearchCursor('Service Point selection',["OID@"])
null_address=[]
for row in cursor:
    where="SERVICEPOINTOBJECTID={}".format(row[0])
    cur=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["STREET"],where)
    st=[r[0] for r in cur]
    if len(st)<1: null_address.append(row[0])
