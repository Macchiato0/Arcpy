# creat a layer of audit area complete-fail
# extract the address from the comment of very entry of field audit
# address=*+digit + two strings after the digit+*
import arcpy

cursor=arcpy.da.SearchCursor("AuditArea selection",["COMMENTS"])
row_list=[row[0] for row in cursor]
cursor=arcpy.da.SearchCursor("AuditArea selection",["OBJECTID"])
row_oid=[row[0] for row in cursor]

# normalize and ignore some confused unicode data
import unicodedata
comment=[unicodedata.normalize('NFKD', i).encode('ascii','ignore') for i in row_list]

# Street Address search in a string of comment
import re

# split every string in cooment into word by word 
comment_split=[re.split("\s", i) for i in comment]

# parse the comment and select the address
# 1. assume that all street address start with a number, excludes the number of street (always in (0,100)) or the meter number (7 digits)
# 2. creat a hashable Audit_id_address_1 dataset with key as audit area id and value as the parsed address
Audit_id_address_1={}
for i in comment_split:
    num1=[int(j) for j in i if j.isdigit() and 100<int(re.findall("\d+", j)[0])<10000]
    st_number=max(num1) if len(num1)>0 else None
    text_number='{}'.format(st_number) if st_number>0 else None
    position=i.index(text_number) if text_number in i else None
    address_list=i[position:position+3] if position else None
    address=' '.join(address_list) if address_list else None
    address1=address.replace(".",'') if address else None
    address2=address1.replace(",",'') if address1 else None
    Audit_id_address_1[row_oid[comment_split.index(i)]]=address2
    
# 3. select parsed Audit_id_address_1 from address table and find the oid of service point
# 4. create a hashable dictionary key as Audit_area oid and value as service point oid. 
Audit_Sp={}
for key in Audit_id_address_1:
    street_string="STREET like '%{}%'".format(Audit_id_address_1[key]) 
    cursor=arcpy.da.SearchCursor("ELECDIST.ServiceAddress",["SERVICEPOINTOBJECTID"],street_string) 
    for row in cursor:
        sp_oid=row[0]
    #print sp_oid    
    Audit_Sp[key]=sp_oid
    
# 5. check if the Audit_Area and Service Point are at the right location by go through Audit_Area and service point in  
Audit_Sp


# 6. check if all the audit_area has a coresponding service point

#
    



