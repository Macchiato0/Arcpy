#ctrl+c to stop calculation
import csv
from functools import reduce
import json
# create a dictionary of work HQ polygon object and their id
cursor=arcpy.da.SearchCursor(r'E:\Apps\Application Launch\Electric\CVMWNT0146_GISLand.sde\GISLand.DBO.Land\GISLand.DBO.ElectricDistributionWHQ'
,["BOUNDARYNAMECD","SHAPE@"])
wkhd_plyg=dict ([(i[0],i[1]) for i in cursor])
wkhd_plyg
u_31=[]
for k in wkhd_plyg:
    b=wkhd_plyg[k].boundary () 
    a=b.buffer(500)
    u_31.append(a)
al_31=reduce(lambda a,b : a.union(b),u_31)
cursor = arcpy.da.InsertCursor(r'E:\Data\yfan\sand_box.gdb\wq',["SHAPE@"])
cursor.insertRow([al_31])

cursor = arcpy.da.SearchCursor(r'E:\Data\yfan\sand_box.gdb\wq',["SHAPE@"])
for i in cursor:
    ply=i[0]

#Set geoprocessing environments 
n=0
sp_oid_sp={}
cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@","SHAPE@XY"])
for row in cursor:
  sp_oid_sp[row[0]]=row[1]  
  n+=1
  if (n%19013==0):
    print n*100//1901285

oid_whq={}
cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ServiceAddress',["SERVICEPOINTOBJECTID","WORKHEADQUARTERS"])
for row in cursor:
  oid_whq[row[0]]=row[1]  
    
sp_oid['287145']
with open('E:\\Data\\yfan\\PyModules\\oid_whq.json', 'w') as fp:
  json.dump(oid_whq, fp)  

with open('E:\\Data\\yfan\\PyModules\\oid_whq.json') as fp:
  oid_whq = json.load(fp)   

with open('E:\\Data\\yfan\\PyModules\\sp_oid.json', 'w') as fp:
  json.dump(sp_oid_sp, fp)    
    
with open('E:\\Data\\yfan\\PyModules\\sp_oid.json') as f:
  sp_oid = json.load(f)
                
               
len(sp_oid_sp)    
sp_oid['1']
                               
                             
                          
n=0
sp_inbuffer=[]
for k in sp_oid:
  n+=1  
  pt=arcpy.Point(sp_oid[k][0],sp_oid[k][1])
  if ply.contains(pt):
    sp_inbuffer.append(k)  
  if (n%19013==0):
    print n*100//1901285




# open output file for writing
with open('E:\\Data\\yfan\\PyModules\\sp_in500.txt', 'w') as filehandle:
    json.dump(sp_inbuffer, filehandle) 
    
with open('E:\\Data\\yfan\\PyModules\\sp_in500.txt') as fp:
  p = json.load(fp)   


pt_buff=[]
pt_wr=[]
for i in p:
  pt_xy=sp_oid[str(i)]
  pt=arcpy.Point(pt_xy[0],pt_xy[1])
  try:     
    whq = oid_whq[str(i)]
    pg=wkhd_plyg[whq]
    m=pg.distanceTo(pt) 
    if m>0 and m<500:
      pt_buff.append(i)
    if m>500:
      pt_wr.append(i)  
  except:  
    pass  
        
#remove the erro caused by wrong whq        
with open('E:\\Data\\yfan\\PyModules\\feeder_hdq.json') as fp:
  feeder_hdq = json.load(fp)          

pt_buff_fid={}

for i in pt_buff:
  cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["FEEDERID"],"OBJECTID={}".format(i))
  for r in cursor:
    fid=r[0]
  pt_buff_fid[i]=fid  


pt_buff_2=[i for i in pt_buff]
for k in pt_buff_fid:
  try:
    whq1 = oid_whq[k]
    whq2=feeder_hdq[pt_buff_fid[k]]
    if whq1!=whq2:
      pt_buff_2.remove(k)
  except:
    pass

real_whd={}
for i in pt_buff_2:
  p=sp_oid[str(i)]    
  pt=arcpy.Point(p[0],p[1])
  for k in wkhd_plyg:
    if wkhd_plyg[k].contains(pt):
      real_whd[i]=k
    


with open('E:\\Data\\yfan\\PyModules\\sp_out_bound.csv', 'wb') as csvfile:
  filewriter = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
  header=["Service_oid","Feederid","Device","WHQ","Real_WHQ"]
  filewriter.writerow(header)
  for i in pt_buff_2:  
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["FEEDERID","DEVICELOCATION"],"OBJECTID={}".format(i))
    for r in cursor:
        dv=r[1]
        fid=r[0]
    try:    
      row=[i,fid,dv,oid_whq[str(i)],real_whd[i]]  
    except:
      row=[i,fid,dv,oid_whq[str(i)],'None']  
    filewriter.writerow(row)




