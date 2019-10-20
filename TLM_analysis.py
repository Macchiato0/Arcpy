import csv
tlm=[]
sp_oid=[]
with open('E:\\Data\\ESME\\TLMAnalysis\\010702.csv') as csvfile:
  readCSV = csv.reader(csvfile, delimiter=',')
  for row in readCSV:
    tlm.append(row[2])
    sp_oid.append(row[3])
 
tlm.pop(0)
sp_oid.pop(0)

sp_tlm=zip(sp_oid,tlm)

def update_tlm(sp,tlm):
  workspace = r'E:\Data\yfan\Connection to dgsep011.sde'
  edit = arcpy.da.Editor(workspace)
  edit.startEditing(False, True)
  edit.startOperation()
  where="OBJECTID={}".format(sp)
  cursor=arcpy.da.UpdateCursor(r'E:\Data\yfan\Connection to dgsep011.sde\ELECDIST.ElectricDist\ELECDIST.ServicePoint',["TLM"],where)
  for row in cursor:
    row[0]=tlm
    cursor.updateRow(row)
  edit.stopOperation()
  
for i in sp_tlm:
  update_tlm(i[0],i[1])
