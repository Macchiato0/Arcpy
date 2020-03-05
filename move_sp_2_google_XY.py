# import google XY file to E drive

# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# move_sp_2_google_XY.py
# Created on: 2020-03-05 13:29
# (Author by Yi Fan)
# Description: 
# Move a servive point to google geocoded location
# ---------------------------------------------------------------------------

# Import arcpy module

import arcpy

# update shp variable first

shp='XY-address-Lat-Long'

def move_googleXY(oid,shp):
