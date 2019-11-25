#this script will calculate the distance between sp on CE ELlectric with sp on Outage_Map

#join severice point with service address table on objectid, join servie point with customer location on account number (only keep matched)

acc_geo_0={}
cursor1=arcpy.da.SearchCursor('CUSTOMER_LOCATION',["ACCOUNT","SHAPE@"])
n=0
for row in cursor1:
  acc_geo_0[row[0]]=row[1]
  n=n+1
  if n%38000==0:
    print n
    
    
print len(acc_geo_0)    




acc_geo_2={}
cursor2=arcpy.da.SearchCursor(r"Customers & Transformers\Service Point",["ELECDIST.ServiceAddress.ACCOUNTNUMBER","SHAPE@"])
n=0
for row in cursor2:
  acc_geo_2[row[0]]=row[1]
  n=n+1
  if n%38000==0:
    print n

print len(acc_geo_2)     
  

acc_dist={}  
for k in acc_geo_0:
  try:
    dist=acc_geo_0[k].distanceTo(acc_geo_2[k])
    acc_dist[k]=dist
  except:
    pass
  
print len(acc_dist)   


