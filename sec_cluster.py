cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment',["OID@","SHAPE@"],"feederid='{}'".format(self.fid))
line_shp={k:v for (k,v) in cursor}
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.Transformer',["OID@","SHAPE@","TLM"],"feederid='{}'".format(self.fid))
tlm_shp={k:(v1,v2) for (k,v1,v2) in cursor}
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.ServicePoint',["OID@","SHAPE@","DEVICELOCATION"],"feederid='{}'".format(self.fid))
sp_shp={k:(v1,v2) for (k,v1,v2) in cursor}
cluster=[]        
cluster1=dict([self.line_shp.popitem()])
cluster2=self.cluster1 #temp store of clustered lines    
line_shp_temp=copy.deepcopy(self.line_shp)
        
# recursive method:
# search lines linked to [line1] 

def find_line(self): #find the linked lines, lines=a.sub_cluster1
    line_cont={}
    for k1 in self.line_shp_temp:
        for k2 in self.cluster1:
            if self.cluster1[k2].distanceTo(self.line_shp[k1])==0:
                line_cont[k1]=self.line_shp.pop(k1)
                self.line_shp_temp=copy.deepcopy(self.line_shp)
    if len(line_cont)>0:
        self.cluster2.update(line_cont)
        self.cluster1={}
        self.cluster1.update(line_cont)
        self.find_line(self)
    elif len(line_cont)==0 and len(self.line_shp)>0:
        self.cluster.append(self.cluster2)
        self.cluster1=dict([self.line_shp.popitem()])
        self.line_shp_temp=copy.deepcopy(self.line_shp)
        self.cluster2={}
        self.cluster2.update(self.cluster1)
        self.find_line(self)
    else:
        return self.cluster
            
