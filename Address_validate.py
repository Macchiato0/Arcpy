# creat a layer of audit area complete-fail
# extract the address from the comment of very entry of field audit
# address=*+digit + two strings after the digit+*
import arcpy

cursor=arcpy.da.SearchCursor("AuditArea selection",["COMMENTS"])

comment=[row[0] for row in cursor]

# Street Address search in a string of comment


