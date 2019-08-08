
'''
select the tap points with LCP based on feederid
feederid in ('042101', '042102', '026801', '026802', '119601', '119602', '040201', '040202', '020502', '078201', '078202', '037001', '037002', '158901', '158902', '049801') and LCP is not Null
'''

import itertools



#delete the lable of tap points to close to each other
def get_close_tap(feederid): 
    where="feederid='{}'".format(feederid)
    cursor=arcpy.da.SearchCursor("Tap Dots, T-points, & Wire Changes selection",["OID@","SHAPE@","LCP"],where)
    rows=[q for q in cursor]
    rows2=[]
    #find the taps with a label
    tap1=[]
    tap2=[]
    tap3=[]
    for j in rows:     
        where2="FEATUREID={}".format(j[0])
        cursor1=arcpy.da.SearchCursor(r'Misc Network Features\Feature Linked Anno\MiscNetworkFeature_Label_300',["SHAPE@"],where2)
        cursor2=arcpy.da.SearchCursor(r'Misc Network Features\Feature Linked Anno\MiscNetworkFeature_Label_3200',["SHAPE@"],where2)
        cursor3=arcpy.da.SearchCursor(r'Misc Network Features\Feature Linked Anno\MiscNetworkFeature_Label_600',["SHAPE@"],where2)
        #apply try keywords to escape empty cursor error
        try:
            lable_shp300=[r1[0] for r1 in cursor1]
        except:
            pass
        try:
            lable_shp3200=[r2[0] for r2 in cursor2]
        except:
            pass
        try:
            lable_shp600=[r3[0] for r3 in cursor3]
        except:
            pass
        lable=lable_shp300+lable_shp3200+lable_shp600    
        if len(lable)>0:
            rows2.append(j)        
    for x,y in itertools.combinations(rows2, 2):
        meters=x[1].distanceTo(y[1])
        if 300<=meters<=400:
            tap3.append(x[0])
            tap3.append(y[0])
        elif 200<=meters<300:
            tap2.append(x[0])
            tap2.append(y[0])
        else:
            tap1.append(x[0])
            tap1.append(y[0])
    tapr1=list(set(tap1))
    tapr2=list(set(tap2))
    tapr3=list(set(tap3))
    tapr=[tapr1,tapr2,tapr3]
    return tapr 
   
'''
test taps
cursor=arcpy.da.SearchCursor("Tap Dots, T-points, & Wire Changes selection",["OID@"])
l1=[i[0] for i in cursor]
