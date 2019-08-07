'''
select the tap points with LCP based on feederid
feederid in ('129802','051101','051102','060203','060204','140701','140702','026501','026502','077201','077202') and LCP is not Null
'''
feederid=['129802','051101','051102','060203','060204','140701','140702','026501','026502','077201','077202']

for i in feederid: 
    where="feederid='{}'".format(i)
    cursor=arcpy.da.SearchCursor("Tap Dots, T-points, & Wire Changes selection",["OID@","SHAPE@"],where)
    rows=[i for i in cursor]
    #oids=[i[0] for i in rows]
    #pts=[i[1] for i in rows]
    print rows
    tap0=list(filter(lambda a[1],b[1]: a[1].distanceTo(b[1])<500,rows))
    tap1=[i[0] for i in tap0]
    print tap1
