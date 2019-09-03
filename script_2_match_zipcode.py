# py script to detect the sp with inconsistent zip+4 code in a zone
def find_zipcode(x):
    where='serviceobjectid={}'.format(x)
    cursor=arcpy.da.Search("address",["zip"],where)
    for row in cursor:
        postcode=row[0]
    return postcode

list_sp=[list of objectid of a circuit]

zip_list=[find_zipcode(i) for i in list]

sp_zipcode=zip(list_sp, zip_list)

groups_zipcode=[i for i in list(set(zip_list)) if i[-4] not '0000']

#remove the zipcode+4 with 0000 as the block code
#0000 is the address not verified by usps service
#last 4 digit identifies a block, a segment of street, or a certain area for delivering purpose
import itertools

def get_pt(x): #x is oid of sp
    where='Objectid={}'.format(x)
    cursor=arcpy.da.Search('sp',["SHAPE@"],where]
    for row in cursor:
        p=row[0]
    return p


incosistant_pt={}
for i in groups_zipcode:
    pts_oid=[j[0] for j in list_sp if j[1]==i]
    pts_shp=[get_pt(p) for p in pts_oid]
    d_pt_oid = dict(zip(pts_oid, pts_shp))                       
    pair_pt=list(itertools.combinations(pts_oid,2))                       
    for z in pair_pt:
        m=d_pt_oid(z[0]).distanceTo(d_pt_oid(z[1]))
        if m>= 1000:     #distance between 2 sp with same zip+4 is farer than 1000 meter               
            incosistant_pt(z)=m
                           
                           

