# 1.Create an empty list of tlm


# 2.check if the removed tlm have feederID and Search the delete/removed tlm in the database
#   update the feederID of floating tlm of the ciruit
#   select the removed tlm and create a cursor



# 3.check if the tlm in its town section(1 is ture, 0 is false)
#   create a list of tlm in the wrong town section
#   create a list of coordinates for the tlm to go
import arcpy
cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Secondary Transformers",["TLM","SHAPE@"])
tlm_move_to=[]
tlm_select=[]
for row in cursor:
    section_id=str(row[0])[:8]
    pt=row[1]
    sel="SIXTEENTHSECTIONNAME=" + "'"+section_id+"'"
    cur=arcpy.da.SearchCursor(r"CE Landbase\Sixteenth Section",["SHAPE@"], sel)
    for i in cur:
        section=i[0]
        if section.contains(pt):
            print '0'
        else:
            print "'"+row[0]+"'"
            trans = str(row[0])
            ctpnt=section.centroid
            location=ctpnt.X,ctpnt.Y
            tlm_move_to.append(location)
            tlm_select.append(trans)
    




for tlm in tlm_select:
    try:
        x = "TLM = " + "'"+tlm+"'"
        ii = tlm_select.index(tlm) 
        cur = arcpy.da.UpdateCursor(r"Customers & Transformers\Secondary Transformers",["SHAPE@XY"],x) 
        for ro in cur:
            ro[0] = tlm_move_to[ii]    
            cur.updateRow(ro)
    except:
        pass                




return len(tlm_move_to),len(tlm_select)



# 4. move the tlm to their corresponding town section
#    create a layer of tlm selected

for tlm in tlm_select:
    try:
        x = "TLM = " + "'"+tlm+"'"
        ii = tlm_select.index(tlm) 
        cur = arcpy.da.UpdateCursor(r"Customers & Transformers\Secondary Transformers",["SHAPE@XY"],x) 
        for ro in cur:
            ro[0] = tlm_move_to[ii]    
            cur.updateRow(ro)
    except:
        pass   


print len(tlm_move_to),len(tlm_select)

