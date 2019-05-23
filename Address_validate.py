# creat a layer of audit area complete-fail
# extract the address from the comment of very entry of field audit
# address=*+digit + two strings after the digit+*
import arcpy

cursor=arcpy.da.SearchCursor("AuditArea selection",["COMMENTS"])

row_list=[row[0] for row in cursor]

# normalize and ignore some confused unicode data
import unicodedata
comment=[unicodedata.normalize('NFKD', i).encode('ascii','ignore') for i in row_list]

# Street Address search in a string of comment
import re

# split every string in cooment into word by word 
comment_split=[re.split("\s", i) for i in comment]

# parse the comment and select the address
# 1. assume that all street address start with a number, excludes the number of street (always in (0,100)) or the meter number (7 digits)
for i in comment_split:
    num1=[int(j) for j in i if j.isdigit() and 100<int(re.findall("\d+", j)[0])<10000]
    st_number=max(num1) if len(num1)>0 else None
    text_number='{}'.format(st_number) if st_number>0 else None
    position=i.index(text_number) if text_number in i else None
    address=i[position:position+3] if position else None 
    print address
    
    


    



