# creat a layer of audit area complete-fail
# extract the address from the comment of very entry of field audit
# address=*+digit + two strings after the digit+*
import arcpy

cursor=arcpy.da.SearchCursor("AuditArea selection",["COMMENTS"])

row_list=[row[0] for row in cursor]

#normalize and ignore some confused unicode data

comment=[unicodedata.normalize('NFKD', i).encode('ascii','ignore') for i in row_list]

# Street Address search in a string of comment

import re

# split every string in cooment into word by word 
comment_split=[re.split("\s", i) for i in comment]


