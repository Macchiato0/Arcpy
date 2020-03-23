import json
with open(r'E:\Data\yfan\sec_cir_update.json', 'rb') as fp:
    data_dict = json.load(fp)
'''
cursor template
where="SIXTEENTHSECTIONNAME like '{}%'".format(n)
cursor=arcpy.da.SearchCursor(r"CE Landbase\Sixteenth Section",["SHAPE@","SIXTEENTHSECTIONNAME"],where)


where="FEEDERID= '{}'".format(n)
cursor=arcpy.da.SearchCursor(r'Org Bounds\Circuit Boundaries',["FEEDERID","SHAPE@"],where)
'''

sixteen_feed={}
for k in data_dict:
    if len(data_dict[k])==1:
        fd1=data_dict[k]
        where1="SIXTEENTHSECTIONNAME like '{}%'".format(k) 
        cursor1=arcpy.da.SearchCursor(r"CE Landbase\Sixteenth Section",["SIXTEENTHSECTIONNAME"],where1)
        for r1 in cursor1:
            sixteen_feed[r1]=fd1

circuit={}
cursor_circuit=arcpy.da.SearchCursor(r'Org Bounds\Circuit Boundaries',["SHAPE@","FEEDERID"])
for row in cursor_circuit:
    fd=row[1]
    shp=row[0]
    circuit[fd]=shp

sixteen_feed_0=[]
for k in data_dict:
    if len(data_dict[k])>1:
        feederid=data_dict[k]
        feederid_set=set(feederid)
        fd2=list(feederid_set)

        fd2_poly=[]
        for f in fd2:
            fd2_poly.append(circuit[f])    
        nm=len(fd2)
        #print nm
        where2="SIXTEENTHSECTIONNAME like '{}%'".format(k) 
        cursor2=arcpy.da.SearchCursor(r"CE Landbase\Sixteenth Section",["SIXTEENTHSECTIONNAME","SHAPE@"],where2)        
        for r2 in cursor2:
            name_16=r2[0]
            
            poly_16=r2[1]
            #print name_16,poly_16
            sixteen_feed[name_16]=[]        
            for n in range(nm):               
                if poly_16.overlaps(fd2_poly[n]) or fd2_poly[n].contains(poly_16):
                    sixteen_feed[name_16].append(fd2[n])
                    #print 't'
            if len(sixteen_feed[name_16])==0:
                sixteen_feed_0.append(name_16)

#manually update the tiny circuit
