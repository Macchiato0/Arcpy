arcpy.SelectLayerByLocation_management(r"Customers & Transformers\Secondary Transformers","INTERSECT",r"Primary Lines\Primary Overhead Conductor")
#<Result 'Customers & Transformers\\Secondary Transformers'>
'''
1.Primary OH and UG line segments connected directly to Transformer
does not work unless pause drawing
select the overhead primary connected to transformers
'''
arcpy.SelectLayerByLocation_management(r"Primary Lines\Primary Overhead Conductor","INTERSECT",r"Customers & Transformers\Secondary Transformers") 

#<Result 'Primary Lines\\Primary Overhead Conductor'>
#make a layer "primary_oh" of the selection

arcpy.MakeFeatureLayer_management(r"Primary Lines\Primary Overhead Conductor",'primary_oh')

#select the underground primary connected to transformers

arcpy.SelectLayerByLocation_management(r"Primary Lines\Primary Underground Conductor","INTERSECT",r"Customers & Transformers\Secondary Transformers"
                                       
#make a layer "primary_un" of the selection
arcpy.MakeFeatureLayer_management(r"Primary Lines\Primary Underground Conductor",'primary_un')  

'''                                       
2.PriOHElectricLineSegment (Subtype = 7) where they intersect Transformers (LOCATIONTYPE = PAD) vise versa
'''
#select padmont transformer and make a layer
arcpy.SelectLayerByAttribute_management(r"Customers & Transformers\Secondary Transformers","NEW_SELECTION","LOCATIONTYPE = 'PAD'")
#<Result 'Customers & Transformers\\Secondary Transformers'>
arcpy.MakeFeatureLayer_management(r"Customers & Transformers\Secondary Transformers",'Pad_transformers')                                 
#select the overhead primary lines connected to padmount transformers      
arcpy.SelectLayerByLocation_management("primary_oh","INTERSECT","Pad_transformers") 
#make a layer "primary_oh2pad_trans" of the selection
arcpy.MakeFeatureLayer_management(r"Primary Lines\Primary Overhead Conductor","primary_oh2pad_trans")
'''
if there is 0 selection in primary_oh, there will be no primary overhead connected to pad mounted transformers
'''
#select underground primary lines connected to pole transformer and make a layer
arcpy.SelectLayerByLocation_management("primary_un","INTERSECT","Pad_transformers")           
'''
if all primary_un is select, there will be no primary underground connected to pole transformers
'''                                       
arcpy.SelectLayerByAttribute_management("primary_un","SWITCH_SELECTION") 
arcpy.MakeFeatureLayer_management("primary_un","primary_un2pole_trans")                                       
                                       
