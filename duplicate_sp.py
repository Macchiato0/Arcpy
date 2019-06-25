cursor=arcpy.da.SearchCursor('Service Point selection',["OID@","TLM","DEVICELOCATION","SHAPE@","FEEDERID"])

#make a dictionary of tlm:[(device location,point,oid),(device loaction, point,oid)]
#

rows=[i for i in cursor]

#tlm as keys of a dictionary
tlm_list={str(i[1]) for i in rows}

"""
test the duplicate device location
dev_l=[i[2] for i in rows]

make sure they are all duplicate
dup_sp=[i for i in set(dev_l) if dev_l.count(i)==2]

make a dictionary of dup_sp:[(oid, pt,feed),(oid,pt,feed)]

dev_pt= {x: [(i[0],i[3],str(i[4])) for i in rows if i[2]==x] for x in dup_sp} 

test the distance between two dup sp

del_sp=[k for k in dup_sp if dev_pt[k][0][1].distanceTo(dev_pt[k][1][1])<20]

print del_sp
p=''
for i in del_sp:
    p=p+str(i)[:-2]+','
p
del_list=[]
for i in del_sp:
    id_l=[j[0] for j in dev_pt[i]]
    feed_l=[j[2] for j in dev_pt[i]]
    pt_l=[j[1] for j in dev_pt[i]]
    cursor0=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["STREET"],"SERVICEPOINTOBJECTID={}".format(id_l[0]))
    cursor1=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["STREET"],"SERVICEPOINTOBJECTID={}".format(id_l[1]))
    stree_num=[len([r for r in cursor0]),len([r for r in cursor1])] # search if sp has street address
    min_stree=min(stree_num)
    if min_stree>0: # both have address
        n=stree_num.index(min_stree)
        del_list.append((i,id_l[n],feed_l[n],pt_l[n]))
    elif min_stree==0 and max(stree_num)>0: # one sp has no address 
        n=stree_num.index(min_stree)
        del_list.append((i,id_l[n],feed_l[n],pt_l[n]))
    else: #no sp has address
        del_list.append((i,id_l[1],feed_l[1],pt_l[1]))

sp_line=[]
for i in (i for i in del_list):
    fd=i[2]
    cursor=arcpy.da.SearchCursor(r'Customers & Transformers\Secondary Overhead Conductor',["SHAPE@","OID@"],"FEEDERID='{}'".format(fd))
    for l in cursor:
        if i[3].distanceTo(l[0])==0:
            sp_line.append((i[1],l[1]))
            continue
        else:
            continue
 

sp_line_un=[]
for i in (i for i in del_list):
    fd=i[2]
    cursor=arcpy.da.SearchCursor(r'Customers & Transformers\Secondary Underground Conductor',["SHAPE@","OID@"],"FEEDERID='{}'".format(fd))
    for l in cursor:
        if i[3].distanceTo(l[0])==0:
            sp_line_un.append((i[1],l[1]))
            continue
        else:
            continue

"""
#create a dictionary tlm:[(oid,dl,pointgeom),(oid,dl,pointgeom)]
dict_pt = {x: [(i[0],i[2],i[3],str(i[4])) for i in rows if str(i[1])==x] for x in tlm_list}

"""
'0757212102': [(2461123, 6001688895.0, <PointGeometry object at 0x8bc0ac90L[0x8bc0ac60L]>), (2036003, 6001688895.0, <PointGeometry object at 0x8bd6cc10L[0x8bd6cbe0L]>)], 
"""

#find the tlm with duplicate device location i.e. one tlm with two same sp
key_list=[key for key in dict_pt if len(set([i[1] for i in dict_pt[key]]))==1 and len(dict_pt[key])==2]

#find if the 2 sp are geographically on a same tlm (assume distance between the 2 sp less than 10 m are on one tlm)
del_tlm=[i for i in key_list if dict_pt[i][0][2].distanceTo(dict_pt[i][1][2])<150]


#select the sp based on del_tlm and delete the sp without address or created earlist

del_list=[]
for i in del_tlm:
    id_l=[j[0] for j in dict_pt[i]]
    feed_l=[j[3] for j in dict_pt[i]]
    pt_l=[j[2] for j in dict_pt[i]]
    cursor0=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["STREET"],"SERVICEPOINTOBJECTID={}".format(id_l[0]))
    cursor1=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["STREET"],"SERVICEPOINTOBJECTID={}".format(id_l[1]))
    stree_num=[len([r for r in cursor0]),len([r for r in cursor1])] # search if sp has street address
    min_stree=min(stree_num)
    if min_stree>0: # both have address
        n=stree_num.index(min_stree)
        del_list.append((i,id_l[n],feed_l[n],pt_l[n]))
    elif min_stree==0 and max(stree_num)>0: # one sp has no address 
        n=stree_num.index(min_stree)
        del_list.append((i,id_l[n],feed_l[n],pt_l[n]))
    else: #no sp has address
        del_list.append((i,id_l[1],feed_l[1],pt_l[1]))



"""

"""
r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.SecOHElectricLineSegment'
workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
sp_line=[]
for i in (i for i in del_list):
    fd=i[2]
    cursor=arcpy.da.SearchCursor(r'Customers & Transformers\Secondary Overhead Conductor',["SHAPE@","OID@"],"FEEDERID='{}'".format(fd))
    for l in cursor:
        if i[3].distanceTo(l[0])==0:
            sp_line.append((i[1],l[1]))
            continue
        else:
            continue
 

sp_line_un=[]
for i in (i for i in del_list):
    fd=i[2]
    cursor=arcpy.da.SearchCursor(r'Customers & Transformers\Secondary Underground Conductor',["SHAPE@","OID@"],"FEEDERID='{}'".format(fd))
    for l in cursor:
        if i[3].distanceTo(l[0])==0:
            sp_line_un.append((i[1],l[1]))
            continue
        else:
            continue



