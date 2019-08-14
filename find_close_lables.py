'''
select lable cluster

'''

import itertools



#delete the lable of tap points to close to each other

def get_close_lable(feederid): 
    layers=[
    r'Devices\Protective Devices & Switches\Fuse',
    r'Devices\Protective Devices & Switches\Switch',
    r'Devices\Protective Devices & Switches\Dynamic Protective Device',
    r'Devices\Primary Devices\Regulators & Boosters',
    r'Devices\Primary Devices\Isolator',
    r'Devices\Primary Devices\Capacitors'
    ]    
    where="feederid='{}'".format(feederid)
    oid,shp,lay=[],[],[]
    for layer in layers:
        cursor=arcpy.da.SearchCursor(layer,["OID@","SHAPE@"],where)
        for i in cursor:
            oid.append(i[0])
            shp.append(i[1]) 
            lay.append(layer) 
    cursor=arcpy.da.SearchCursor(r'Misc Network Features\Tap Dots, T-points, & Wire Changes',["OID@","SHAPE@"],where)
    for row in cursor:
        where2="FEATUREID={}".format(row[0])
        cursor1=arcpy.da.SearchCursor(r'Misc Network Features\Feature Linked Anno\MiscNetworkFeature_Label_300',["FEATUREID"],where2)
        for r1 in cursor1:
            if r1:
                oid.append(row[0])
                shp.append(row[1])
                lay.append(layer)            
        cursor2=arcpy.da.SearchCursor(r'Misc Network Features\Feature Linked Anno\MiscNetworkFeature_Label_3200',["FEATUREID"],where2)
        for r2 in cursor2:
            if r2:
                oid.append(row[0])
                shp.append(row[1])
                lay.append(layer)            
        cursor3=arcpy.da.SearchCursor(r'Misc Network Features\Feature Linked Anno\MiscNetworkFeature_Label_600',["FEATUREID"],where2)
        for r3 in cursor1:
            if r3:
                oid.append(row[0])
                shp.append(row[1])
                lay.append(layer)        
    #FIND THE CLUSTER
    Fuse_layer=           
    return oid 
'''
