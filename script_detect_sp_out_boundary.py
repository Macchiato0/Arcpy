#ctrl+c to stop calculation
cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@","SHAPE@"])
for i in cursor:
  oid=i[0]
  pt=i[1]
  #select work_hQ from address table:r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ServiceAddress'
  where="SERVICEPOINTOBJECTID={}".format(oid)
  cur_adrs=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ServiceAddress',["STREET","CITY","WORKHEADQUARTERS"],where)
  for w in cur_adrs:
    #wh is work HQ,st is street, ct is city
    st,ct,wh=w[0],w[1],w[2]
    #print st,ct,wh
  #select polygon of workQH bondary
  where="WORKHEADQUARTERS={}".format(wh)
  cur_wkhq=arcpy.da.SearchCursor(,["SHAPE@"],where)
  for pg in cur_wkhq:
    if not pg
    
  
    
  
