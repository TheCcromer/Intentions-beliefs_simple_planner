class Node:
    def __init__(self,data):
        self.data = data
        self.children = []

    def add_new_child(self,node):
        self.children.append(node)
        return node

    def atom_searching(self):
        atom_list = []
        atom_list.append(self.recursive_atom_searching(atom_list))
        #self.sort_atom_list(atom_list)
        return atom_list
    
    def recursive_atom_searching(self,atom_list):
        if(len(self.children) > 0): #the node is not a leaf
            for child in self.children:
                atom_list.append(child.recursive_atom_searching(atom_list))    
        return self.data

    def sort_atom_list(self,atom_list):
        pass

        

