import sys
sys.getrecursionlimit()
sys.setrecursionlimit(100000)

fid='011004'
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment',["OID@","SHAPE@","WIRETYPE"],"feederid='{}'".format(fid))
line_shp=[[i[0],[(int(i[1].firstPoint.X),int(i[1].firstPoint.Y)),(int(i[1].lastPoint.X),int(i[1].lastPoint.Y))],i[2]] for i in cursor]
