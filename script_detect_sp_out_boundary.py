#ctrl+c to stop calculation
import csv

file_name='E:\\Data\\yfan\\PyModules\\sp_not_in_wkhq.csv'

# create a dictionary of work HQ polygon object and their id
cursor=arcpy.da.SearchCursor(r'E:\Apps\Application Launch\Electric\CVMWNT0146_GISLand.sde\GISLand.DBO.Land\GISLand.DBO.ElectricDistributionWHQ'
,["BOUNDARYNAMECD","SHAPE@"])
wkhd_plyg=dict ([(i[0],i[1]) for i in cursor])

wrong_wh_sp=[]
with open(file_name, 'wb') as csvfile:
  filewriter = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
  cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@","SHAPE@","FeederID"])
  for i in cursor:
    oid=i[0]
    pt=i[1]
    fid=i[2]
    #select work_hQ from address table:r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ServiceAddress'
    where="SERVICEPOINTOBJECTID={}".format(oid)
    cur_adrs=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ServiceAddress',["STREET","CITY","WORKHEADQUARTERS"],where)
    for w in cur_adrs:
      #wh is work HQ,st is street, ct is city
      st,ct,wh=w[0],w[1],w[2]
      #filewriter.writerow([st,ct,wh])  
    #select polygon of workQH bondary
    if wh is None or not wkhd_plyg[wh].contains(pt) :
      for k_pg in wkhd_plyg:
        if wkhd_plyg[k_pg].contains(pt):
          row=[oid,fid,st,ct,wh,k_pg]
          wrong_wh_sp.append(oid,wh,k_pg)
      filewriter.writerow(row) 
    else:
      row=[oid,fid,st,ct,wh,wh]
      filewriter.writerow(row) 
    
  
  
      
    
   
  
  
