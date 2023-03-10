from tree import Node

#expresion functions -----------------------------------------------------------------------
#every function here (except not and equal) are recursive, verify if children is a atom (stop condition, means is a leaf, function dict_handle is used to determine that) or if it another expressions.

def and_expression(world,ast):   
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
                

def not_expression(world,ast):  
    for item in world[0]:
        if item == ast.children[0].data:
            return False   
    return True

def equal_expression(world, ast):
    if(ast.children[0].data == ast.children[1].data):
        return True
    return False

def imply_expression(world,ast):
    if(dict_handle(ast.children[1].data)):
        if operators_functions[ast.children[1].data](world,ast.children[1]):
            return True    
    else:
        for item in world[0]:
            if item == ast.children[1].data:
                return True 

    #if the code gets here, means B is false

    if(dict_handle(ast.children[0].data)):
        if operators_functions[ast.children[0].data](world,ast.children[0]):
            return False    
    else:
        for item in world[0]:
            if item == ast.children[0].data:
                return False

    return True #This means that both A and B are false


def exists_expression(world,ast):
    values = world[1][ast.children[0].data[2]] #The values in the dictionary are obtained
    for value in values:
        if models(world,substitute(ast.children[1],ast.children[0].data[0],value)):
            return True
    return False

def forall_expression(world,ast):  
    values = world[1][ast.children[0].data[2]] #The values in the dictionary are obtained
    for value in values:
        if not models(world,substitute(ast.children[1],ast.children[0].data[0],value)):
            return False
    return True


#apply functions ------------------------------------------------------------------------------------------------
#These functions create a new Tree in base of the change the apply function wants to implement
#every function here (except not) are recursive, verify if children is a atom (stop condition, means is a leaf, function dict_handle is used to determine that) or if it another expressions.

def apply_and(world,new_world,effect):
    for child in effect.children:
        if(dict_handle(child.data)):
            apply_functions[child.data](world,new_world,child)
        else:
            new_world[0].append(child.data)

def apply_not(world,new_world,effect):
    new_world[0].remove(effect.children[0].data) if effect.children[0].data in new_world[0] else new_world[0]

def apply_when(world,new_world,effect):
    if(models(world,effect.children[0])):
        if(dict_handle(effect.children[1].data)):
            apply_functions[effect.children[1].data](world,new_world,effect.children[1])
        else:
            new_world[0].append(effect.children[1].data)

def apply_forall(world,new_world,effect):
    values = world[1][effect.children[0].data[2]]
    for value in values:
        temp_world = apply(new_world,substitute(effect.children[1],effect.children[0].data[0],value))
        for item in temp_world[0]:
            new_world[0].append(item) if item not in new_world[0] else new_world[0] #append the new items found in every sustitution 

    
#dictionaries --------------------------------------------------------------------------------------------------------- 

#these are used as a switch  

operators_dict = {"and": True , "or": True , "not" : True, "=" : True, "imply": True , "when" : True, "exists" : True , "forall" : True}

operators_functions = {"and": and_expression , "or": or_expression , "not" : not_expression, "=" : equal_expression, "imply": imply_expression, "exists" : exists_expression , "forall" : forall_expression}

apply_functions =  {"and": apply_and, "not" : apply_not, "when" : apply_when, "forall" : apply_forall}

#functions --------------------------------------------------------------------------------------------------------------

"""
This function receives a sequence (list or tuple) representing the abstract syntax tree of a logical expression and returns an expression object suitable for further processing. 
"""
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
            parent.add_new_child(Node(item))

"""
This function receives a list of atomic propositions, and a dictionary of sets and returns an object representing a logical world.
"""
def make_world(atoms, sets):
    atom_list = []

    for atom in atoms:
        atom_list.append(atom)
    
    return (atom_list,sets)
    
"""
This function takes a world and a logical expression, and determines if the expression holds in the given world, i.e. if the world models the condition.
"""
def models(world, condition):
    is_modeled = False
    if(dict_handle(condition.data)):
        is_modeled = operators_functions[condition.data](world,condition) #calls the respective expression functions using the dictionary 
    elif condition.data in world[0]:
        is_modeled = True
    return is_modeled    
    
