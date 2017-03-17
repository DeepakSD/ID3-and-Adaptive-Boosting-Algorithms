'''
Created on Sep 26, 2016

@author: deepaks
'''
import csv
import math
cv=[]
fvlist=[]
fvlength=0
train="/Users/deepaks/Documents/workspace/AML/Assignment2/mush_train.data"
attribute_file="/Users/deepaks/Documents/workspace/AML/Assignment2/attribute_mapping.txt"
test="/Users/deepaks/Documents/workspace/AML/Assignment2/mush_test.data"

def read(train):
    with open(train) as inp:
        lines=csv.reader(inp)
        for line in lines:
            fvmap=dict()
            for i in range(0,len(line)):
                key='a'+str(i)
                fvmap[key]=line[i]
            fvlist.append(fvmap)
            
def decision_tree():
    bestatt,att_map=best_att(fvlist,{})
    bestatt_name='a'+str(bestatt)
    root=Node(bestatt_name,att_map,[bestatt_name],len(fvlist[0]))
    build_tree([root])
    return root

class Node(object):
    def __init__(self,att_name,att_map,usedatt,total_att):
        self.att_name=att_name
        self.att_map=att_map
        self.usedatt=usedatt
        self.usedatt_map=dict()
        self.total_att=total_att
        self.class_name=dict()
        self.children=dict()
    def get_usedatt_map(self):
        return self.usedatt_map
    def get_usedatt(self):
        return self.usedatt
    def set_class_value(self,att_name,class_name):
        self.class_name[att_name]=class_name
    def append_child(self,att_name,obj):
        self.children[att_name]=obj
    def set_att_map(self,usedatt_map):
        self.usedatt_map=usedatt_map

def build_tree(nodelist):
    if not nodelist:
        return
    treelist=[]
    for node in nodelist:
        for att_name,att_value_map in node.att_map.items():
            total_entropy=compute_total_entropy(att_value_map.map)
            if (len(node.usedatt)-(node.total_att-1))==0 or (total_entropy==0):
                for m,n in att_value_map.map.items():
                    class_name=m
                    class_count=n
                node.set_class_value(att_name,class_name)
                continue
            else:
                usedatt_map=node.get_usedatt_map()
                usedatt_map[node.att_name]=att_name
                new_fvlist=[]
                for fvmap in fvlist:
                    match=set(fvmap.items())&set(node.usedatt_map.items())
                    if match==set(node.usedatt_map.items()):
                        new_fvlist.append(fvmap)
                if not new_fvlist:
                    return
                bestatt,att_cmap=best_att(new_fvlist,node.usedatt)
                child=build_node(node,bestatt,att_cmap)
                node.append_child(att_name,child)
                treelist.append(child)
    build_tree(treelist)
                
                
def best_att(fvlist,used_att):
    alist=[{} for _ in range(len(fvlist[0])-1)]
    for fvmap in fvlist:
        for i in range(1,len(fvmap)):
            att='a'+str(i)
            if att in used_att:
                continue;
            else:
                count=1
                att_name=fvmap[att]
                class_name=fvmap['a0']
                if att_name in alist[i-1]:
                    att_map=alist[i-1][att_name]
                    if class_name in att_map.map:
                        count=att_map.map[class_name]+1
                    att_map.map[class_name]=count
                    att_map.tcount=att_map.tcount+1   
                else:
                    map=dict()
                    map[class_name]=count
                    att_map=avalues(map,1)
                    alist[i-1][att_name]=att_map
    k=1
    max_ig=-1
    ig=0
    class_map=get_class_map(fvlist)
    total_entropy=compute_total_entropy(class_map)
    for att in alist:
        name='a'+str(k)
        if not att.items():
            k=k+1
            continue
        else:
            ig=total_entropy-compute_att_entropy(att)
            if max_ig<ig:
                max_ig=ig
                bestatt=k 
            k=k+1
    return bestatt,alist[bestatt-1]

def build_node(parent,bestatt,att_map):
    bestatt_name='a'+str(bestatt)
    usedatt=parent.get_usedatt()
    usedatt.append(bestatt_name)
    usedatt_map=parent.get_usedatt_map()
    child=Node(bestatt_name,att_map,usedatt,len(fvlist[0]))
    child.set_att_map(usedatt_map)
    return child

