# _*_ coding: utf-8 _*_ 
# By Yi Fan
'''
goal: draw clusters based on nodes 
'''
import arcpy
class tap:
    def __init__(self,name): #name type is string, input is feederid
        self.name=name
    def feederid(self):
        self.where="feederid='{}'".format(self.name)
        print self.where
    def get_data(self): #extract lines and nodes from database
        cursor1=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.PriOHElectricLineSegment',["OID@","SHAPE@","OPERATINGVOLTAGE"],self.where)
        self.primary_line={key:(v1,v2) for (key,v1,v2) in cursor1}
        cursor2=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.PriUGElectricLineSegment',["OID@","SHAPE@","OPERATINGVOLTAGE"],self.where)
        self.primary_un_pl={key:(v1,v2) for (key,v1,v2) in cursor2}
        self.primary_line.update(self.primary_un_pl)
        cursor3=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.MiscNetworkFeature',["OID@","SHAPE@"],self.where+"and NETWORKLEVEL=500")
        self.mns_pt={key:v for (key,v) in cursor3}
        self.voltage_list=list(set(self.primary_line[key][1] for key in self.primary_line))
        cursor4=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.MiscNetworkFeature',["OID@","SHAPE@"],self.where+"and NETWORKLEVEL in (200,100)")
        self.sec_mn={k:v for (k,v) in cursor4}
        cursor5=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment',["OID@","SHAPE@"],self.where)
        self.sec_line={k:v for (k,v) in cursor5}
        cursor6=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecUGElectricLineSegment',["OID@","SHAPE@"],self.where)
        self.sec_un={k:v for (k,v) in cursor6}
        self.sec_line.update(self.sec_un)
        cursor7=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.Transformer',["OID@","SHAPE@","OPERATINGVOLTAGE"],self.where)
        self.tlm_sh={k:[v1,v2] for (k,v1,v2) in cursor7}
    def _find_volt(self,pt,line_dict):  #find voltage of all lines
        for key in line_dict:
            if line_dict[key][0].distanceTo(pt)==0:
                if line_dict[key][1]!=None:
                    return line_dict[key][1]
                else:
                    None
            else:
                None
    def get_pri_volt(self):       #add voltage to lines
        self.mn_pri=[]
        for k in self.mns_pt:
            t=(k,self._find_volt(self.mns_pt[k],self.primary_line))
            if t[1] is not None:
                self.mn_pri.append(t)
    def _search_line(self,pt):  #inner function for class method based on deletion searching
        result={}
        for k in self.sec_line:
            if self.sec_line[k].distanceTo(pt)==0:
                result[k]=self.sec_line[k]
        for key in result:
            del self.sec_line[key]
        return result
'''
recursive method:
search 1[lines] linked to a point --> search 2[lines] linked to 1[lines]......
return when no line found linked to n[lines]
'''
    def _find_line(self,*args): #*args could be a point a line or a tuple of lines
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
    def all_volt(self):
        sec_mn_volt=[]
        for i in self.clusters:
            if len(i)==3:
                for j in i[0]:
                    t=(j,i[2])
                    sec_mn_volt.append(t)
        self.all_tap=self.mn_pri+sec_mn_volt
    
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
  a=tap('060202')
  a.main()
        
                
        
        
    




      
