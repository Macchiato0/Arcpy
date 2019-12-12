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
  
print acc_dist[u'7001391527']
print len(x)

x = [acc_dist[key] for key in acc_dist]
import numpy
arr = numpy.array(x)
counts, bins = numpy.histogram(x)
plt.hist(bins[:-1], bins, weights=counts)
(array([  3.84359000e+05,   3.00000000e+00,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
         0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
         1.00000000e+00]), array([  7.73989990e-07,   1.47390595e+04,   2.94781191e+04,
         4.42171786e+04,   5.89562381e+04,   7.36952977e+04,
         8.84343572e+04,   1.03173417e+05,   1.17912476e+05,
         1.32651536e+05,   1.47390595e+05]), <a list of 10 Patch objects>)

#pick out the outliars

y=[i for i in x if i>99]
num_bins=20
n, bins, patches = plt.hist(y, num_bins, facecolor='blue', alpha=0.5)
plt.show()


import json
with open(r'E:\Data\yfan\PyModules\acc_dist1125.json', 'w') as fp:
    json.dump(acc_dist, fp)
    

#open python idle
import json
with open(r'E:\Data\yfan\PyModules\acc_dist1125.json', 'r') as fp:
    acc_dist=json.loads(fp.read())
    
len(acc_dist)

#import matplotlib.pyplot as plt

x = [[key,acc_dist[key]] for key in acc_dist]

l_1000_2000=[]

for i in x:
  dist=i[1]
  if dist<2000 and dist>1000:
    l_1000_2000.append(i)

l_1_2=[]    
for i in l_1000_2000:
  acct=i[0]
  where='ELECDIST.ServiceAddress.ACCOUNTNUMBER={}'.format(acct)
  try:
    cursor=arcpy.da.SearchCursor(r'Customers & Transformers\Service Point',["ELECDIST.ServicePoint.OBJECTID"],where)    
    for row in cursor:
      sp_id=row[0]
      r=sp_id+i
    l_1_2.append(r)
  except:
    pass


plt.hist(x, bins = 100)