class avalues(object):
    map=dict()
    tcount=0
    def __init__(self,map,tcount):
        self.map=map
        self.tcount=tcount

def get_class_map(fvlist):
    tempdict=dict()
    for fvmap in fvlist:
        temp=fvmap['a0']
        c=1
        if temp in tempdict:
            c=tempdict[temp]+1
        tempdict[temp]=c
    return tempdict
    
def compute_total_entropy(tempdict):
    total_class=0
    total_entropy=0
    for m,n in tempdict.items():
        total_class=total_class+n
    for m,n in tempdict.items():
        total_entropy=total_entropy+compute_entropy(n,total_class)
    return total_entropy

def compute_entropy(n,tot):
    prob=n/tot
    entropy=-(prob*math.log(prob,2))
    return entropy

def compute_att_entropy(att_map):
    ss=0
    att_ent=0
    for att_name,att_map_value in att_map.items():
        ss=ss+att_map_value.tcount
    for att_name,att_map_value in att_map.items():
        att_value_map=att_map_value.map
        tcount=att_map_value.tcount
        ent=0
        for class_name,count in att_value_map.items():
            ent=ent+compute_entropy(count,tcount)
        att_ent=att_ent+(tcount/ss)*ent
    return att_ent

def att_mapping(attribute_file):
    file=open(attribute_file)
    att_info=dict()
    i=1
    for line in file:
        att=line.split(': ')
        att_name=att[0].split('. ')[1]
        tmap={n.rstrip():m for m,n in (x.split('=') for x in att[1].split(','))}
        att_obj=Att_name_map(att_name,tmap)
        att_info['a'+str(i)]=att_obj
        i=i+1
    return att_info
                
class Att_name_map(object):
    map=dict()
    name=''
    def __init__(self,name,map):
        self.name=name
        self.map=map
        
def show_tree(root,att_info,space):
    attr=att_info[root.att_name]
    print('*'+attr.name)
    x=len(attr.name)+space
    if root.class_name:
        for m,n in root.class_name.items():
            for i in range(1,x):
                print(' ',end="")
            print(' '+attr.map[m]+' -- '+n,)
    if root.children:
        for m,n in root.children.items():
            for i in range(1,x):
                print(' ',end="")
            print(' '+attr.map[m]+'  ',end="" )
            space=space+len(attr.name)+len(attr.map[m])+5
            show_tree(n,att_info,space)
            
def accuracy(root,dataset):
    par_fvlist=[]
    with open(dataset) as inp:
        lines=csv.reader(inp)
        for line in lines:
            par_fvmap=dict()
            for i in range(0,len(line)):
                key='a'+str(i)
                par_fvmap[key]=line[i]
            par_fvlist.append(par_fvmap)
    i=1
    match=0
    for par_fvmap in par_fvlist:
        superior=root
        temp=par_fvmap[root.att_name]
        while True:
            if temp in superior.att_map:
                if temp in superior.class_name:
                    out_temp=superior.class_name[temp]
                    break
                else:
                    superior=superior.children[temp]
                    temp=par_fvmap[superior.att_name]
            else:
                new_class_map=dict()
                for att_name,att_map in superior.att_map.items():
                    for class_name,class_count in att_map.map.items():
                        if class_name in new_class_map:
                            new_class_map[class_name]=class_count+new_class_map[class_name]
                        else:
                            new_class_map[class_name]=class_count
                count=0
                out_temp=0
                for m,n in new_class_map.items():
                    if n>count:
                        out_temp=m
                        count=n
                break
        if (out_temp==par_fvmap['a0']):
            match=match+1
        i=i+1
    acc=match/len(par_fvlist)
    print(acc*100)
                           
read(train)
root=decision_tree()
att_info=att_mapping(attribute_file)
show_tree(root,att_info,1)  
print("Accuracy on mush_train.data: ")
accuracy(root,train)
print("Accuracy on mush_test.data: ")
accuracy(root,test)
    