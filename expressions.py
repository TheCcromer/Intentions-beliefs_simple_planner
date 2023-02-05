from tree import Node

def and_expression(world,ast):   #posible agregarle un apply de parametro
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

def or_expression(world,ast):
    for child in ast.children:
        if(dict_handle(child.data)):
            if operators_functions[child.data](world,child):
                return True    
        else:
            for item in world[0]:
                if item == child.data:
                    return True    
    return False
                

def not_expression(world,ast):  #agregarle un apply de parametro
    for item in world[0]:
        if item == ast.children[0].data:
            return False   
    return True

def equal_expression(world, ast):
    if(ast.children[0].data == ast.children[1].data):
        return True
    return False

def imply_expression(world,ast):
    print(ast.children[0].data)
    print(ast.children[1].data)
    if(dict_handle(ast.children[1].data)):
        if operators_functions[ast.children[1].data](world,ast.children[1]):
            return True    
    else:
        for item in world[0]:
            if item == ast.children[1].data:
                return True 

    if(dict_handle(ast.children[0].data)):
        if operators_functions[ast.children[0].data](world,ast.children[0]):
            return False    
    else:
        for item in world[0]:
            if item == ast.children[0].data:
                return False

    return True #llegar aqui significa que ambos son falsos, por lo tanto en la expresion implica es verdadero


def when_expression(world,ast):
    if(models(world,ast.children[0].data)):
        return True
    return False

def exists_expression(ast):
    pass

def forall_expression(world,ast):  #se le deberia agregar un apply
    values = world[1][ast.children[0].data[2]]
    for value in values:
        if not models(world,substitute(ast.children[1],ast.children[0].data[0],value)):
            return False
    return True


def apply_and():
    pass

def apply_not():
    pass

def apply_when():
    pass

def apply_forall():
    pass

operators_dict = {"and": True , "or": True , "not" : True, "=" : True, "imply": True , "when" : True, "exists" : True , "forall" : True}

operators_functions = {"and": and_expression , "or": or_expression , "not" : not_expression, "=" : equal_expression, "imply": imply_expression , "when" : when_expression, "exists" : exists_expression , "forall" : forall_expression}

apply_functions =  {"and": apply_and, "not" : apply_not, "when" : apply_when, "forall" : apply_forall}

def make_expression(ast):
    if(dict_handle(ast[0])):
        root = Node(ast[0])
        make_expression_recursive(ast[1:],root)
        return root
    return Node(ast)
    
def make_expression_recursive(ast,parent):
    for item in ast:
        if(dict_handle(item[0])):  #stop condition: if is a operator it means that it has parameters. 
            child = parent.add_new_child(Node(item[0]))
            make_expression_recursive(item[1:],child)
        else: #In other case it means is a atom and it has to be a leaf
            #parent.add_new_child(Node(read_atom(item)))
            parent.add_new_child(Node(item))

"""
This function receives a list of atomic propositions, and a dictionary of sets and returns an object representing a logical world.
"""
def make_world(atoms, sets):
    atom_list = []

    for atom in atoms:
        atom_list.append(atom)
    
    return (atom_list,sets)
    

def models(world, condition):
    is_modeled = False
    if(dict_handle(condition.data)):
        is_modeled = operators_functions[condition.data](world,condition)
    return is_modeled    
    
def substitute(expression, variable, value):
    if(dict_handle(expression.data)):
        root = Node(expression.data)
        for child in expression.children:
            new_child = Node(child.data)
            new_child = root.add_new_child(recursive_sustitute(child, variable, value, new_child))
    else:
        new_expression = []
        for item in expression.data:
            if item == variable:
                new_expression.append(value)
            else:
                new_expression.append(item)
        new_expression = tuple(new_expression)
        root = Node(new_expression)
    return root

def recursive_sustitute(expression, variable, value, tree):
    if(dict_handle(expression.data)):
        for child in expression.children:
            new_child = Node(child.data)
            new_child = tree.add_new_child(recursive_sustitute(child, variable, value, new_child))
    else:
        new_expression = []
        for item in expression.data:
            if item == variable:
                new_expression.append(value)
            else:
                new_expression.append(item)
        new_expression = tuple(new_expression)
    return Node(new_expression)

    
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
    
   