fid='011003'
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment',["OID@","SHAPE@"],"feederid='{}'".format(fid))
line_shp={k:v for (k,v) in cursor}
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.Transformer',["OID@","SHAPE@","TLM"],"feederid='{}'".format(fid))
tlm_shp={k:(v1,v2) for (k,v1,v2) in cursor}
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.ServicePoint',["OID@","SHAPE@","DEVICELOCATION"],"feederid='{}'".format(fid))
sp_shp={k:(v1,v2) for (k,v1,v2) in cursor}
cluster=[]        
cluster1=dict([line_shp.popitem()])
cluster2=cluster1 #temp store of clustered lines    
line_shp_temp=copy.deepcopy(line_shp)
        
# recursive method:
# search lines linked to [line1] 

def find_line(): #find the linked lines, lines=a.sub_cluster1
    line_cont={}
    for k1 in line_shp_temp:
        for k2 in cluster1:
            if cluster1[k2].distanceTo(line_shp[k1])==0:
                line_cont[k1]=line_shp.pop(k1)
                line_shp_temp=copy.deepcopy(line_shp)
    if len(line_cont)>0:
        cluster2.update(line_cont)
        cluster1={}
        cluster1.update(line_cont)
        find_line()
    elif len(line_cont)==0 and len(line_shp)>0:
        cluster.append(cluster2)
        cluster1=dict([line_shp.popitem()])
        line_shp_temp=copy.deepcopy(line_shp)
        cluster2={}
        cluster2.update(cluster1)
        find_line()
    else:
        return cluster
            
