# _*_ coding: utf-8 _*_

"""
Pt.py by Yi Fan
"""
class Pt:
#A parent class of all point features classes on map: TLM, Service point, (other features could be added into child class
    feature_class={
            1:'ELECDIST.ServicePoint',
            2:'ELECDIST.Transformer'
    }
    def __init__(self, oid, f_class,feederid):
        self.oid = oid
        self.f_class = Pt.feature_class[f_class]
        self.feederid = feederid
    workspace = 'E:\\Data\\yfan\\Connection to dgsep011.sde'
    dataset='\\ELECDIST.ElectricDist\\'

#feederid: string
#f_class:1 or 2
#oid: integer, objectid of the feature
    def get_sde(self):
        data_source=Pt.workspace+Pt.dataset+Pt.f_class

#create the directory of sde data source

    def get_geom(self):
        cursor=arcpy.da.SearchCursor(self.get_sde(),["SHAPE@"],"OBJECTID={}".format(self.oid))
        for row in cursor:
            pt_geo=row[0]
        return pt_geo

#class method to get point geometry of a point from the sde data source

class Svp(Pt):
#child class for methodes of service points

    def find_TLM(self):
        

if __name__ == '__main__':
    print 'package initializing'
