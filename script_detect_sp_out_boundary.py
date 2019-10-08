#ctrl+c to stop calculation
import csv


# create a dictionary of work HQ polygon object and their id
cursor=arcpy.da.SearchCursor(r'E:\Apps\Application Launch\Electric\CVMWNT0146_GISLand.sde\GISLand.DBO.Land\GISLand.DBO.ElectricDistributionWHQ'
,["BOUNDARYNAMECD","SHAPE@"])
wkhd_plyg=dict ([(i[0],i[1]) for i in cursor])

file_name1='E:\\Data\\yfan\\PyModules\\sp_list.csv'
with open(file_name1, 'wb') as csvfile:
  filewriter = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
  header=["OBJECTID","FEEDERID","SHAPE"]
  filewriter.writerow(header)
  cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@","FeederID","SHAPE"])
  for i in cursor:
    oid=i[0]
    fid=i[1]
    shp=i[2]
    filewriter.writerow([oid,fid,shp]) 
    
  
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

    
    
    
'''
file_name1='E:\\Data\\yfan\\PyModules\\sp_list.csv'
file_name2='E:\\Data\\yfan\\PyModules\\sp_address.csv'

data1 = csv.reader(open(file_name1),delimiter=',')
data2 = csv.reader(open(file_name2),delimiter=',')
file_name3='E:\\Data\\yfan\\PyModules\\sp_workHQ.csv'
'''





arcpy.env.workspace= 'E:\\Data\\yfan\\PyModules'
arcpy.MakeTableView_management(in_table=file_name1, out_view='SP')
arcpy.MakeTableView_management(in_table=file_name2, out_view='SP_adrs')

# Set the local parameters

inFeatures = "SP"
inField = "OBJECTID"
joinTable = "SP_adrs"
joinField = "SERVICEPOINTOBJECTID"

arcpy.JoinField_management (inFeatures, inField, joinTable, joinField)

point = arcpy.Point(25282, 43770)
ptGeometry = arcpy.PointGeometry(point)






