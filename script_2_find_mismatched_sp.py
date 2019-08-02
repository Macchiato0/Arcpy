select_oid = arcpy.da.SearchCursor("Service Point selection", ["OID@","TLM","SHAPE@"])

oid = [] #list of device location
tlm_spshp=[]#list of tlm, tlm should be in str because tlm may start at 0

# create a list of device location for every sp
for row1 in select_oid:
    x1 = row1[0]
    x2 = str(row1[1])
    x3=row1[2]
    oid.append(x1)
    tlm_spshp.append([x2,x3])


sp_tlm=dict(zip(oid,tlm_spshp))

        
for key in sp_tlm:
    a = sp_tlm[key][0]
    sel = "TLM = '{}'".format(a)
    select_tlm = arcpy.da.SearchCursor(r'Customers & Transformers\Secondary Transformers',["SHAPE@"], sel)
    for row in select_tlm: 
        sp_tlm[key].append(row[0])    

to_move_oid=[]
for key in sp_tlm:
    p1=sp_tlm[key][1]
    p2=sp_tlm[key][2]
    meter=p1.distanceTo(p2)
    if meter>200:
        to_move_oid.append(key)        
