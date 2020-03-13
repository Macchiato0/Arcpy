#import to E drive
#
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# import create_section_ciruits_selection.py
# Created on: 2020-03-11 
# Author by Yi Fan
# Description: 
# select the circuits within every section polygon and create a spread sheet
# ---------------------------------------------------------------------------

# Import arcpy module

import arcpy
from functools import reduce

#select all the section polygons overlapping with circuit boundary

cursor=arcpy.da.SearchCursor('Circuit Boundaries',["SHAPE@"])
shp=[row[0] for row in cursor]

union_circuit_boundary=reduce(lambda a,b : a.union(b),shp)

cursor = arcpy.da.InsertCursor(r'E:\Data\yfan\sand_box.gdb\myfeatures',["SHAPE@"]) 
cursor.insertRow([union_circuit_boundary])

#select all sections in circuits boundary
arcpy.SelectLayerByLocation_management("SectionName","INTERSECT","myfeatures")

arcpy.MakeFeatureLayer_management("SectionName",'sectionXcircuits')

#make a grid reference on the map and select a set of sectionXcircuits and circuits boundary

cursor=arcpy.da.SearchCursor(r'Org Bounds\Circuit Boundaries',["FEEDERID","SHAPE@"])
circuit_shp=[]
circuit_fd=[]
for row in cursor:
    circuit_fd.append(row[0])
    circuit_shp.append(row[1])
    
sec_shp=[]
sec_nm=[]
cursor=arcpy.da.SearchCursor("sectionXcircuits",["SECTIONNAME","SHAPE@"])
for row in cursor:
    sec_nm.append(row[0])
    sec_shp.append(row[1])

#calculate the overlapping section and circuits
def get_sec_cir(circuit_shp,circuit_fd,sec_shp,sec_nm):
    sec_cir={}
    for i in range(len(sec_nm)):
        sec_cir[sec_nm[i]]=[]  
        for j in range(len(circuit_fd)):
            if sec_shp[i].overlaps(circuit_shp[j]):  
                sec_cir[sec_nm[i]].append(circuit_fd[j])
    return sec_cir

sec_cir1=get_sec_cir(circuit_shp,circuit_fd,sec_shp,sec_nm)

#select a new area of section and circuit and create new circuit_shp,circuit_fd,sec_nm,sec_shp

sec_cir2=get_sec_cir(circuit_shp,circuit_fd,sec_shp,sec_nm)

sec_cir3=get_sec_cir(circuit_shp,circuit_fd,sec_shp,sec_nm)

sec_cir4=get_sec_cir(circuit_shp,circuit_fd,sec_shp,sec_nm)

sec_cir5=get_sec_cir(circuit_shp,circuit_fd,sec_shp,sec_nm)

sec_cir6=get_sec_cir(circuit_shp,circuit_fd,sec_shp,sec_nm)

sec_cir7=get_sec_cir(circuit_shp,circuit_fd,sec_shp,sec_nm) 

def merge(dict1,dict2):
    keys1=set(list(dict1.keys())) 
    keys2=set(list(dict2.keys())) 
    join=keys1&keys2
    if len(join)==0:
        return dict(dict1.items()+dict2.items())
    else:
        for i in join:
            if dict1[i]==dict2[i]:
                dict2.pop(i)
            else:
                temp=list(set(dict1[i]+dict2[i]))             
                dict1[i]=temp
                dict2.pop(i)
        return dict(dict1.items()+dict2.items())



sec_cir_merge=reduce(lambda a,b : merge(a,b),[sec_cir1,sec_cir2,sec_cir3,sec_cir4,sec_cir5,sec_cir6,sec_cir7])     

#dump dictionary to json file

sec_cir_merge

import json
with open(r'E:\Data\yfan\sec_cir.json', 'w') as fp:
    json.dump(sec_cir_merge, fp)

#examin section with more than 6 circuits

check_section=[key for key in sec_cir_merge if len(sec_cir_merge[key])>6]
check_section_str=[str(i) for i in check_section]
[u'125402', u'125403', u'531104', u'075615', u'075614', u'075613', u'075612', u'085625', u'520812', u'055635', u'101634', u'101633', u'101632', u'040115', u'075718', u'061123', u'520801', u'145216', u'075622', u'075621', u'521213', u'071119', u'061106', u'145224', u'061225', u'081127', u'075730', u'075731', u'020108', u'061218', u'101629', u'040122', u'061124', u'071235', u'520133', u'520135', u'520134', u'071121', u'071120', u'140414', u'125416', u'125413', u'061236', u'531115', u'061030', u'125519', u'075704', u'075707', u'075706', u'521126', u'521125', u'521123', u'521122', u'125426', u'125427', u'125424', u'125425', u'125423', u'071214', u'071213', u'075729', u'521115', u'530103', u'530102', u'061118', u'061114', u'061117', u'061111', u'061110', u'061113', u'071224', u'071225', u'071223', u'065709', u'061018', u'061019', u'071130', u'510832', u'220933']