"""
for i in delDataList:
 	#create update cursor
 	cursor = arcpy.da.UpdateCursor(i,"*","CONSTRUCTIONSTATUS=55") 
 	for row in cursor:
 	cursor.deleteRow() 
 	#delete cursor when finished
 	del cursor
"""

cursor=arcpy.da.SearchCursor('Service Point selection',["OID@","TLM","DEVICELOCATION","SHAPE@","FEEDERID","DATECREATED"])

rows=[i for i in cursor]
device=[i[2] for i in rows]

device_2=list(set([i for i in set(device) if device.count(i)>1]))

#test the sp with more than 2 repeated device location
for i in device_2:
    l_sp=[j for j in rows if j[2]==i]
    pts=[p[3] for p in l_sp]
    if len(pts)>2:
        print i




"""
test1 
    DATEMODIFIED not null

        delete: DATEMODIFIED ealier

    DATEMODIFIED null

        delete: DATECREATED earlier
test2
    if address null
    add address

find OH lines:
find UN lines

cursor=arcpy.da.SearchCursor('Service Point selection',["OID@","DATEMODIFIED","DEVICELOCATION","SHAPE@","FEEDERID","DATECREATED"])
rows=[i for i in cursor]
dev_l=[i[2] for i in rows]    

make a dict device location:(oid,DATEMODIFIED,DATECREATED,pt),(oid,DATEMODIFIED,DATECREATED,pt)

dev_dat={x:[i for i in rows if i[2]==x] for x in set(dev_l)}

find the sp of duplicate service point with DATEMODIFIED ealier,create a dictionary device location:oid removable

dev_del={}

for k,v in dev_dat.iteritems():
    y_m_d=[i[1] for i in v]
    y_m_d_t=[i[5] for i in v]
    oid_l=[i[0] for i in v] 
    if None not in y_m_d and y_m_d[0]!=y_m_d[1]:
        n=y_m_d.index(min(y_m_d))
        keep=y_m_d.index(max(y_m_d))
        dev_del[k]=(v[n],v[keep])
    elif y_m_d[0]==y_m_d[1]:
        n=oid_l.index(min(oid_l))
        keep=oid_l.index(max(oid_l))
        dev_del[k]=(v[n],v[keep])
    elif y_m_d_t[0]!=y_m_d_t[1]:
        n=y_m_d_t.index(min(y_m_d_t))
        keep=y_m_d_t.index(max(y_m_d_t))
        dev_del[k]=(v[n],v[keep])
    else:
        n=oid_l.index(min(oid_l))
        keep=oid_l.index(max(oid_l))
        dev_del[k]=(v[n],v[keep])


[dev_del[k][0][0] for k in dev_del]

check if the sp in dev_del has address and the left sp has no address, and swop the address to the kept sp

workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()
for k,v in dev_del.iteritems():
    id_l=[i[0] for i in v]
    cursor0=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["STREET"],"SERVICEPOINTOBJECTID={}".format(id_l[0]))
    street0=[r for r in cursor0]
    cursor6=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["STREET"],"SERVICEPOINTOBJECTID={}".format(id_l[1]))
    street6=[r for r in cursor6] # search if sp has street address for 0 and 1
    if len(street6)==0 and len(street0)>0: 
        cursor_0=arcpy.da.UpdateCursor("ELECDIST.ServiceAddress",["SERVICEPOINTOBJECTID"],"SERVICEPOINTOBJECTID={}".format(id_l[0]))
        for row in cursor_0:
            row[0]=id_l[1]
            cursor_0.updateRow(row) 
    else:
        pass
edit.stopOperation()
        

check if the 
for k,v in dev_del.iteritems():
    id_l=[i[0] for i in v]
    cursor0=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["STREET"],"SERVICEPOINTOBJECTID={}".format(id_l[0]))
    street0=[r for r in cursor0]
    cursor6=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["STREET"],"SERVICEPOINTOBJECTID={}".format(id_l[1]))
    street6=[r for r in cursor6] # search if sp has street address for 0 and 1
    if len(street6)==0 and len(street0)>0: 
        print id_l[0] 
    else:
        None

del_pt=[dev_del[k][0][0] for k in dev_del]
cursor=arcpy.da.SearchCursor('Service Point selection',["OID@","SHAPE@","FEEDERID"])
del_pt_r=[i for i in cursor]
 
sp_line=[]
for i in del_pt_r:
    fd=str(i[2])
    poit=i[1]
    sp_oid=i[0]
    cursor=arcpy.da.SearchCursor(r'Customers & Transformers\Secondary Overhead Conductor',["SHAPE@","OID@"],"FEEDERID='{}'".format(fd))
    for l in cursor:
        if poit.distanceTo(l[0])==0:
            sp_line.append((sp_oid,l[1]))
        else:
            pass
 
s_v=[i[0] for i in sp_line]

del_pt_r_un=[i for i in del_pt_r if i[0] not in s_v]
del_pt_r_un=[i for i in cursor]

sp_line_un=[]
for i in del_pt_r_un:
    fd=str(i[2])
    poit=i[1]
    sp_oid=i[0]
    cursor=arcpy.da.SearchCursor(r'Customers & Transformers\Secondary Underground Conductor',["SHAPE@","OID@"],"FEEDERID='{}'".format(fd))
    for l in cursor:
        if poit.distanceTo(l[0])==0:
            sp_line_un.append((sp_oid,l[1]))
        else:
            pass

done_=list(set([i[0] for i in sp_line])| set([i[0] for i in sp_line_un]))
[i for i in del_pt if i not in done_]
