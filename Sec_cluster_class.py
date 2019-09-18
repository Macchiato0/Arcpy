# a=sec_cluster('011003')

import arcpy
class sec_cluster:
    __slots__ = 'line_shp','fid','tlm_shp','sp_shp'
    def __init__(self,fid): #name type is string, input is feederid
        self.fid=fid

    def get_data(self): #extract lines and nodes from database
        cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment',["OID@","SHAPE@"],"feederid='{}'".format(self.fid))
        self.line_shp={k:v for (k,v) in cursor}
        cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.Transformer',["OID@","SHAPE@","TLM"],"feederid='{}'".format(self.fid))
        self.tlm_shp={k:(v1,v2) for (k,v1,v2) in cursor}
        cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.ServicePoint',["OID@","SHAPE@","DEVICELOCATION"],"feederid='{}'".format(self.fid))
        self.sp_shp={k:(v1,v2) for (k,v1,v2) in cursor}
        
    '''            
    def _search_line(self,pt): #inner function for class method based on deletion searching
        result={}
        for k in self.line_shp:
            if self.line_shp[k].distanceTo(pt)==0:
                result[k]=self.sec_line[k]
        for key in result:
            del self.sec_line[key]
        return result
    '''
    
# recursive method:
# search 1[lines] linked to a point --> search 2[lines] linked to 1[lines]......
# return when no line found linked to n[lines]

    def _find_line(self): #find the linked lines
        sub_cluster=dict([self.line_shp.popitem()])
        sub_iter,line_iter=sub_cluster.iteritems(),line_iter.iteritems()
        #sub_iter,sup_iter=sub_cluster.itervalues(),**kwargs.itervalues()
        while (len(self.line_shp)<1):
        l1,l2=sub_iter.next(),line_iter.next()
        sub_cluster=[]
        if l1[1].distanceTo(l2[1])==0
            sub_cluster[l2[0]]=self.line_shp.pop(l2[0])
         
        
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
        
                
        
        
    
