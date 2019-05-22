1. make sure the removed sp are not connected to the network


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

cursor = arcpy.da.SearchCursor("Service Point selection 2",["SHAPE@","OID@"])

for i in cursor:
    added_pt.append(i[0])
    added_obj.append(i[1])

print len(added_pt), len(added_obj)
print len(added_pt)==len(added_obj)

#calculate the distance between removed and added 
#if minimum distance less than 90, the remove and added should be the couple

match_added_pt=[]
match_added_obj=[]
for i in remove_pt:
    meters=[]
    for j in added_pt:
        dist=i.distanceTo(j)
        meters.append(dist)
    added_i=meters.index(min(meters))
    if min(meters)<30:   
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
    if i is not None:
        print i
        while match_added_obj.count(i)>1:
            po=match_added_obj.index(i)
            match_added_obj[po]=None
            print po

#check if None is the only duplicates
for i in set(match_added_obj):
    n=match_added_obj.count(i)
    if n>1:
        print i


#replace the duplicates in point list with None based on ID list

for i in range(len(match_added_obj)):
    if match_added_obj[i]==None:
        match_added_pt[i]=None

#check if None is the only duplicates
for i in set(match_added_pt):
    n=match_added_pt.count(i)
    if n>1:
        print i 

#move the removed sp to the added sp

#create a list of XY tuple for the matched added sp
coor = []

for i in match_added_pt:
    if i is not None:
        pt=i.centroid.X, i.centroid.Y
        coor.append(pt)
    else:
        coor.append(None)
    
#move the removed sp to coor
####RuntimeError: Objects in this class cannot be updated outside an edit session [ELECDIST.ServicePoint]
####updatecursor can not work on selected table



####copy print to excel-->make a list of objectID of matched added sp

del_add=[]
for i in match_added_obj:
    if i is not None:
        print i
        del_add.append(i)

#make a list of match_added_obj in excel-->select them in service point-->delet them

sp_move=[]
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