"""
This function takes an expression, the name of a variable (usually starting with a question mark), and a constant value, and returns a *new* expression with all occurences of the variable 
replaced with the value
"""
def substitute(expression, variable, value):
    if(dict_handle(expression.data)):
        root = Node(expression.data)
        for child in expression.children:
            new_child = Node(child.data)
            root.add_new_child(recursive_sustitute(child, variable, value, new_child))
    else:
        new_expression = []
        if not expression.data[0] == "?": #condition to stop splitting the token when founds ? 
            for item in expression.data:
                if item == variable:
                    new_expression.append(value)
                else:
                    new_expression.append(item)
        else:
            if expression.data == variable:
                new_expression.append(value)
            else:
                new_expression.append(expression.data)
        new_expression = tuple(new_expression)
        root = Node(new_expression)
    return root

def recursive_sustitute(expression, variable, value, tree):
    if(dict_handle(expression.data)):
        for child in expression.children:
            new_child = Node(child.data)
            tree.add_new_child(recursive_sustitute(child, variable, value, new_child))
    else:
        new_expression = []
        if not expression.data[0] == "?": #condition to stop splitting the token when founds ? 
            for item in expression.data:
                if item == variable:
                    new_expression.append(value)
                else:
                    new_expression.append(item)
        else:
            if expression.data == variable:
                new_expression.append(value)
            else:
                new_expression.append(expression.data)
        new_expression = tuple(new_expression)
        return Node(new_expression)
    return tree

"""
This function takes a world, and an expression, and returns a new world, with the expression used to change the world. 
"""
def apply(world, effect):
    new_world = (world[0].copy(),world[1].copy()) #this is to avoid the member by member copy 

    if(dict_handle(effect.data)):
        apply_functions[effect.data](world,new_world,effect) ##calls the respective apply functions using the dictionary 
    elif effect.data not in new_world:
        new_world[0].append(effect.data)

    return new_world

"""
This functions receive an expressions and returns false if is an Atom and True otherwise
"""
def dict_handle(exp):
    try:
        return operators_dict[exp]
    except:
        return False

#Testing ------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    exp = make_expression(("or", ("on", "a", "b"), ("on", "a", "d")))
    world = make_world([("on", "a", "b"), ("on", "b", "c"), ("on", "c", "d")], {})
    
    print("Should be True: ", end="")
    print(models(world, exp))
    change = make_expression(["and", ("not", ("on", "a", "b")), ("on", "a", "c")])
    
    print("Should be False: ", end="")
    print(models(apply(world, change), exp))
    
    
    print("mickey/minny example")
    world = make_world([("at", "store", "mickey"), ("at", "airport", "minny")], {"Locations": ["home", "park", "store", "airport", "theater"], "": ["home", "park", "store", "airport", "theater", "mickey", "minny"]})
    exp = make_expression(("and", 
        ("not", ("at", "park", "mickey")), 
        ("or", 
              ("at", "home", "mickey"), 
              ("at", "store", "mickey"), 
              ("at", "theater", "mickey"), 
              ("at", "airport", "mickey")), 
        ("imply", 
                  ("friends", "mickey", "minny"), 
                  ("forall", 
                            ("?l", "-", "Locations"),
                            ("imply",
                                    ("at", "?l", "mickey"),
                                    ("at", "?l", "minny"))))))
                                    
    print("Should be True: ", end="")
    print(models(world, exp))
    become_friends = make_expression(("friends", "mickey", "minny"))
    friendsworld = apply(world, become_friends)
    print("Should be False: ", end="")
    print(models(friendsworld, exp))
    move_minny = make_expression(("and", ("at", "store", "minny"), ("not", ("at", "airport", "minny"))))
    
    movedworld = apply(friendsworld, move_minny)
    print("Should be True: ", end="")
    print(models(movedworld, exp))
    
    
    move_both_cond = make_expression(("and", 
                                           ("at", "home", "mickey"), 
                                           ("not", ("at", "store", "mickey")), 
                                           ("when", 
                                                 ("at", "store", "minny"), 
                                                 ("and", 
                                                      ("at", "home", "minny"), 
                                                      ("not", ("at", "store", "minny"))))))
                                                      
    
    print("Should be True: ", end="")
    print(models(apply(movedworld, move_both_cond), exp))
    
    print("Should be False: ", end="")
    print(models(apply(friendsworld, move_both_cond), exp))
    
    exp1 = make_expression(("forall", 
                            ("?l", "-", "Locations"),
                            ("forall",
                                  ("?l1", "-", "Locations"),
                                  ("imply", 
                                       ("and", ("at", "?l", "mickey"),
                                               ("at", "?l1", "minny")),
                                       ("=", "?l", "?l1")))))
                                       
    print("Should be True: ", end="")
    print(models(apply(movedworld, move_both_cond), exp1))
    
    print("Should be False: ", end="")
    print(models(apply(friendsworld, move_both_cond), exp1))