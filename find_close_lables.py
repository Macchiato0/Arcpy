'''
select lable cluster

'''

# import itertools



#delete the lable of tap points to close to each other

def get_close_lable(feederid): 
    layers=[r'Misc Network Features\Feature Linked Anno\MiscNetworkFeature_Label_300',
    r'Misc Network Features\Feature Linked Anno\MiscNetworkFeature_Label_3200',
    r'Misc Network Features\Feature Linked Anno\MiscNetworkFeature_Label_600',
    r'Customers & Transformers\Feature Linked Anno\PrimaryMeter_Label_300',
    r'Customers & Transformers\Feature Linked Anno\PrimaryMeter_Label_600',
    r'Customers & Transformers\Feature Linked Anno\PrimaryMeter_Label_3200',
    r'Devices\Protective Devices & Switches\Feature Linked Anno\DynamicProtectiveDevice_Label_300',
    r'Devices\Protective Devices & Switches\Feature Linked Anno\DynamicProtectiveDevice_Label_600',
    r'Devices\Protective Devices & Switches\Feature Linked Anno\DynamicProtectiveDevice_Label_3200',
    r'Devices\Protective Devices & Switches\Feature Linked Anno\Fuse_Label_300',
    r'Devices\Protective Devices & Switches\Feature Linked Anno\Fuse_Label_600',
    r'Devices\Protective Devices & Switches\Feature Linked Anno\Fuse_Label_3200',
    r'Devices\Protective Devices & Switches\Feature Linked Anno\Switch_Label_300',
    r'Devices\Protective Devices & Switches\Feature Linked Anno\Switch_Label_600',
    r'Devices\Protective Devices & Switches\Feature Linked Anno\Switch_Label_3200',
    r'Devices\Primary Devices\Feature Linked Anno\PFCorrectingEquipment_Label_300',
    r'Devices\Primary Devices\Feature Linked Anno\PFCorrectingEquipment_Label_600',
    r'Devices\Primary Devices\Feature Linked Anno\PFCorrectingEquipment_Label_3200',
    r'Devices\Primary Devices\Feature Linked Anno\Transformer_Label_300',
    r'Devices\Primary Devices\Feature Linked Anno\Transformer_Label_600',
    r'Devices\Primary Devices\Feature Linked Anno\Transformer_Label_3200',
    r'Devices\Primary Devices\Feature Linked Anno\VoltageRegulator_Label_300',
    r'Devices\Primary Devices\Feature Linked Anno\VoltageRegulator_Label_600',
    r'Devices\Primary Devices\Feature Linked Anno\VoltageRegulator_Label_3200']    
    where="feederid='{}'".format(feederid)
    oid,shp=[],[]
    for layer in layers:
        cursor=arcpy.da.SearchCursor(layer,["OID@","SHAPE@"],where)
        for i in cursor:
            oid.append(i[0])
            shp.append(i[1])     
    return oid 
'''