#create a file of sec_cir_merge
#select service point intersect with checked section
#Try:
#arcpy.SelectLayerByAttribute_management("SectionName","NEW_SELECTION","SECTIONNAME=125403")
sec_cir_check={}
mxd = arcpy.mapping.MapDocument("CURRENT")
for i in check_section:
    arcpy.SelectLayerByAttribute_management("SectionName","NEW_SELECTION","SECTIONNAME={}".format(i))
    arcpy.MakeFeatureLayer_management("SectionName","SectionName{}".format(i))
    arcpy.SelectLayerByLocation_management(r"Customers & Transformers\Service Point","INTERSECT","SectionName{}".format(i))
    cursor=arcpy.da.SearchCursor(r"Customers & Transformers\Service Point",["FEEDERID"])
    feed=list(set([row[0] for row in cursor]))
    feed1=list(filter(None, feed)) 
    sec_cir_check[i]=feed1
    for df in arcpy.mapping.ListDataFrames(mxd):
        for lyr in arcpy.mapping.ListLayers(mxd, "*",df):
            if lyr.name == "SectionName{}".format(i):
                arcpy.mapping.RemoveLayer(df, lyr)

'''
sec_cir_check      
{u'125426': [u'002903', u'117701', u'033901', u'050502', u'139601', u'050501', u'039301', u'039303', u'039302'], u'125427': [u'021701', u'033901', u'033903', u'033902', u'039303', u'039302'], u'125402': [u'111803', u'111802', u'111801', u'111804', u'035202', u'072304'], u'125403': [u'099101', u'111803', u'072304', u'111804'], u'075622': [u'022401', u'115901', u'028901', u'028903', u'028902'], u'125423': [u'021703', u'050502', u'050503', u'050501', u'072301', u'109201', u'039301', u'039303'], u'520812': [u'008503', u'008506', u'078405', u'078406', u'078401', u'078403', u'078402', u'036002', u'036004', u'021902'], u'075621': [u'022402', u'022403', u'022401', u'104404', u'104406', u'028901', u'028903'], u'125413': [u'034101', u'035201', u'072302', u'034103', u'034104', u'034105', u'109202', u'109201'], u'075718': [u'106601', u'106603', u'106602', u'006105', u'006104', u'106504', u'006106', u'106502', u'006107'], u'075707': [u'052303', u'006106', u'006108', u'090601', u'058601', u'106504', u'070103', u'070104', u'070105', u'006103', u'006105', u'006101'], u'075706': [u'090601', u'058604', u'090602', u'058601', u'090103'], u'521126': [u'021202', u'060803', u'060801', u'021203', u'080401', u'060804', u'113601'], u'521125': [u'134803', u'060801', u'060802', u'060803', u'060804', u'060805', u'113603', u'113601'], u'125425': [u'002901', u'002903', u'002902', u'002904', u'072402', u'050501', u'057702', u'017503', u'017502'], u'521123': [u'083301', u'060801', u'068604', u'021202', u'060804', u'076511'], u'521122': [u'036901', u'021201', u'068604', u'021202', u'068602', u'068603', u'068601', u'076502', u'076508', u'076509', u'076511', u'076510', u'076505'], u'520133': [u'021802', u'021801', u'090802', u'066802', u'066801', u'078703', u'124403', u'124402'], u'065709': [u'002303', u'009801', u'009802', u'006202', u'006203', u'006201', u'117903'], u'531104': [u'063401', u'122602', u'063403', u'135301', u'063404', u'135302', u'027502'], u'145224': [u'097201', u'108801', u'108803', u'108804', u'147802', u'108802'], u'020108': [u'114202', u'114203', u'114201', u'135902', u'135903', u'135904', u'135905'], u'531115': [u'024404', u'135303', u'024401', u'024402', u'166401'], u'061236': [u'041104', u'041102', u'091703', u'091701', u'066503'], u'040122': [u'060401', u'060402', u'115005', u'115004', u'115002', u'115001'], u'125424': [u'002902', u'002904', u'034103', u'050502', u'050503', u'050501', u'072301', u'057702', u'109201', u'109202', u'066902', u'066905', u'066904'], u'101629': [u'041302', u'041303', u'077601', u'000702', u'000705', u'060702'], u'071224': [u'077404', u'077401', u'077402', u'077403', u'119801', u'070802', u'152303', u'049203', u'049202', u'065801', u'054804', u'054802', u'054801', u'044007', u'044004'], u'071225': [u'010008', u'010914', u'010911', u'010913', u'010912', u'010921', u'077404', u'077403', u'010904', u'061805', u'010906', u'010907', u'010922', u'010923', u'010902', u'010903', u'010901', u'010909', u'010005', u'010003', u'044005', u'044003', u'044001'], u'071223': [u'010001', u'069902', u'077401', u'077402', u'049202'], u'085625': [u'090601', u'064704', u'027801', u'064705', u'090101'], u'061019': [u'203401', u'136804', u'130906', u'090501', u'130902', u'090504'], u'061018': [u'130906', u'130903', u'130902', u'130901'], u'075730': [u'018102', u'018101', u'074301', u'106503', u'106501', u'074304', u'074303', u'076606'], u'075731': [u'018101', u'074301', u'076601', u'076603', u'076606'], u'071121': [u'056801', u'017004', u'017005', u'098205', u'098201', u'098203'], u'071120': [u'070801', u'017003', u'017006', u'017004', u'017005', u'017002', u'098201', u'054801'], u'061225': [u'041104', u'041101', u'041102', u'041103', u'091703', u'091702', u'106301', u'106302'], u'520134': [u'090806', u'090804', u'090803', u'090802', u'090801', u'031902', u'066801', u'070301', u'124402', u'070304', u'070305'], u'061111': [u'100204', u'100202', u'100201', u'093402', u'093403', u'093401', u'093404', u'130905'], u'061110': [u'100203', u'100202', u'093402', u'093401', u'124205', u'124204', u'093404'], u'061030': [u'011501', u'090501', u'161901', u'011503', u'011502'], u'061118': [u'070602', u'106102', u'124203', u'106101', u'200901', u'023508', u'023505', u'023506', u'023507'], u'520801': [u'008507', u'008504', u'078401', u'108202', u'108201', u'078402', u'036003', u'036002', u'036001', u'078403', u'036004'], u'125519': [u'002902', u'057701', u'034101', u'057702', u'034105', u'066902', u'066905', u'066904'], u'145216': [u'108804', u'053404', u'032102', u'032103', u'053401', u'147801', u'132304', u'053402'], u'125416': [u'076006', u'076005', u'076003', u'021701', u'076001', u'021702', u'076002'], u'075615': [u'115904', u'115902', u'115903', u'115901', u'039004', u'022401', u'028901'], u'075614': [u'052302', u'115904', u'115902', u'115903', u'115901', u'039004', u'106601', u'039003'], u'075613': [u'052302', u'106601', u'039003', u'106603', u'006106', u'098101', u'115903'], u'075612': [u'052302', u'052303', u'052301', u'106601', u'011601', u'090602', u'006101', u'157003', u'006106'], u'075704': [u'058604', u'058606', u'058602', u'029406', u'029405', u'099601', u'085602'], u'530103': [u'090807', u'021302', u'021303', u'124402', u'039202', u'070302', u'070301', u'031902', u'070305'], u'530102': [u'021301', u'021302', u'090804', u'135401', u'094401', u'099202', u'070303', u'031902', u'031901', u'001903'], u'071214': [u'077402', u'049203', u'049202', u'049206', u'049204', u'069902'], u'071213': [u'207901', u'077401', u'049203', u'049202', u'054804', u'049206', u'054801', u'049204', u'049205', u'054802'], u'081127': [u'121001', u'121002', u'121004'], u'061114': [u'100204', u'100203', u'100202', u'100201', u'136801', u'130905'], u'061117': [u'070604', u'070602', u'124201', u'124203', u'106102', u'023506'], u'055635': [u'122701', u'122704', u'122705', u'005602', u'149803'], u'510832': [u'164201', u'099501', u'125604', u'085608', u'085603', u'085602', u'085601'], u'071235': [u'010007', u'046201', u'122801', u'090301', u'010002'], u'101634': [u'045401', u'045403', u'045402', u'077602', u'061903', u'031801', u'045404'], u'520135': [u'090804', u'090803', u'090801', u'031902', u'001904', u'001901', u'031901'], u'521115': [u'036902', u'036901', u'036906', u'036904', u'036903', u'076508', u'022001', u'091602', u'036905', u'091601', u'145001', u'091603', u'076511', u'076510', u'076507'], u'071130': [u'010904', u'152309', u'010912', u'017002', u'017003', u'010902', u'152301', u'152303', u'044003', u'024103', u'061808', u'061806', u'061805', u'061804', u'061803', u'061802'], u'071119': [u'152309', u'070801', u'017003', u'070803', u'070802', u'152303', u'054804', u'054801', u'152304', u'152307'], u'101633': [u'081701', u'077604', u'077602', u'061903', u'061901', u'000703', u'077603'], u'101632': [u'077604', u'077602', u'077601', u'000703', u'000702', u'000705', u'000704'], u'140414': [u'107603', u'082002', u'107601', u'107604', u'082001'], u'220933': [u'113404', u'113401', u'113403', u'113402', u'003503', u'003501', u'003506', u'125301'], u'061113': [u'136804', u'136801', u'136802', u'136803', u'130905', u'130903', u'130901'], u'521213': [u'128403', u'128402', u'111203', u'111202', u'111205', u'111206', u'061102'], u'040115': [u'017302', u'115005', u'115004', u'115002', u'147601'], u'061106': [u'070703', u'024103', u'024102', u'024105', u'024104', u'070701'], u'075729': [u'0', u'074304', u'036404', u'074302', u'074303', u'036401', u'074301'], u'061123': [u'136804', u'136805', u'136806', u'136801', u'136802', u'136803', u'214801'], u'061124': [u'136804', u'136802', u'136803', u'090502', u'090503', u'090504'], u'061218': [u'014102', u'014103', u'031303', u'014104', u'095302']}
'''


