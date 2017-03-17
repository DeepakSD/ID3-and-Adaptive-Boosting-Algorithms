class Node:
    def __init__(self, name=None, class_list=None):
        if name is None:
            self.name=''
        else:
            self.name=name
        if class_list is None:
            self.class_list=[]
        else:
            self.class_list=class_list
        self.children=[]

    def get_name(self):
        return self.name
    
    def get_class_list(self):
        return self.class_list

    def get_is_label(self):
        return self.is_label
    
    def get_children(self):
        return self.children

class Tree:
    def __init__(self,parent,left,right):
        self.parent=parent
        self.left=left
        self.right=right
    
    def get_parent(self):
        return self.parent
    
    def get_left(self):
        return self.left

    def get_right(self):
        return self.right