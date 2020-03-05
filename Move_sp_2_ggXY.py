#import to E drive

# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# import_boundary.py
# Created on: 2020-03-05 
#   (Author by Yi Fan)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
gg_file="XY-address-Lat-Long"

cursor=arcpy.da.SearchCursor(gg_file,["OID_","Lat","Long"])

ggxy={row[0]:(row[1],row[2]) for row in cursor}

def move_p2gg(oid,ggxy):
    workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    
    for row in cursor:
        pt=row[0]
    where="OBJECTID={}".format(a)
    cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        row[0]=pt
        cursor.updateRow(row)
    edit.stopOperation()
