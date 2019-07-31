cursor=arcpy.da.SearchCursor('Service Point selection',["OID@"])
null_address=[]
for row in cursor:
    where="SERVICEPOINTOBJECTID={}".format(row[0])
    cur=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["STREET"],where)
    st=[r[0] for r in cur]
    if len(st)<1: null_address.append(row[0])
'''
print the address of sp
'''
cursor=arcpy.da.SearchCursor("Service Point selection",["OID@"])
oid_list=[]
for row in cursor:
    oid_list.append(int(row[0]))
    
    
for i in oid_list:
    where="SERVICEPOINTOBJECTID={}".format(i)
    cursor=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["SERVICEPOINTOBJECTID","STREET", "CITY", "POSTALCODE"], where)
    for row in cursor:
        print str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])[0:5]
