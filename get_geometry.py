4497 sp without XY processed by DRG

where clause:"DRG is not null and LATITUDE is null and LONGITUDE is null"

#select the sp first  
def get_geometry():
    #make sure service points are selected
    selectedCount = len([int(fid) for fid in arcpy.Describe(r"Customers & Transformers\Service Point").fidset.split(";") if fid != ''])
    if selectedCount>0:
        cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Service Point",["OID@","SHAPE@XY"])
        A_list=[row for row in cursor]
        return A_list
    else:
        print "select points please"
      
      
    
    
  
  