'''    
cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@","FeederID","SHAPE@"])    
sp={}
for i in cursor:
  sp[i[0]]=[i[1],i[2]]
print len(sp)    

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

del sp
del sp_adrs

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
sp[1414737]

out_bound[0:1000]


for i in out_bound[0:1000]:
  w1='OBJECTID={}'.format(i)  
  cursor1=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["OID@","SHAPE@"],w1) 
  for row in cursor1:
    pt=row[1]
  w2="SERVICEPOINTOBJECTID={}".format(i)    
  cursor2=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ServiceAddress',["WORKHEADQUARTERS"],w2) 
  for row in cursor2:
    whq=row[0]
  meter=wkhd_plyg[whq].distanceTo(pt)
  print i,whq,meter
    





    
real_sp_wh={}
for i in out_bound:
  for k in wkhd_plyg:
    if wkhd_plyg[k].contains(sp[i][1]):
      real_sp_wh[i]=k
    

print real_sp_wh[1324595],real_sp_wh[1328838]

#sp without address
no_address=[]
for k in sp:
    if len(sp[k])<5:
      no_address.append(k)  
    
len(no_address)
print no_address[10000]    

no_address_sp={}
for i in no_address:
  for k in wkhd_plyg:
    if wkhd_plyg[k].contains(sp[i][1]):
      no_address_sp[i]=k
    
print len(no_address_sp),no_address[10000]

sp[1414737]
sp[14]

n=0
for i in sp:
    if sp[i][0] is None:
        n+=1

for k in real_sp_wh:
    sp[k].append(real_sp_wh[k])

print sp[1324595]

[u'032302', <PointGeometry object at 0x418c0050[0x418c0020]>, u'13280 ROUND LAKE RD', u'SUNFIELD', u'HML', u'LAN']

for k in no_address_sp:
    sp[k]=[sp[k][0],sp[k][1]]+['','','',no_address_sp[k]]

sp[1414737]

#arcpy geometry data removed
n=0
for k in sp:
  if len(sp[k])==5:
    a=sp[k][4]
    sp[k].append(a)

check the number    
n=0
for k in sp:
  if len(sp[k])!=6:
    print sp[14],k
    
check the none whq
no_hq=[]
for k in sp:
  if not sp[k][5]:
    no_hq.append(k)
print len(no_hq)    
no_hq[9]   
sp[4114657]

for i in no_hq:
  for k in wkhd_plyg:
    if wkhd_plyg[k].contains(sp[i][1]):
      a=k  
      sp[i][5]=a
        
#fix the sp[k] not in boundary
2221439,3167552
for k in wkhd_plyg:
    if wkhd_plyg[k].contains(sp[3167552][1]):
      a=k
sp[3167552]=[sp[3167552][0],sp[3167552][1]]+['','','',a]

sp[1]
[u'129802', <PointGeometry object at 0x26fa80b0[0x26fa8080]>, u'12594 SHIRE RD', u'WOLVERINE', u'BNC', u'BNC']
n=1
file_name3='E:\\Data\\yfan\\PyModules\\sp_HQ.csv'
with open(file_name3, 'wb') as csvfile:
  filewriter = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
  header=["row_id","feederid","address","city","WHQ","real_WHQ","service_oid"]
  filewriter.writerow(header)
  for k_row in sp:  
    row=[n]+[sp[k_row][0]]+sp[k_row][2:]+[k_row]
    filewriter.writerow(row)    
    n+=1    

for k in sp:
    a=[sp[k][0]]+sp[k][2:]
    
sp[1095743]
len(no_hq),len(no_address_sp),len(    
import csv    
import json
#creat json data
sp_dump={}
for k in sp:
    sp_dump[k]=[sp[k][0]]+sp[k][2:]
    
    
with open('E:\\Data\\yfan\\PyModules\\sp_hq.json', 'w') as fp:
  json.dump(sp_dump, fp)
  
with open('E:\\Data\\yfan\\PyModules\\sp_real_hq.json', 'w') as fp:
  json.dump(real_sp_wh, fp)

#open json data
with open('E:\\Data\\yfan\\PyModules\\sp_hq.json') as f:
  sp_hq = json.load(f)

with open('E:\\Data\\yfan\\PyModules\\sp_real_hq.json') as f:
  sp_real_hq = json.load(f)

empty_sp={}
n=0
for k in sp_hq:
    if len(sp_hq[k])<4:
        print sp_hq[k]
        n+=1
        
        

part_sp={}  
for k in sp_real_hq:
    insert_l=sp_hq[k][:3]+[sp_real_hq[k]]
    part_sp[k]=insert_l

#pop the k in part_up from sp_hq
#? pop print out the poped item
n=0
for k in part_sp:
    sp_hq.pop(k)
    n+=1

sp_hq.update(part_sp)

n=1
file_name3='E:\\Data\\yfan\\PyModules\\sp_HQ.csv'
with open(file_name3, 'wb') as csvfile:
  filewriter = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
  header=["row_id","feederid","address","city","WHQ","service_oid"]
  filewriter.writerow(header)
  for k_row in sp_hq:  
    if len(sp_hq[k_row])<4:
      row=[n]+['','','','']+[k_row]
    else:
      row=[n]+sp_hq[k_row]+[k_row]
    filewriter.writerow(row)    
    n+=1
    
    
    
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

