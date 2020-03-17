#import to E drive
#
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# import Move_sp_2_ggXY.py
# Created on: 2020-03-05 
# Author by Yi Fan
# Description: 
# X is long Y is lat
# ---------------------------------------------------------------------------

# Import arcpy module

import arcpy

gg_file='XYBay-City-Address'

cursor=arcpy.da.SearchCursor(gg_file,["OID_","Lat","Long"])

ggxy={row[0]:(row[1],row[2]) for row in cursor}

def move_p2gg(oid,shp):
    workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
    edit = arcpy.da.Editor(workspace)
    edit.startEditing(False, True)
    edit.startOperation()
    xy=shp[oid]
    point = arcpy.Point(xy[1]-5,xy[0]-5)
    ptGeometry = arcpy.PointGeometry(point)
    where="OBJECTID={}".format(oid)
    cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["SHAPE@"],where)
    for row in cursor:
        row[0]=ptGeometry
        cursor.updateRow(row)
    edit.stopOperation()
