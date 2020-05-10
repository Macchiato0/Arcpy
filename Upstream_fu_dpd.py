

# trace the upstream devices of a tie


# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------

# upstream_device.py

# Created on: 2020-05-05 14:29

# (Author by Yi Fan)

# Description: 

# trace the upstream devices of a tie from two directions

# input include: 

#     feederid

#     feature class to stop tracing

# ---------------------------------------------------------------------------



# Import arcpy module


# extract data from sde dbs. result data type is list
def extract_data(fid):
    where="FEEDERID = '{}'".format(fid)
    # edges
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.PriOHElectricLineSegment',["SHAPE@"],where)
    PriOH=[i[0] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.PriUGElectricLineSegment',["SHAPE@"],where)
    PriUG=[i[0] for i in cursor]
    # SUBTYPECD= 7, tlm connectors linked to isolators as a part of primary network
    Pri_lines=PriOH+PriUG
    lines=[[(i.firstPoint.X,i.firstPoint.Y),(i.lastPoint.X,i.lastPoint.Y)] for i in Pri_lines]
    #Points
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Fuse',["OID@","SHAPE@","LCP"],where)
    fuse=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y),i[2]] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.DynamicProtectiveDevice',["OID@","SHAPE@","LCP"],where)
    dpd=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y),i[2]] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.DynamicProtectiveDevice',["OID@","SHAPE@","LCP"],where+" and SUBSTATIONDEVICE='Y'")
    start_p=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y),i[2]] for i in cursor]
    cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.Switch',["OID@","SHAPE@","LCP","FEEDERID"],"TieSwitchIndicator = 'Y' and PHASEDESIGNATION= 7 and (FEEDERID2='{}' or FEEDERID='{}') and (FEEDERID2 is not null and FEEDERID is not null)".format(fid,fid))
    sw_t=[[i[0],(i[1].firstPoint.X,i[1].firstPoint.Y),i[2],i[3]] for i in cursor]
    return lines,fuse,dpd,sw_t,start_p
    
def get_pt(edges):
    import functools 
    lines=[]
    # reduce the (x,y) pairs  [[(x1,y1),(x2,y2)],[(x3,y3),(x4,y4)],...] into a list of [(x,y), tuples]
    p_s=list(set([functools.reduce(lambda x,y:x+y,edges)][0]))
    #print 'number of points: ',len(p_s)
    hash_pts=dict([[p_s[n],n] for n in range(len(p_s))])
    #print 'number of hash dict: ',len(hash_pts)
    pts_dict={}
    for k in hash_pts:
        pts_dict[hash_pts[k]]=k
    #print 'number of pts: ',len(pts_dict)
    for i in edges:
        pt1=hash_pts[i[0]]
        pt2=hash_pts[i[1]]   
        line=[pt1,pt2] 
        lines.append(line)
    #print 'number of lines: ',len(lines)
    return pts_dict,lines 

# reduce the close 2 points into one point if their x_distance or y_distance less than 0.1

def revise_connectivity(pt_list,pt_dict,line_pt):
    removed_pt=[]# store the pt needs to be removed
    replaced_pt=[]# store the pt needs to replace removed pt
    for i in range(1,len(pt_list)):
        if abs(pt_list[i][1][0]-pt_list[i-1][1][0])<0.1: #absolute x distance
            if abs(pt_list[i][1][1]-pt_list[i-1][1][1])<0.1: #absolute y distance
                removed_pt.append(pt_list[i][0])
                replaced_pt.append(pt_list[i-1][0])

    #remove the pt in pt_dictionary
    for i in range(len(removed_pt)):
        pt_dict.pop(removed_pt[i])
    #remove the pt in line_id,
    for i in line_pt:
        if i[0] in removed_pt:
            ind1=removed_pt.index(i[0])
            #print ind1,i
            i[0]=replaced_pt[ind1]
            #print i
        if i[1] in removed_pt:
            ind2=removed_pt.index(i[1])
            #print ind2
            i[1]=replaced_pt[ind2]    
            
def binarySearch (arr,l,r,x): 
    #r=0
    #l=len(arr)-1
    if r >= l: 
        mid = l + (r - l)//2  
        # If element is present at the middle itself 
        if abs(arr[mid][1][0] - x[0])<0.1 and abs(arr[mid][1][1] - x[1])<0.1: 
            return mid 
          
        # If element is smaller than mid, then it can only 
        # be present in left subarray 
        elif arr[mid][1][0] > x[0]: 
            
            return binarySearch(arr, l, mid-1, x) 
  
        # Else the element can only be present in right subarray 
        else: 
            return binarySearch(arr, mid+1, r, x) 
  
    else: 
        # Element is not present in the array or xy are very close:
        return -1


def convert_pt(devices,plist):
    pt_n={}
    for i in devices:
        n=binarySearch(plist,0,len(plist)-1,i[1])
        if n!=-1:
            #print n,i[0]
            pt_n[plist[n][0]]=i[:1]+i[2:]
        else:
            for t in plist:
                xy=t[1]
                x=i[1]
                #make sure the binary result -1 is not caused by tiny x_distance unmatch
                if abs(xy[0] - x[0])<0.1 and abs(xy[1] - x[1])<0.1:
                    ind=plist.index(t)
                    pt_n[plist[ind][0]]=i[:1]+i[2:]
                #else:
                    #return -1
    return pt_n


