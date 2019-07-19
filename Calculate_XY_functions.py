#This script update the service points without x and y
#two ways to update the XY fields : field calculation and arcpy script updates
'''
4497 sp without XY processed by DRG
geo reference system 4269
''''

where clause:"DRG is not null and LATITUDE is null and LONGITUDE is null"

# get the XY of a point geometry in decimal degree
def get_XY_degree(pt):
    lat=pt.projectAs(arcpy.SpatialReference(4269)).firstPoint.Y
    lon=pt.projectAs(arcpy.SpatialReference(4269)).firstPoint.X
    coor=(lat,lon)
    return coor
"""
code has same function for field calculator
arcpy.PointGeometry(!Shape!.firstPoint,!Shape!.spatialReference).projectAs(arcpy.SpatialReference(4269)).firstPoint.Y
arcpy.PointGeometry(!Shape!.firstPoint,!Shape!.spatialReference).projectAs(arcpy.SpatialReference(4269)).firstPoint.X
"""
#decorator to get XY in decimal degree
def get_XY(func):
    def wrapper():
        A_list=[i[1] for i in func()]#a list of point geometry
        B_list=[i[0] for i in func()]#b list of point oid
        XY_list=map(get_XY_degree, A_list)
        m_t=lambda a,b : (a,b)
        result=map(m_t, B_list,XY_list)
        return result
    return wrapper

#select the sp first, output is point geometry 
@get_XY
def get_geometry():
    #make sure service points are selected
    selectedCount = len([int(fid) for fid in arcpy.Describe(r"Customers & Transformers\Service Point").fidset.split(";") if fid != ''])
    if selectedCount==0:
        cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Service Point",["OID@","SHAPE@"])
        A_list=[row for row in cursor]
        return A_list
    else:
        print "select points please"
        
        
def update_geometry():
    selectedCount = len([int(fid) for fid in arcpy.Describe(r"Customers & Transformers\Service Point").fidset.split(";") if fid != ''])
    if selectedCount==1:
        Lat=get_geometry()[0][1][0]
        Long=get_geometry()[0][1][1]
        cursor=arcpy.da.UpdateCursor(r"Customers & Transformers\Service Point",["LATITUDE","LONGITUDE","SHAPE@XY"])
        for row in cursor:
            row[0]=Lat
            row[1]=Long
            cursor.updateRow(row)
    else:
        print "select service point first"
        

    
        
      
      
    
    
  
  
