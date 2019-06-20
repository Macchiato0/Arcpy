#move the disconnected service points to the correct tlm

def move_point(it):
    select_id='OBJECTID='+str(it)
    select_tlm = arcpy.da.SearchCursor(r"Customers & Transformers\Service Point", ["TLM"], select_id)
    for row in select_tlm:
        tlm=str(row[0])
    section=tlm[0:8]
    sel="SIXTEENTHSECTIONNAME=" + "'"+section+"'"
    select_section=arcpy.da.SearchCursor(r"CE Landbase\Sixteenth Section",["SHAPE@"], sel)
    for i in select_section:
        location = i[0]
        pnt=location.centroid
        coordinate=pnt.X,pnt.Y
    update_pt = arcpy.da.UpdateCursor(r"Customers & Transformers\Service Point", ["SHAPE@"])
    for ro in update_pt:
        try:
            ro[0] = coordinate
            update_pt.updateRow(ro)
        except:
            pass
    return it


#update the coordinate by applying moving function
