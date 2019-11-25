#this script will calculate the distance between sp on CE ELlectric with sp on Outage_Map

#join severice point with service address table on objectid, join servie point with customer location on account number


acc_l,geo_l=[],[]
cursor1=arcpy.da.SearchCursor("CUSTOMER_LOCATION",["ACCOUNT","SHAPE@"])
for row in cursor1:
  acc_l.append(row[0])
  geo_l.append(row[1])

for i in range(len(acc_l)):
  acc=acc_l[i]
  geo=geo_l[i]
  where="ELECDIST.ServiceAddress.ACCOUNTNUMBER='{}'".format(acc)
  cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Service Point",["SHAPE@"])
  for p in cursor:
    meter=p[0].distanceTo(geo)
  print meter  
