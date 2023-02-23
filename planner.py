import time
from pddl import *
import graph
from expressions import *
import pathfinding
import sys 

def list_combination(list1,list2):
    tmp_list = []
    for x in range(0, len(list1)):
        for y in range(0, len(list2)):
            if type(list1[x]) == list:
                tmp = list1[x].copy()
                tmp.append(list2[y])
                tmp_list.append(tmp)
            else:
                tmp_list.append([list1[x],list2[y]])
    return tmp_list

def ground_parameter(object_dict,parameter_list):
    result_list = object_dict[parameter_list[0]]
    for i in range(1, len(parameter_list)):
        result_list = list_combination(result_list,object_dict[parameter_list[i]])
    return result_list

def parse_parameter(file_parsed):
    parameter_list = {}
    for action in file_parsed[":action"]:
        file_parsed[":action"][action][":parameters"] = parse_dash_list(file_parsed[":action"][action][":parameters"])
        parameter_list[action] = []
        for parameter in file_parsed[":action"][action][":parameters"]:
            for i in range(0,len(parameter[0])):
                parameter_list[action].append(parameter[1])
    return parameter_list

def parse_objects(file_parsed):
    object_list = {}
    object_list[""] = []
    for object in file_parsed[":objects"]:
        object_list[object[1]] = object[0]
        for item in object[0]:
            object_list[""].append(item)
    return object_list

def plan(domain, problem, useheuristic=True):
    """
    Find a solution to a planning problem in the given domain 
    
    The parameters domain and problem are exactly what is returned from pddl.parse_domain and pddl.parse_problem. If useheuristic is true,
    a planning heuristic (developed in task 4) should be used, otherwise use pathfinding.default_heuristic. This allows you to compare 
    the effect of your heuristic vs. the default one easily.
    
    The return value of this function should be a 4-tuple, with the exact same elements as returned by pathfinding.astar:
       - A plan, which is a sequence of graph.Edge objects that have to be traversed to reach a goal state from the start. Each Edge object represents an action, 
         and the edge's name should be the name of the action, consisting of the name of the operator the action was derived from, followed by the parenthesized 
         and comma-separated parameter values e.g. "move(agent-1,sq-1-1,sq-2-1)"
       - distance is the number of actions in the plan (i.e. each action has cost 1)
       - visited is the total number of nodes that were added to the frontier during the execution of the algorithm 
       - expanded is the total number of nodes that were expanded (i.e. whose neighbors were added to the frontier)
    """

    #tengo que hacer el object_dict en el formato del world
    parameter_list = parse_parameter(domain)
    object_dict = parse_objects(problem)
    

    ground_parameter(object_dict,parameter_list)

    def heuristic(state, action):
        return pathfinding.default_heuristic
        
    def isgoal(state):
        return True
    

    #pasar los objects del problema a formato diccionario para crear el mundo
    #debo crear un forall especial para sustituir las variables
    #que neighbors devuelva todos los nodos posibles a los que se puede llegar

    start = graph.Node()
    return pathfinding.astar(start, heuristic if useheuristic else pathfinding.default_heuristic, isgoal)

def main(domain, problem, useheuristic):
    t0 = time.time()
    (path,cost,visited_cnt,expanded_cnt) = plan(pddl.parse_domain(domain), pddl.parse_problem(problem), useheuristic)
    print("visited nodes:", visited_cnt, "expanded nodes:",expanded_cnt)
    if path is not None:
        print("Plan found with cost", cost)
        for n in path:
            print(n.name)
    else:
        print("No plan found")
    print("needed %.2f seconds"%(time.time() - t0))
    

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], "-d" not in sys.argv)