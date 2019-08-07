'''
select the tap points with LCP based on feederid
feederid in ('129802','051101','051102','060203','060204','140701','140702','026501','026502','077201','077202') and LCP is not Null
'''

cursor=arcpy.da.SearchCursor("Tap Dots, T-points, & Wire Changes selection",["SHAPE@"])

