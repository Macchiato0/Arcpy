!!4497 sp without XY processed by DRG

!! geo reference system 4269

where clause:"DRG is not null and LATITUDE is null and LONGITUDE is null"

#select the sp first, output is point geometry  
def get_geometry():
    #make sure service points are selected
    selectedCount = len([int(fid) for fid in arcpy.Describe(r"Customers & Transformers\Service Point").fidset.split(";") if fid != ''])
    if selectedCount>0:
        cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Service Point",["OID@","SHAPE@"])
        A_list=[row for row in cursor]
        return A_list
    else:
        print "select points please"

# get the XY of a point geometry in decimal degree
deg get_XY_degree(pt):
    lat=pt.projectAs(arcpy.SpatialReference(4269)).firstPoint.Y
    long=pt.projectAs(arcpy.SpatialReference(4269)).firstPoint.X
    coor=(lat,long)
    return coor

#decorator for 
def get_XY(func):
    def wrapper():
        A_list=[i[1] for i in func()]#a list of point geometry
        result=map(get_XY_degree, A_list)
        return result
    return wrapper
        
        
        
        
        
        
def update_geometry():
    selectedCount = len([int(fid) for fid in arcpy.Describe(r"Customers & Transformers\Service Point").fidset.split(";") if fid != ''])
    if selectedCount>0:
        cursor=arcpy.da.UpdateCursor(r"Customers & Transformers\Service Point",["LATITUDE","LONGITUDE","SHAPE@XY"])
        

    
        
      
      
    
    
  
  
