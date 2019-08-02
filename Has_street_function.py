#function to test if the address in address table and extract the matched SP OID
def is_intable(x): 
    where="SERVICEPOINTOBJECTID={}".format(x)
    cursor=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["STREET"],where)
    id=[row[0] for row in cursor]
    if len(id)>0:
       return 1
    else:
        return 0
        
        
cursor=arcpy.da.SearchCursor("Service Point selection",["OID@"])

oid=[i[0] for i in cursor]
oid_no_street=[]
for i in oid:
    if is_intable(i)==0:
        oid_no_street.append(i)
