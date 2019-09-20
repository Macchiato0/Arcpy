import sys
sys.getrecursionlimit()
sys.setrecursionlimit(100000)

fid='011003'
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecOHElectricLineSegment',["OID@","SHAPE@"],"feederid='{}'".format(fid))

line_shp=[[i[0],[(int(i[1].firstPoint.X),int(i[1].firstPoint.Y)),(int(i[1].lastPoint.X),int(i[1].lastPoint.Y))]] for i in cursor]

line_all=[]
for i in line_shp:
    line_all.append([i,0])
#0 is oh
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecUGElectricLineSegment',["OID@","SHAPE@"],"feederid='{}'".format(fid))

line_shp_1=[[i[0],[(int(i[1].firstPoint.X),int(i[1].firstPoint.Y)),(int(i[1].lastPoint.X),int(i[1].lastPoint.Y))]] for i in cursor]

#1 is underground 
for i in line_shp_1:
    line_all.append([i,1])


cluster=[]        
#cluster1=[line_shp[0]]
cluster1=[line_all[0]]
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

find_line(cluster1)




#form oh sec network clusters  (recursive method)

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

find_line(cluster1)


#find the tlm for each cluster
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.Transformer',["SHAPE@","TLM"],"feederid='{}'".format(fid))
tlm_shp=[[i[1],(int(i[0].firstPoint.X),int(i[0].firstPoint.Y))] for i in cursor]
cluster_tlm=[]
def line_oh_tlm(oh_clust,tlm):#oh_clust is the element of cluster, tlm is the element of tlm_shp
    n=0
    for i in oh_clust:
        if [l for l in i[1] if l==tlm[1]]:
            n=n+1
    if n>0:
        row=[oh_clust,tlm]
        cluster_tlm.append(row)
        
for i in cluster:
    for j in tlm_shp:
        line_oh_tlm(i,j)


























#form sec underground to sec overhead network clusters,same algorithem as above 
#the following is the algorithm for underground
fid='011003'
cursor=arcpy.da.SearchCursor('E:\\Data\\yfan\\Connection to dgsep011.sde\\ELECDIST.ElectricDist\\ELECDIST.SecUGElectricLineSegment',["OID@","SHAPE@"],"feederid='{}'".format(fid))

line_shp=[[i[0],[(int(i[1].firstPoint.X),int(i[1].firstPoint.Y)),(int(i[1].lastPoint.X),int(i[1].lastPoint.Y))]] for i in cursor]

un_cluster=[]        
un_cluster1=[line_shp[0]]
un_cluster2=[]
un_cluster3=[]
    
def find_line(lists):#lists=un_cluster1
    global un_cluster
    global un_cluster2
    global un_cluster1
    global un_cluster3
    global line_shp
    for l in lists:
        if l in line_shp:
            line_shp.remove(l)
    for i in line_shp:
        for j in lists:
            if [a for a in i[1] if a in j[1]]:  
                if i not in lists:
                    un_cluster2.append(i)
    if len(un_cluster2)>0:
        un_cluster3=[]
        for h in un_cluster2:
            un_cluster1.append(h)
            un_cluster3.append(h)
        un_cluster2=[]
        #print cluster1
        find_line(un_cluster3)
    elif len(line_shp)>0:
        un_cluster.append(un_cluster1)
        un_cluster3=[]
        un_cluster1=[line_shp[0]]
        find_line(un_cluster1)
    else:
        un_cluster.append(un_cluster1)
        return len(un_cluster)
find_line(un_cluster1)
        
        
#add under sec network cluster to overhead network cluster        
def link_cluster(oh_cluster,un_l):#oh_cluster is the oh sub cluster,un_l is a single under sec line
    n=0
    for oh in oh_cluster: 
        if [l for l in oh_l[1] if l in un_l[1]]:#if two line share same point
            n=n+1
    if n>0:
        return True
    else:
        return False
                

            
  
    
        
        
        
        

   
