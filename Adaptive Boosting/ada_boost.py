'''
@author: deepaks
'''
import sys
import csv
import numpy as np

fvlist=list()
fvlist1=list()
fnlist=list()
hspace=list()
m=10
chosen_classifier=list()

class Node:
    def __init__(self, fname=None, flist=None):
        if fname is None:
            self.fname=''
        else:
            self.fname=fname
        if flist is None:
            self.flist=[]
        else:
            self.flist=flist
        self.children=[]

    def get_fname(self):
        return self.fname
    
    def get_flist(self):
        return self.flist
    

class Tree:
    def __init__(self,root,left_child,right_child):
        self.root=root
        self.left_child=left_child
        self.right_child=right_child
    
    def get_root(self):
        return self.root
    
    def get_left_child(self):
        return self.left_child

    def get_right_child(self):
        return self.right_child
    
def read_train(input_data):
    with open(input_data) as inp:
        reader=csv.reader(inp)
        for row in reader:
            temp = (row[1:],row[0])
            fvlist.append(temp)
        for x in range(1,len(fvlist[0][0])+1):
            name='F'+str(x)
            fnlist.append(name)
    return
def read_test(input_data):
    with open(input_data) as inp:
        reader=csv.reader(inp)
        for row in reader:
            temp = (row[1:],row[0])
            fvlist1.append(temp)
    return

def hypothesis_space():
    for i in range(0,len(fnlist)):
        root=Node(fnlist[i])
        for j in range(0,len(fnlist)):
            if(j==i):
                continue
            else:
                left_child=fnlist[j]
                left=[]
                for x in range(2):
                    for y in range(2):
                        left.append(Node(left_child,[str(x),str(y)]))
            for k in range(0,len(fnlist)):
                if k==i:
                    continue
                else:
                    right_child=fnlist[k]
                    right=[]
                    for x in range(2):
                        for y in range(2):
                            right.append(Node(right_child,[str(x),str(y)]))
                    for a in left:
                        for b in right:
                            tree=Tree(root,a,b)
                            hspace.append(tree)
    print(len(hspace))
    return  
                            
def adaboost():
    weight=[float(1.0/len(fvlist))]*len(fvlist)
    #print(weight)
    for i in range(int(m)):
        err_list=[]
        cnt=0
        for j in hspace:
            cnt=cnt+1
            if cnt>20:
                break
            wt=0
            for line in range(len(fvlist)):
                if parse(fvlist[line],j)==0:
                    wt+=weight[line]
            err_list.append(wt)
        min_err=min(err_list)
        chosen_hindex=err_list.index(min_err)
        tree=hspace[chosen_hindex]
        print('Root: ',tree.get_root().get_fname())
        print('Left_child(0): ',tree.get_left_child().get_fname())
        print('Class_Label: ',tree.get_left_child().get_flist())
        print('Right_child(1): ',tree.get_right_child().get_fname())
        print('Class_Label: ',tree.get_right_child().get_flist())
        print('Hypothesis Error',min_err) 
        alpha=(1/2)*(np.log((1-min_err)/min_err))
        chosen_classifier.append((tree,alpha))
        print('Hypothesis Weight',alpha)
        d=2*np.sqrt(min_err*(1-min_err))
        for line in range(len(fvlist)):
            c=parse(fvlist[line],tree)
            if c==1:
                t=-1
            else:
                t=1
            weight[line]=(weight[line]*np.exp(t*alpha))/d  
            
def parse(data,tree):  
        root=tree.get_root()
        root_value=data[0][fnlist.index(root.get_fname())]
        if int(root_value)==0:
            child=tree.get_left_child()
        else:
            child=tree.get_right_child()
        cvalue=data[0][fnlist.index(child.get_fname())]
        flist=child.get_flist()
        if int(cvalue)==0:
            if int(flist[0])!=int(data[1]):
                return 0
        else:
            if int(flist[1])!=int(data[1]):
                return 0
        return 1
    
def accuracy():
    correct=0
    for i in range(len(fvlist)):
        total=0
        for h in chosen_classifier:
            total+=accuracy_parse(fvlist[i],h[0])*h[1]
        if(total>0 and int(fvlist[i][1])==1)or(total<=0 and int(fvlist[i][1])==0):
            correct+=1
    print('Accuracy of AdaBoost Algorithm on Train Data',(correct/len(fvlist)))
    
    correct=0
    for i in range(len(fvlist1)):
        total=0
        for h in chosen_classifier:
            total+=accuracy_parse(fvlist1[i],h[0])*h[1]
        if(total>0 and int(fvlist1[i][1])==1)or(total<=0 and int(fvlist1[i][1])==0):
            correct+=1
    print('Accuracy of AdaBoost Algorithm on Test Data',(correct/len(fvlist1)))
    
def accuracy_parse(data,tree):  
        root=tree.get_root()
        root_value=data[0][fnlist.index(root.get_fname())]
        if int(root_value)==0:
            child=tree.get_left_child()
        else:
            child=tree.get_right_child()
        cvalue=data[0][fnlist.index(child.get_fname())]
        flist=child.get_flist()
        if int(cvalue)==0:
            if int(flist[0])==0:
                return -1
            else:
                return 1
        else:
            if int(flist[1])==0:
                return -1
            else:
                return 1

def main(args):
    train_data="/heart_train.data"
    test_data="/heart_test.data"
    read_train(train_data)
    hypothesis_space()
    adaboost()
    read_test(test_data)
    accuracy()
    
main(sys.argv)
