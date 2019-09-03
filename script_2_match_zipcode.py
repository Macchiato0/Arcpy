
# py script to detect the sp with inconsistent zip+4 code in a zone
'''
script_2_check_null_address.py

cursor=arcpy.da.SearchCursor('Service Point selection',["OID@"])
null_address=[]
for row in cursor:
    where="SERVICEPOINTOBJECTID={}".format(row[0])
    cur=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["POSTALCODE"],where)
    st=[r[0] for r in cur]
    if len(st)<1: null_address.append(row[0])
    
'''
def find_zipcode(x):
    where='SERVICEPOINTOBJECTID={}'.format(x)
    cursor=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["POSTALCODE"],where)
    for row in cursor:
        postcode=row[0]
    return postcode

cursor=arcpy.da.SearchCursor('Service Point selection',["OID@","DEVICELOCATION"])
#only sp with DEVICELOCATION has address
list_sp=[row[0] for row in cursor if row[1] is not None]

'''
zip_list=[]
for i in list_sp:
    code0=find_zipcode(i) 
    zip_list.append(code0)
'''
zip_list=[find_zipcode(i) for i in list_sp]

#make a dictionary of oid-zipcode
sp_zipcode=dict(zip(list_sp, zip_list))

#groups_zipcode is the collection of zip code with valid 4 digit block code 
groups_zipcode=[sp_zipcode[k] for k in sp_zipcode if len(sp_zipcode[k])==10 and sp_zipcode[k][-4:]!=u'0000'] 

len(groups_zipcode)
#1260

len(set(groups_zipcode))
#248

#remove the zipcode+4 with 0000 as the block code
#0000 is the address not verified by usps service
#last 4 digit identifies a block, a segment of street, or a certain area for delivering purpose
import itertools

def get_pt(x): #x is oid of sp
    where='OBJECTID={}'.format(x)
    cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        p=row[0]
    return p
'''
def center(l): #l is a list of points. this function create the center of a list of points
    p=[i.firstPoint for i in l]
    x=[i.X for i in p]
    y=[i.Y for i in p]
    meanX=sum(x) / float(len(x))
    meanY=sum(y) / float(len(y))
    pt0=arcpy.Point(meanX,meanY) 
    center=arcpy.PointGeometry(pt0)
    return center



def rad(l): #l is a list of points, this function calculate the radius of a list of points
    a=center(l)
    for p1 in l:
        a.distanceTo(l
'''    
    
#far_pt is the dictionary of sp far away from its zip+4 zone
far_pt={}

#set of zip+4 code for a circuit
post_set=list(set(groups_zipcode))

for i in post_set:
    pts_oid=[k for k in sp_zipcode if sp_zipcode[k]==i]
    pts_shp=[get_pt(p) for p in pts_oid]
    d_pt_oid = dict(zip(pts_oid, pts_shp))                       
    pair_pt=list(itertools.combinations(pts_oid,2))
    for z in pair_pt:
        meters=d_pt_oid[z[0]].distanceTo(d_pt_oid[z[1]])
        if meters>= 1000:     #distance between 2 sp with same zip+4 is farer than 1000 meter               
            far_pt[z]=meters
                    
                           
l1=[k[0] for k in far_pt]
l2=[k[1] for k in far_pt]
l3=l1+l2
set(l3)