with open(r'E:\Data\yfan\sec_cir.json', 'r') as myfile:
    data=myfile.read()

sec_cir_merge = json.loads(data)

for k in sec_cir_check:
    if sec_cir_check[k]!=sec_cir_merge[k]:
        sec_cir_merge[k]=sec_cir_check[k]

k_within=[]       
for k in sec_cir_merge:
    if len(sec_cir_merge[k])==0:
        k_within.append(k)

cursor=arcpy.da.SearchCursor(r'Org Bounds\Circuit Boundaries',["FEEDERID","SHAPE@"])
circuit_shp=[]
circuit_fd=[]
for row in cursor:
    circuit_fd.append(row[0])
    circuit_shp.append(row[1])

k_shp=[]
for i in k_within:
    cursor=arcpy.da.SearchCursor('SectionName',["SHAPE@"],"SECTIONNAME={}".format(i))
    for row in cursor:
        k_shp.append(row[0])

sec_cir_contain={}
for i in range(len(k_within)):
    sec_cir_contain[k_within[i]]=[]
    for j in range(len(circuit_fd)):
        if circuit_shp[j].contains(k_shp[i]):
            sec_cir_contain[k_within[i]].append(circuit_fd[j])    

for k in sec_cir_contain:
    if sec_cir_contain[k]!=sec_cir_merge[k]:
        sec_cir_merge[k]=sec_cir_contain[k]