def get_dev_pt(pt_dict,f,d):
    result={}
    for k in pt_dict:
        result[k]=[]
    for k in f.keys():
        result[k]=['f']
    for k in d.keys():
        result[k]=['d']
    return result  


def create_graph(pts,edges):
    undirected_graph={}
    for v in pts:
        #print v
        undirected_graph[v[0]]=[]
    for i in edges:
        #print i
        if i[1] not in undirected_graph[i[0]]:
            undirected_graph[i[0]].append(i[1])
        if i[0] not in undirected_graph[i[1]]:
            undirected_graph[i[1]].append(i[0]) 
    return undirected_graph


def bfs(graph, initial):    
    import copy
    directed_g=copy.deepcopy(graph)
    reverse_g={initial:-1}
    queue = [initial] 
    visited=[0]*10000
    #print len(visited)
    while len(queue)>0:        
        node = queue.pop(0)
        visited[node]=1         
        neighbours = directed_g[node]           
        for neighbour in neighbours:
            reverse_g[neighbour]=node
            if visited[neighbour]!= 1:
                queue.append(neighbour)
                if node in directed_g[neighbour]:
                    directed_g[neighbour].remove(node)
    return directed_g,reverse_g
    
    
def upstream_trace_device(sw_one,rever_g,device_nodes):
    start=sw_one
    parent_node=start
    while parent_node in rever_g.keys():#node has no device
        if len(device_nodes[parent_node])!=0 and parent_node!=start:
            #print device_nodes[parent_node]
            return device_nodes[parent_node][0],parent_node       
        else:
            parent_node=rever_g[parent_node] 
    return -1,-1


def second_upstream_trace(sw_one,graph,device_nodes): #un_graph,pt_dev
    start=sw_one
    visit=[0]*10000
    q=[start]
    distance=[0]*10000
    dv_found=[]
    while len(q)>0:
        node=q.pop(0)
        if node!=start and device_nodes[node]!=[]:
            dv_found.append(node)
        visit[node]=1
        neighbor=graph[node]
        for u in neighbor:
            if visit[u]!=1:
                distance[u]=distance[node]+1
                q.append(u)
    if dv_found==[]:
        return -1,-1
    else:
        #print dv_found
        steps=min([distance[i] for i in dv_found])
        #print [distance[i] for i in dv_found]
        #print distance.count(steps)
        if distance.count(steps)>1:
            #print 'many'
            return -1,-1
        else:
            n_d=distance.index(steps)
            d_v=device_nodes[n_d][0]
            #print str(start)+" is on disconnected geo primary conductors"
            return d_v,n_d    
            
warning_al=[]
def find_up_device(s_t,rever_g,device_nodes,dv_dict,graph,fid):
    result={}
    for k in s_t:
        result[s_t[k][0]]=s_t[k][1:]+[0]*4    
    for k in s_t:
        dv,nd=upstream_trace_device(k,rever_g,device_nodes)
        if dv!=-1 and nd!=-1:       
            oid_lcp=dv_dict[dv][nd]
            l=[dv]+oid_lcp
            #print l,s_t[k]
            result[s_t[k][0]]=s_t[k][1:]+l+[fid]
        else:
            dv,nd=second_upstream_trace(k,graph,device_nodes)
            if dv!=-1 and nd!=-1:  
                oid_lcp=dv_dict[dv][nd]
                l=[dv]+oid_lcp
                global warning_al
                warning_al.append('warning: '+'sw '+str(s_t[k])+' & '+ dv+' '+str(oid_lcp)+" are on disconnected geo primary conductors!")
                result[s_t[k][0]]=s_t[k][1:]+l+[fid]
    return result            
           
    
    
                    
def main(fid):
    lines,fu,dp,sw_t,start=extract_data(fid) 
    if len(start)<1 or len(sw_t)<1:
        print "circuit '{}'".format(fid)+" num start pt = " + str(len(start))+" num tie switch = "+ str(len(sw_t))
        return 
    else:
        p_dict,line_id=get_pt(lines)
        pts_list=p_dict.items()
        pts_list.sort(key=lambda r:r[1][0])#sort    
        revise_connectivity(pts_list,p_dict,line_id) 
        pts_list=p_dict.items()
        pts_list.sort(key=lambda r:r[1][0])
        fu_pid=convert_pt(fu,pts_list)
        dp_pid=convert_pt(dp,pts_list)
        sw_t_pid=convert_pt(sw_t,pts_list)
        start_pt=convert_pt(start,pts_list)
        start_pt=start_pt.items()[0][0]
        pt_dev=get_dev_pt(p_dict,fu_pid,dp_pid)
        un_graph=create_graph(pts_list,line_id)
        d_gr,r_gr=bfs(un_graph,start_pt)
        dev_dict={'f':fu_pid,'d':dp_pid}
        result0=find_up_device(sw_t_pid,r_gr,pt_dev,dev_dict,un_graph,fid)
        print "'{}' is completed".format(fid)
        return result0

cursor=arcpy.da.SearchCursor(r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist_GO\ELECDIST.Boundary_Feeder_GO',["FEEDERID"])
fd_list=[str(i[0]) for i in cursor] #2312
fd_list=list(set(fd_list)) #2298

final_list=[]
final_result={}
for i in fd_list:
    result=main(i)
    if result!=None:
        for ky in result:
            if ky not in final_list:
                final_list.append(ky)
                final_result[ky]=list()
                final_result[ky].append(result[ky])   
            else:
                final_result[ky].append(result[ky])         
