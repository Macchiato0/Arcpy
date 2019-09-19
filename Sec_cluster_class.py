# a=sec_cluster('011003')

import arcpy
class sec_cluster:
    __slots__ : 'line_shp','fid','tlm_shp','sp_shp','cluster','sub_cluster','cluster2'
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
        self.sub_cluster=dict([self.line_shp.popitem()])
        self.cluster2=self.sub_cluster #temp store of clustered lines
    
# recursive method:
# search lines linked to [line1] 

    def _find_line(self,lines): #find the linked lines, lines=self.sub_cluster
        line_cont={}
        for k1 in lines:
            for k2 in self.sub_cluster:
                if lines[k1].distanceTo(self.sub_cluster[k2]):
                    line_cont[k1]= lines.pop(k1)
        if len(line_cont)>0:
            self.sub_cluster2.update(line_cont)
            self.sub_cluster=line_cont
            self._find_line(self.sub_cluster)
        elif len(line_cont)==0 and len(self.line_shp)>0:
            self.cluster.append(self.cluster2)
            self.sub_cluster=dict([self.line_shp.popitem()])
            self.cluster2=self.sub_cluster
            self._find_line(self.sub_cluster)
        else:
            break
            
        '''
        geo2={}
        if type(args[0]) is dict:
            args=[args[0][k] for k in args[0]]     
        for i in args:
            result=self._search_line(i)
            geo2.update(result)
            self.geo1.update(geo2)      
        if len(geo2)==0:
            return self.geo1
        else:
            self._find_line(geo2)    
        '''
        
    def sec_clusters(self):
        self.clusters=[]
        self.allKeys=self.sec_mn.keys()
        for k in self.allKeys:
            tg=0
            for cl in self.clusters:
                pls=[cl[1][key] for key in cl[1]]
                linked=[l for l in pls if l.distanceTo(self.sec_mn[k])==0]
                if len(linked)>0:
                    cl[0].append(k)
                    tg=1
            if tg==1:
                continue          
            self.geo1={}
            self._find_line(self.sec_mn[k])
            a_cluster=[[k],self.geo1]
            self.clusters.append(a_cluster)

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
        
                
        
        
    
