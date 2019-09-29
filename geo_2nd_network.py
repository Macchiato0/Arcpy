import sys
sys.getrecursionlimit()
sys.setrecursionlimit(10000)

fid='011004'

#create a list of secondary over head conductor
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment',["OID@","SHAPE@","WIRETYPE","WIRESIZE"],"feederid='{}'".format(fid))
line_shp=[[i[0],[(int(i[1].firstPoint.X),int(i[1].firstPoint.Y)),(int(i[1].lastPoint.X),int(i[1].lastPoint.Y))],i[2],i[3]] for i in cursor]

#line_shp[0]
#[11341189, [(559725, 230913), (559714, 230922)], u'Aluminum', u'4TX']
#i[1] [(559725, 230913), (559714, 230922)]
#create points based based on line_shp,oid is unique
pt_shp=[]
n=0
for i in line_shp:
  for j in i[1]:
    n+=1
    row=[n,j]
    pt_shp.append(row)
#swap coordinate tuple (x,y) with point id in pt_shp   
n=0
for i in line_shp:
  for j in range(len(i[1])):
    n+=1
    i[1][j]=n
        
#pt_shp[0]
#[1, (559725, 230913)]
#all points data are in the form [id,(x,y)]
#create list of service point
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.ServicePoint',["SHAPE@","DEVICELOCATION"],"feederid='{}'".format(fid))
sp_shp=[[i[1],(int(i[0].firstPoint.X),int(i[0].firstPoint.Y))] for i in cursor]

#create list of transformers
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.Transformer',["SHAPE@","TLM"],"feederid='{}'".format(fid))
tlm_shp=[[str(i[1]),(int(i[0].firstPoint.X),int(i[0].firstPoint.Y))] for i in cursor]

#sort pt,sp, and tlm @ Py_sort_search_data_structure/quick_sort_point.py 

#search and match pt with sp and tlm @ Py_sort_search_data_structure/binary_search_point.py











