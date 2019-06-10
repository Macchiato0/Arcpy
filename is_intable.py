#function to test if the address in address table and extract the matched SP OID
def is_intable(x): 
    cursor=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["SERVICEPOINTOBJECTID"],x)
    id=[row[0] for row in cursor]
    return id


