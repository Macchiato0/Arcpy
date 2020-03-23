import json
with open(r'E:\Data\yfan\sec_cir_update.json', 'rb') as fp:
    data_dict = json.load(fp)

where="SIXTEENTHSECTIONNAME like '{}%'".format(n)
cursor=arcpy.da.SearchCursor(r"CE Landbase\Sixteenth Section",["SHAPE@","SIXTEENTHSECTIONNAME"],where)


where="FEEDERID= '{}'".format(n)
cursor=arcpy.da.SearchCursor(r'Org Bounds\Circuit Boundaries',["FEEDERID","SHAPE@"],where)


sixteen_feed={}
for k in data_dict:
    if len(data_dict[k])==1:
        fd1=data_dict[k]
        where1="SIXTEENTHSECTIONNAME like '{}%'".format(k) 
        cursor1=arcpy.da.SearchCursor(r"CE Landbase\Sixteenth Section",["SIXTEENTHSECTIONNAME"],where1)
        for r1 in cursor1:
            sixteen_feed[r1]=fd1


for k in data_dict:
    if len(data_dict[k])>1:
        fd2=data_dict[k]
        fd2_poly=[]
        for fd in fd2:
            where_circuit="FEEDERID= '{}'".format(fd)
            cursor_circuit=arcpy.da.SearchCursor(r'Org Bounds\Circuit Boundaries',["SHAPE@"],where_circuit)
            for row_c in cursor_circuit:
                fd2_poly.append(row_c[0])
            
        where2="SIXTEENTHSECTIONNAME like '{}%'".format(k) 
        cursor2=arcpy.da.SearchCursor(r"CE Landbase\Sixteenth Section",["SIXTEENTHSECTIONNAME","SHAPE@"],where2)
        for r2 in cursor2:

            16_name=r2[0]
            16_poly=r2[1]
            sixteen_feed[16_name]=[]
            for n in range(len(fd2)):
                if 16_poly.overlaps(fd2_poly[n]) or fd2_poly[n].contains(16_poly):
                    sixteen_feed[16_name].append(fd2[n])
                else:
                    sixteen_feed[16_name]=fd2

#manually update the tiny circuit
