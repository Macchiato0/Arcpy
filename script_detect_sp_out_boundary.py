#ctrl+c to stop calculation
import csv

file_name4='E:\\Data\\yfan\\PyModules\\sp_adrs_list.csv'
with open(file_name4, 'wb') as csvfile:
  filewriter = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
  header=["OID","FEEDERID","SHAPE","OID","STEET","CITY","WHQ"]
  filewriter.writerow(header)
  cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@","FeederID","SHAPE"])
  for i in cursor:
    oid=i[0]
    fid=i[1]
    shp=i[2]
    sp_id=i[0]
    where="SERVICEPOINTOBJECTID={}".format(oid)
    cur=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ServiceAddress',["STREET","CITY","WORKHEADQUARTERS"],where)
    for r in cur:
      st=r[0]
      ct=r[1]
      wq=r[2]
      filewriter.writerow([oid,fid,shp,sp_id,st,ct,wq]) 
      
     
    
    
# create a dictionary of work HQ polygon object and their id
cursor=arcpy.da.SearchCursor(r'E:\Apps\Application Launch\Electric\CVMWNT0146_GISLand.sde\GISLand.DBO.Land\GISLand.DBO.ElectricDistributionWHQ'
,["BOUNDARYNAMECD","SHAPE@"])
wkhd_plyg=dict ([(i[0],i[1]) for i in cursor])

file_name1='E:\\Data\\yfan\\PyModules\\sp_list.csv'
with open(file_name1, 'wb') as csvfile:
  filewriter = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
  header=["ServiceID","FEEDERID","SHAPE"]
  filewriter.writerow(header)
  cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@","FeederID","SHAPE"])
  for i in cursor:
    oid=i[0]
    fid=i[1]
    shp=i[2]
    filewriter.writerow([oid,fid,shp]) 
    cursor=arcpy.da.SearchCursor("SP",['SP.ServiceID', 'SP.FEEDERID', 'SP.SHAPE','SP_adrs.SERVICEPOINTOBJECTID', 'SP_adrs.STREET', 'SP_adrs.CITY', 'SP_adrs.WORKHEADQUARTERS'])
    
    
    
  
file_name2='E:\\Data\\yfan\\PyModules\\sp_address.csv'
with open(file_name2, 'wb') as csvfile:
  filewriter = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
  header=["SERVICEPOINTOBJECTID","STREET","CITY","WORKHEADQUARTERS"]
  filewriter.writerow(header)
  cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ServiceAddress',["SERVICEPOINTOBJECTID","STREET","CITY","WORKHEADQUARTERS"])
  for i in cursor:
    sp_oid=i[0]
    st=i[1]
    ct=i[2]
    wh=i[3]
    filewriter.writerow([sp_oid,st,ct,wh])       

file_name1='E:\\Data\\yfan\\PyModules\\sp_list.csv'
out_gdb = r'E:\Data\yfan\service_address_WHQ.gdb'

arcpy.TableToTable_conversion(file_name1, out_gdb, 'SP') 
arcpy.TableToTable_conversion(file_name2, out_gdb, 'SP_adrs') 
arcpy.AddJoin_management("SP", "ServiceID", "SP_adrs", "SERVICEPOINTOBJECTID","KEEP_ALL")

#above take 20 mins    
    
'''
file_name1='E:\\Data\\yfan\\PyModules\\sp_list.csv'
file_name2='E:\\Data\\yfan\\PyModules\\sp_address.csv'
data1 = csv.reader(open(file_name1),delimiter=',')
data2 = csv.reader(open(file_name2),delimiter=',')
file_name3='E:\\Data\\yfan\\PyModules\\sp_workHQ.csv'
arcpy.env.workspace= 'E:\\Data\\yfan\\PyModules'
arcpy.MakeTableView_management(in_table=file_name2, out_view='SP_adrs')
# Set the local parameters

inFeatures = r'E:\Data\yfan\service_address_WHQ.gdb\SP'
layerName = "SP_layer"
joinTable = "SP_adrs"
Field = "ServiceID"
field="SERVICEPOINTOBJECTID"
outFeature = "sp_hq"
'''

arcpy.env.workspace= r'E:\Data\yfan\service_address_WHQ.gdb'
arcpy.MakeTableView_management('SP',"SP")
arcpy.MakeTableView_management("SP_adrs","SP_adrs")
#arcpy.JoinField_management ("SP", "ServiceID", "SP_adrs", "SERVICEPOINTOBJECTID",["STREET","CITY","WORKHEADQUARTERS"])

#arcpy.MakeFeatureLayer_management ("SP",  layerName)
    
# Join the feature layer to a table
arcpy.AddJoin_management("SP", "ServiceID", "SP_adrs", "SERVICEPOINTOBJECTID","KEEP_ALL")
cursor=arcpy.da.SearchCursor("SP",["*"])
cursor.fields                         
#arcpy.CopyFeatures_management("SP", outFeature)
#arcpy.CopyRows_management("SP", "SP_HQ")

file_name3='E:\\Data\\yfan\\PyModules\\sp_HQ.csv'
with open(file_name3, 'wb') as csvfile:
  filewriter = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
  header=["FEEDERID","SHAPE","SERVICEPOINTOBJECTID","STREET","CITY","WORKHEADQUARTERS"]
  filewriter.writerow(header)
  cursor=arcpy.da.SearchCursor("SP",['SP.ServiceID', 'SP.FEEDERID', 'SP.SHAPE','SP_adrs.SERVICEPOINTOBJECTID', 'SP_adrs.STREET', 'SP_adrs.CITY', 'SP_adrs.WORKHEADQUARTERS'])
  for i in cursor:
    rows=list(i)
    filewriter.writerow(rows)          


point = arcpy.Point(25282, 43770)
ptGeometry = arcpy.PointGeometry(point)