#manually check the section poly without any circuit

[k for k in sec_cir_merge if sec_cir_merge[k]==[]]
'''
[u'340828', u'145521', u'060528', u'261212', u'315807', u'280101', u'335802', u'315424', u'340222']
'''      

sec_cir_merge['340828']=[u'097801']
sec_cir_merge[u'145521']=[u'019102']
sec_cir_merge[u'060528']=[u'096301']
sec_cir_merge[u'261212']=[u'099301']
sec_cir_merge[u'315807']=[u'068902']
sec_cir_merge[u'280101']=[u'090901',u'090902']
sec_cir_merge[u'335802']=[u'207401']
sec_cir_merge[u'315424']=[u'204701']
sec_cir_merge[u'340222']=[u'069301']

#chek if all values are in list type

[k for k in sec_cir_merge if str(type(sec_cir_merge[k]))!="<type 'list'>"]

#save updated dictionary into json file

with open(r'E:\Data\yfan\sec_cir_update.json', 'w') as fp:
    json.dump(sec_cir_merge, fp)

import csv

with open(r'E:\Data\yfan\section_feeder.csv', 'wb') as file:
    writer = csv.writer(file,delimiter=",", quotechar="'", quoting=csv.QUOTE_ALL)
    writer.writerow(['Section_name', 'Feederid_1', 'Feederid_2', 'Feederid_3', 'Feederid_4', 'Feederid_5', 'Feederid_6', 'Feederid_7', 'Feederid_8', 'Feederid_9', 'Feederid_10', 'Feederid_11', 'Feederid_12', 'Feederid_13', 'Feederid_14', 'Feederid_15', 'Feederid_16', 'Feederid_17', 'Feederid_18', 'Feederid_19', 'Feederid_20', 'Feederid_21', 'Feederid_22', 'Feederid_23'])
    for k in sec_cir_merge:
        r0=[k]+sec_cir_merge[k]
        r1=[str(v) for v in r0]
        writer.writerow(r1)



    for k in sec_cir_merge:
        r0=[k]
        r1=r0+sec_cir_merge[k]
        writer.writerow(r1)

   
