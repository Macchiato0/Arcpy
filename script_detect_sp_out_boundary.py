#ctrl+c to stop calculation
import csv

# create a dictionary of work HQ polygon object and their id
cursor=arcpy.da.SearchCursor(r'E:\Apps\Application Launch\Electric\CVMWNT0146_GISLand.sde\GISLand.DBO.Land\GISLand.DBO.ElectricDistributionWHQ'
,["BOUNDARYNAMECD","SHAPE@"])
wkhd_plyg=dict ([(i[0],i[1]) for i in cursor])
wkhd_plyg
    
cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@","FeederID","SHAPE@"])    
sp={}
for i in cursor:
  sp[i[0]]=[i[1],i[2]]
    
cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ServiceAddress',["SERVICEPOINTOBJECTID","STREET","CITY","WORKHEADQUARTERS"],"SERVICEPOINTOBJECTID is not null")    
sp_adrs={}
for r in cursor:
  sp_adrs[r[0]]=[r[1],r[2],r[3]]
  
  
 
print len(sp),len(sp_adrs)

for k in sp:
  try:  
    for v in sp_adrs[k]:
      sp[k].append(v)
  except:
    pass
  
del sp_adrs     
print len(sp)     



print sp[1],sp[20],sp[202][1]




out_bound=[]
for k in sp:
  try:
    whq=sp[k][4]
    if not wkhd_plyg[whq].contains(sp[k][1]):
      out_bound.append(k)
  except:
    pass
      
print len(out_bound)   
out_bound[10000]

real_sp_wh={}
for i in out_bound:
  for k in wkhd_plyg:
    if wkhd_plyg[k].contains(sp[i][1]):
      real_sp_wh[i]=k
    

print real_sp_wh[1324595]


for k in sp:
  sp[k].remove(sp[k][1])
   
    
    
import json

with open('E:\\Data\\yfan\\PyModules\\sp_hq.json', 'w') as fp:
  json.dump(sp, fp)
  
with open('E:\\Data\\yfan\\PyModules\\sp_real_hq.json', 'w') as fp:
  json.dump(real_sp_wh, fp)
  
with open('E:\\Data\\yfan\\PyModules\\sp_hq.json') as f:
  data = json.load(f)

data[10]
  

'''    
file_name1='E:\\Data\\yfan\\PyModules\\sp_list.csv'
out_gdb = r'E:\Data\yfan\service_address_WHQ.gdb'
arcpy.TableToTable_conversion(file_name1, out_gdb, 'SP') 
arcpy.TableToTable_conversion(file_name2, out_gdb, 'SP_adrs') 
'''
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
  header=[]
  filewriter.writerow(header)
  cursor=arcpy.da.SearchCursor("SP",[])
  for i in cursor:
    rows=list(i)
    filewriter.writerow(rows)          


point = arcpy.Point(25282, 43770)
ptGeometry = arcpy.PointGeometry(point)




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

