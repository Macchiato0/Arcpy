
"""
code to create points polylines
t_pt1=arcpy.Point(594307.222,543774.535)
t_pt2=arcpy.Point(594317.222,543784.535)
t_pl=arcpy.Polyline(arcpy.Array([t_pt1,t_pt2]))
"""

#first point
#make a list of last point for lines
#service points
cursor=arcpy.da.SearchCursor("Service Point selection",["OID@","SHAPE@","TLM"])
pt_list=[]
oid_list=[]
TLM_list=[]
for row in cursor:
    pt_list.append(row[1])
    oid_list.append(row[0])
    TLM_list.append(row[2])



#check if all tlm are avaiable
p=''
for i in set(TLM_list):
    tlm="'{}',".format(i)
    p=p+tlm
print p 
print len(set(TLM_list))


#collect tlm points as the first point of a line
pt_0=[]
pt0_phase=[]
for i in TLM_list:
    where="tlm='{}'".format(str(i))
    cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Secondary Transformers",["SHAPE@","PHASEDESIGNATION"],where)
    for row in cursor:
        pt_0.append(row[0])
        pt0_phase.append(row[1])


#zip point 0, point1, and the phase
pts_phase=zip(pt_0,pt_list,pt0_phase)


for i in pts_phase:
    t_pt1,t_pt2=i[0].firstPoint,i[1].firstPoint
    xyz=i[2]
    t_pl=arcpy.Polyline(arcpy.Array([t_pt1,t_pt2]))     
    cursor = arcpy.da.InsertCursor(r'E:\Data\yfan\sand_box.gdb\Sec_OH',["SHAPE@","PHASEDESIGNATION"]) 
    cursor.insertRow([t_pl,xyz])


#test sec_oh

cursor=arcpy.da.SearchCursor(r'E:\Data\yfan\sand_box.gdb\Sec_OH',["*"])
for i in cursor:
    print i

#arcpy.DeleteRows_management('Sec_OH')


