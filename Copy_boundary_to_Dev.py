# delete Bounary Feeder Go

workspace = r'Database Connections\Connection to (OMS-DEV-SDE).sde'
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()
cursor=arcpy.da.UpdateCursor(r'Database Connections\Connection to (OMS-DEV-SDE).sde\ELECDIST.ElectricDist_GO\ELECDIST.Boundary_Feeder_GO',"*", "FEEDERID = '061302'") 
for row in cursor:
    cursor.deleteRow()
edit.stopOperation()


# update Boundary Feeder Go

fields=["SHAPE@","FEEDERID","SUBSTATION","CIRCUIT","HDQ","VOLTAGE","SYSTEM_OWNER","OFFICE_PHONE","SYSTEM_ENGINEER","LVD_ENGINEER","PLANNER","SUBSTATIONID","CIRCUITID","STATUS"]
workspace = r'Database Connections\Connection to (OMS-DEV-SDE).sde'
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()
cursor=arcpy.da.SearchCursor("Boundary_feeder_Go selection",fields)
for row in cursor:
    cursor1=arcpy.da.InsertCursor(r'Database Connections\Connection to (OMS-DEV-SDE).sde\ELECDIST.ElectricDist_GO\ELECDIST.Boundary_Feeder_GO',fields)
    f=[i for i in row]
    cursor1.insertRow(f)
edit.stopOperation()
