from tree import Node

def and_expresion(world,ast):
    for child in ast.children:
        were_equal = False
        if(dict_handle(child.data)):
            if not operators_functions[child.data](world,child):
                return False
        else:
            for item in world[0]:
                if item == child.data:
                    were_equal = True
                    break
            if not were_equal:
                return False
    return True

def or_expresion(world,ast):
    for child in ast.children:
        if(dict_handle(child.data)):
            if operators_functions[child.data](world,child):
                return True    
        else:
            for item in world[0]:
                if item == child.data:
                    return True    
    return False             

def not_expresion(ast):
    pass

def equal_expresion(ast):
    pass

def imply_expresion(ast):
    pass

def when_expresion(ast):
    pass

def exists_expresion(ast):
    pass

def forall_expresion(ast):
    pass


operators_dict = {"and": True , "or": True , "not" : True, "=" : True, "imply": True , "when" : True, "exists" : True , "forall" : True}

operators_functions = {"and": and_expresion , "or": or_expresion , "not" : not_expresion, "=" : equal_expresion, "imply": imply_expresion , "when" : when_expresion, "exists" : exists_expresion , "forall" : forall_expresion}



def make_expression(ast):
    root = Node(ast[0])
    if(dict_handle(ast[0])):
        make_expression_recursive(ast[1:],root)
    return root
    
def make_expression_recursive(ast,parent):
    for item in ast:
        if(dict_handle(item[0])):  #stop condition: if is a operator it means that it has parameters. 
            child = parent.add_new_child(Node(item[0]))
            make_expression_recursive(item[1:],child)
        else: #In other case it means is a atom and it has to be a leaf
            parent.add_new_child(Node(read_atom(item)))

"""
This function receives a list of atomic propositions, and a dictionary of sets and returns an object representing a logical world.
"""
def make_world(atoms, sets):
    atom_list = []

    for atom in atoms:
        atom_list.append(read_atom(atom))
    
    return (atom_list,sets)
    

def models(world, condition):
    is_modeled = False
    if(dict_handle(condition.data)):
        is_modeled = operators_functions[condition.data](world,condition)
    return is_modeled   
    
def substitute(expression, variable, value):

    return expression
    
def apply(world, effect):
    
    return world


"""
This functions reads an atom in a tuple form ("on","a","b") and convert it to "on(a,b)"
"""
def read_atom(atom):
    conv_atom = atom[0] + "("
    for i in range(1,len(atom)):
        conv_atom += atom[i]
        if(i < len(atom) - 1):
            conv_atom += ","
    conv_atom += ")"
    return conv_atom


def dict_handle(exp):
    try:
        return operators_dict[exp]
    except:
        return False


if __name__ == "__main__":
    exp = make_expression(("or", ("on", "a", "b"), ("on", "a", "d")))
    world = make_world([("on", "a", "b"), ("on", "b", "c"), ("on", "c", "d")], {})
    
   