class sec_cluster:
    #__slots__ : 'line_shp','fid','tlm_shp','sp_shp','cluster','sub_cluster','cluster2'
    def __init__(self,fid): #name type is string, input is feederid
        self.fid=fid

    def get_data(self): #extract lines and nodes from database
        cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment',["OID@","SHAPE@"],"feederid='{}'".format(self.fid))
        self.line_shp={k:v for (k,v) in cursor}
        cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.Transformer',["OID@","SHAPE@","TLM"],"feederid='{}'".format(self.fid))
        self.tlm_shp={k:(v1,v2) for (k,v1,v2) in cursor}
        cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.ServicePoint',["OID@","SHAPE@","DEVICELOCATION"],"feederid='{}'".format(self.fid))
        self.sp_shp={k:(v1,v2) for (k,v1,v2) in cursor}
        self.cluster=[]        
        self.cluster1=dict([self.line_shp.popitem()])
        self.cluster2=self.cluster1 #temp store of clustered lines    
        self.line_shp_temp=self.line_shp
        
# recursive method:
# search lines linked to [line1] 
    def find_line(self,lines): #find the linked lines, lines=a.sub_cluster
        line_cont={}
        for k1 in self.line_shp:
            for k2 in lines:
                if lines[k2].distanceTo(self.line_shp_temp[k1])==0:
                    line_cont[k1]=self.line_shp.pop(k1)
                    self.line_shp_temp=self.line_shp
        if len(line_cont)>0:
            self.cluster2.update(line_cont)
            self.cluster1={}
            self.cluster1.update(line_cont)
            self.find_line(self.cluster1)
        elif len(line_cont)==0 and len(self.line_shp)>0:
            self.cluster.append(self.cluster2)
            self.cluster1=dict([self.line_shp.popitem()])
            self.cluster2={}
            self.cluster2.update(self.cluster1)
            self.find_line(self.cluster1)
        else:
            return self.cluster
            

        
   
'''
a=sec_cluster('011003')
a.get_data()
a.find_line(a.cluster1)
'''

def find_line(lines): #find the linked lines, lines=a.sub_cluster
    line_cont=[]
    global cluster1
    global cluster2
    global cluster
    global l
    for i in lines:
        for j in cluster1:
            if i[1].distanceTo(j[1])==0:
                line_cont.append(i)
                l.remove(i)
    if len(line_cont)>0:
        cluster2.update(line_cont)
        cluster1=line_cont
        find_line(cluster1)
    elif len(line_cont)==0 and len(l)>0:
        cluster.append(cluster2)
        cluster1=dict([l.popitem()])
        cluster2=cluster1
        find_line(cluster1)
    else:
        return cluster

















    def link_tlm(self):
        for cl in self.clusters:
            pls=[cl[1][key] for key in cl[1]]
            for key in self.tlm_sh:
                linked=[l for l in pls if l.distanceTo(self.tlm_sh[key][0])==0]
                if len(linked)>0:
                    cl.append(self.tlm_sh[key][1])
                    break

    
    def regroup(self):
        volt=[x for x in self.voltage_list if x is not None]
        self.v_group={}
        for v in volt:
            self.v_group[v]=[]
            for i in self.all_tap:
                if i[1]==v:
                    self.v_group[v].append(i[0])

    def main(self):
        self.feederid()
        self.get_data()
        self.get_pri_volt()
        self.sec_clusters()
        self.link_tlm()
        self.all_volt()
        self.regroup()
                    
if __name__ == "__main__":
  a=tap('070201')
  a.main()
        
                
        
        
    
