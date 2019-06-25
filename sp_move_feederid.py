# 1. select the sp 

# 2.select all the sp and move them about 10 meters away

# 3.select the sp with null feederid and cope them to excel

# 4.undo the selection

# test if all the transformers available
# a. create a list of distinct transformers in excel (sort-->advance-->unique)
# b.select them in the secondary transformer table |TEXT(value,"'0000000000'")
#                                                 |value&","&value

# create a list of devicelocation for removed sp


# 5.select the sp based on their devicelocation

import arcpy

select_oid = arcpy.da.SearchCursor(r"Customers & Transformers\Service Point", ["OID@","TLM"])

select_oid = arcpy.da.SearchCursor("Service Point selection", ["OID@","TLM"])

oid = [] #list of device location
num_tlm=[]#list of tlm, tlm should be in str because tlm may start at 0

# create a list of device location for every sp
for row1 in select_oid:
    x1 = row1[0]
    x2 = row1[1]
    oid.append(x1)
    num_tlm.append(x2)

# if true
print len(oid),len(num_tlm)

# create a list of tlm coordinate for every device location 

coor = [] #list of XY tuple

for tlm in num_tlm:
    sel = "TLM = " + "'%s'" % tlm
    select_tlm = arcpy.da.SearchCursor(r"Customers & Transformers\Secondary Transformers",["SHAPE@"], sel)
    for tlm_row in select_tlm: 
        coor.append(tlm_row [0])



# same?
print len(oid), len(num_tlm), len(coor) 

# if len(coor) is not consistant with len(dl_tlm) 
# find the missing tlm

tlm_set=set(num_tlm)
tlm_list=list(tlm_set)

t_p=","

for i in tlm_list:
    t_p="'"+str(i)+"'"+","+t_p

print t_p


# select the t_p from r"Customers & Transformers\Secondary Transformers"
# len(tlm_list)

cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Secondary Transformers",["TLM"])
tlm_s=[]
for i in cursor:
    tlm_s.append(i[0])
set(tlm_list)-set(tlm_s)

# if there are duplicate tlm

for i in tlm_s:
  if tlm_s.count(i)>1:
    print i

# set is substractable :set(a)-set(b)
# turn set to be list: list(set) 
# merge two list by + : l3=l1+l2

"""
old code
for sp in oid:
    try:
        x = "OBJECTID = {}".format(sp)
        ii = oid.index(sp) 
        cur = arcpy.da.UpdateCursor(r"Customers & Transformers\Service Point",["SHAPE@XY"],x) 
        for ro in cur:
            ro[0] = coor[ii]    
            cur.updateRow(ro)
    except:
        pass
""" 
#put oid and point of tlm in a dictionary
oid_sp_pt_tlm=dict(zip(oid,coor))

workspace = r'E:\Data\yfan\Connection to dgsep011.sde'

#function to move a sp based on oid to an pt object
def move_apPt(a,pt):
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    where="OBJECTID={}".format(a)
    cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        row[0]=pt
        cursor.updateRow(row)
    edit.stopOperation()
    
for sp in oid_sp_pt_tlm:
    pt=oid_sp_pt_tlm[sp]
    move_a2pt(sp,pt)
