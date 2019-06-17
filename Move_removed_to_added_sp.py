# 1. make sure the removed sp are not connected to the network


#set a list of object id of remove sp
#set a list of point geometry of remove sp


remove_obj=[]
remove_pt=[]

cursor = arcpy.da.SearchCursor("Service Point selection",["SHAPE@","OID@"])

for i in cursor:
    remove_pt.append(i[0])
    remove_obj.append(i[1])

print len(remove_pt)==len(remove_obj)
print len(remove_pt), len(remove_obj)



#set a list of object id of added sp
#set a list of point geometry of added sp

added_obj=[]
added_pt=[]

cursor = arcpy.da.SearchCursor('Service Point selection2',["SHAPE@","OID@"])

for i in cursor:
    added_pt.append(i[0])
    added_obj.append(i[1])

print len(added_pt), len(added_obj)
print len(added_pt)==len(added_obj)

#calculate the distance between removed and added 
#if minimum distance less than 10, the remove and added should be the couple

match_added_pt=[]
match_added_obj=[]
for i in remove_pt:
    meters=[]
    for j in added_pt:
        dist=i.distanceTo(j)
        meters.append(dist)
    added_i=meters.index(min(meters))
    if min(meters)<10:   
        match_pt=added_pt[added_i]
        match_id=added_obj[added_i]
        match_added_pt.append(match_pt)
        match_added_obj.append(match_id) 
    else:
        match_pt=None
        match_id=None
        match_added_pt.append(match_pt)
        match_added_obj.append(match_id) 


print len(match_added_pt), len(match_added_obj)
print len(match_added_pt)==len(match_added_obj)

#there are duplicates in match_added_pt and match_added_obj

#find the duplicates in object list and replace the duplicates with None

for i in set(match_added_obj):
   if match_added_obj.count(i)>1:
       print i
   else:
       continue
    
#move the removed sp to coor
####RuntimeError: Objects in this class cannot be updated outside an edit session [ELECDIST.ServicePoint]
####updatecursor can not work on selected table



####copy print to excel-->make a list of objectID of matched added sp

del_add=[]
for i in match_added_obj:
    if i is not None:
        print i
        del_add.append(i)
print len(del_add)

#make a list of match_added_obj in excel-->select them in service point-->delet them
#make a dictionary of removed sp id and added pt geomerty

remove_obj_added=dict(zip(remove_obj,match_added_pt))



def MOVE_A2Pt(a,pt):
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    where="OBJECTID={}".format(a)
    cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        row[0]=pt
        cursor.updateRow(row)
    edit.stopOperation()
    

#only move removed sp with added sp nearby
remove_obj_added2={key:v for (key,v) in remove_obj_added.items() if v is not None}


sp_move=[]
for key in remove_obj_added2:
    pt=remove_obj_added2[key]
    MOVE_r2a(key,pt)
    sp_move.append(key)

"""
old code
for sp in remove_obj:
    ii=remove_obj.index(sp)
    if coor[ii] is not None:
        try:
            print match_added_obj[ii],sp
            sp_move.append(sp)
            x="OBJECTID=" + str(sp)
            cur = arcpy.da.UpdateCursor(r"Customers & Transformers\Service Point",["SHAPE@XY"],x)
            for ro in cur:
                ro[0] = coor[ii]  
                cur.updateRow(ro)
        except:
            pass
      
##copy the print to excel
##make a list of moved removed_obj in excel-->select them in service point-->click ArcFm connect tool


