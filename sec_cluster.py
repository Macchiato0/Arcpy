import sys
sys.getrecursionlimit()
sys.setrecursionlimit(100000)

fid='011003'
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment',["OID@","SHAPE@"],"feederid='{}'".format(fid))

line_shp=[[i[0],[(int(i[1].firstPoint.X),int(i[1].firstPoint.Y)),(int(i[1].lastPoint.X),int(i[1].lastPoint.Y))]] for i in cursor]

cluster=[]        
cluster1=[line_shp[0]]
cluster2=[]
cluster3=[]

  

def find_line(lists):#lists=cluster1
    global cluster
    global cluster2
    global cluster1
    global cluster3
    global line_shp
    for l in lists:
        if l in line_shp:
            line_shp.remove(l)
    for i in line_shp:
        for j in lists:
            if [a for a in i[1] if a in j[1]]:  
                if i not in lists:
                    cluster2.append(i)
    if len(cluster2)>0:
        cluster3=[]
        for h in cluster2:
            cluster1.append(h)
            cluster3.append(h)
        cluster2=[]
        #print cluster1
        find_line(cluster3)
    elif len(line_shp)>0:
        cluster.append(cluster1)
        cluster3=[]
        cluster1=[line_shp[0]]
        find_line(cluster1)
    else:
        cluster.append(cluster1)
        return len(cluster)





fid='011003'
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment',["OID@","SHAPE@"],"feederid='{}'".format(fid))

line_shp=[[i[0],[(int(i[1].firstPoint.X),int(i[1].firstPoint.Y)),(int(i[1].lastPoint.X),int(i[1].lastPoint.Y))]] for i in cursor]

cluster=[]        
cluster1=[line_shp[0]]
cluster2=[]
cluster3=[]

def find_line(lists):#lists=cluster1
    #global cluster
    global cluster2
    global cluster1
    global cluster3
    global line_shp
    for l in lists:
        if l in line_shp:
            line_shp.remove(l)
    for i in line_shp:
        for j in lists:
            if [a for a in i[1] if a in j[1]]:  
                if i not in lists:
                    cluster2.append(i)
    if len(cluster2)>0:
        cluster3=[]
        for h in cluster2:
            cluster1.append(h)
            cluster3.append(h)
        cluster2=[]
        #print cluster1
        find_line(cluster3)
    elif lenfid='011003'
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment',["OID@","SHAPE@"],"feederid='{}'".format(fid))

line_shp=[[i[0],[(int(i[1].firstPoint.X),int(i[1].firstPoint.Y)),(int(i[1].lastPoint.X),int(i[1].lastPoint.Y))]] for i in cursor]

cluster=[]        
cluster1=[line_shp[0]]
cluster2=[]
cluster3=[]

def find_line(lists):#lists=cluster1
    #global cluster
    global cluster2
    global cluster1
    global cluster3
    global line_shp
    for l in lists:
        if l in line_shp:
            line_shp.remove(l)
    for i in line_shp:
        for j in lists:
            if [a for a in i[1] if a in j[1]]:  
                if i not in lists:
                    cluster2.append(i)
    if len(cluster2)>0:
        cluster3=[]
        for h in cluster2:
            cluster1.append(h)
            cluster3.append(h)
        cluster2=[]
        #print cluster1
        find_line(cluster3)
    elif len(line_shp)>0:
        cluster.append(cluster1)
        cluster3=[]
        cluster1=[line_shp[0]]
        find_line(cluster1)
    else:
        cluster.append(cluster1)
        return len(cluster)






def find_line(lists):#lists=cluster1
    #global cluster
    global cluster2
    global cluster1
    global cluster3
    global line_shp
    for l in lists:
        if l in line_shp:
            line_shp.remove(l)
    for i in line_shp:
        for j in lists:
            if [a for a in i[1] if a in j[1]]:  
                if i not in lists:
                    cluster2.append(i)
    if len(cluster2)>0:
        cluster3=[]
        for h in cluster2:
            cluster1.append(h)
            cluster3.append(h)
        cluster2=[]
        #print cluster1
        find_line(cluster3)
    elif lenfid='011003'
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment',["OID@","SHAPE@"],"feederid='{}'".format(fid))

line_shp=[[i[0],[(int(i[1].firstPoint.X),int(i[1].firstPoint.Y)),(int(i[1].lastPoint.X),int(i[1].lastPoint.Y))]] for i in cursor]

cluster=[]        
cluster1=[line_shp[0]]
cluster2=[]
cluster3=[]

def find_line(lists):#lists=cluster1
    #global cluster
    global cluster2
    global cluster1
    global cluster3
    global line_shp
    for l in lists:
        if l in line_shp:
            line_shp.remove(l)
    for i in line_shp:
        for j in lists:
            if [a for a in i[1] if a in j[1]]:  
                if i not in lists:
                    cluster2.append(i)
    if len(cluster2)>0:
        cluster3=[]
        for h in cluster2:
            cluster1.append(h)
            cluster3.append(h)
        cluster2=[]
        #print cluster1
        find_line(cluster3)
    elif len(line_shp)>0:
        cluster.append(cluster1)
        cluster3=[]
        cluster1=[line_shp[0]]
        find_line(cluster1)
    else:
        cluster.append(cluster1)
        return len(cluster)
        
        
        
        
        
        
        
        
def find_line(lists):#lists=line_shp[0]
    global cluster(line_shp)>0:
        cluster.append(cluster1)
        cluster3=[]
        cluster1=[line_shp[0]]
        find_line(cluster1)
    else:
        cluster.append(cluster1)
        return len(cluster)
        
        
        
        
        
        
        
        
def find_line(lists):#lists=line_shp[0]
    global cluster
    global cluster2
    global cluster1
    global cluster3
    for i in [x for x in line_shp if x not in set(lists)|set(cluster3)]:
        for j in lists:
            if [a for a in i[1] if a in j[1]]:  
                cluster2.append(j)
                cluster3.append(j)
    if len(cluster2)>1:
        for h in cluster2:
            cluster1.append(h)
        cluster2=[]
        print cluster1
        find_line(cluster1)
    else len(cluster2)==0:
        cluster.appen(cluster2)

find_line(line_shp[0])

cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.Transformer',["OID@","SHAPE@","TLM"],"feederid='{}'".format(fid))
tlm_shp={k:(v1,v2) for (k,v1,v2) in cursor}
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.ServicePoint',["OID@","SHAPE@","DEVICELOCATION"],"feederid='{}'".format(fid))
sp_shp={k:(v1,v2) for (k,v1,v2) in cursor}

# recursive method:
# search lines linked to [line1] 

def find_line(): #find the linked lines, lines=a.sub_cluster1
    global line_shp
    lines=copy.deepcopy(line_shp)
    global cluster
    global cluster1
    global cluster2
    line_cont={}
    for k1 in lines:
        for k2 in cluster1:
            if cluster1[k2].distanceTo(lines[k1])==0:
                #print k2,k1
                line_cont[k1]=line_shp.pop(k1)   
                print k1
    if len(line_cont)>0:
        #print line_cont
        cluster2.update(line_cont)
        cluster1={}
        cluster1.update(line_cont)
        find_line()
    elif len(line_cont)==0 and len(line_shp)>0:
        cluster.append(cluster2)
        cluster1=dict([line_shp.popitem()])
        #print cluster1
        cluster2={}
        cluster2.update(cluster1)
        find_line()
    else:
        return cluster
