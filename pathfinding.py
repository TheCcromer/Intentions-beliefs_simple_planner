import graph
from priority_queue import *

def default_heuristic(n, edge):
    """
    Default heuristic for A*. Do not change, rename or remove!
    """
    return 0

def astar(start, heuristic, goal):
    path = []
    expanded = 0
    queue = PriorityQueue()
    actual_node = start
    edge_crossed = [[],[],[],[]] #1: list of id   #2: list of source node index   #3: list of distances   #4: list of respective node
    total_edges_seen = ([],[]) #1: list of edges  #2: list of source node
    total_nodes_seen = []
    total_nodes_seen.append(start.get_id())
    edge_crossed[0].append(start.get_id())
    edge_crossed[1].append(start.get_id())
    edge_crossed[2].append(0)
    edge_crossed[3].append(start)
    was_expanded = False
    while(not goal(actual_node)):
        for edge in actual_node.get_neighbors():           
            if(edge not in total_edges_seen[0]): #only add to frontier if the edge was not added before
                total_edges_seen[0].append(edge)
                total_edges_seen[1].append(actual_node.get_id())
                was_expanded = True
                if(edge.target.get_id() not in total_nodes_seen): #this is to calcule the total of nodes visited
                    total_nodes_seen.append(edge.target.get_id())
                actual_node_index = edge_crossed[0].index(actual_node.get_id())
                queue.insert(edge,(edge.cost + edge_crossed[2][actual_node_index]),heuristic(edge.target,edge)) #the edge is added to the priority queue
        if(was_expanded): #if some new edge was added in this iteration, counts as a expandation
            expanded += 1
            was_expanded = False
        selected_edge = queue.pop() #obtaining the high priority edge
        edge_crossed[0].append(selected_edge[0].target.get_id())
        index = total_edges_seen[0].index(selected_edge[0]) 
        source_node = total_edges_seen[1][index]
        edge_crossed[1].append(edge_crossed[0].index(source_node)) #this is important to return the path at the end, because saves the source node of the edge
        edge_crossed[2].append(selected_edge[1]) #this is important to control the distance in a specific node during the searching phase
        edge_crossed[3].append(selected_edge[0].target)
        actual_node = selected_edge[0].target


    #creating the path
    if(goal(start)):
        path.append(start)
    else:
        new_index = len(edge_crossed[0]) - 1
        node_crossed = edge_crossed[3][new_index]  #this will be return the goal node
        while(new_index != 0): #this loop will be doing a backward search from the goal node until the start node
            path.append(node_crossed)
            new_index = edge_crossed[1][new_index]
            node_crossed = edge_crossed[3][new_index]
        path.append(start) #at the end the start node is added
        path.reverse() #Because the path is added from the end to the start, the list is reversed


    return path,edge_crossed[2][-1],len(total_nodes_seen),expanded

def print_path(result):
    (path,cost,visited_cnt,expanded_cnt) = result
    print("visited nodes:", visited_cnt, "expanded nodes:",expanded_cnt)
    if path:
        print("Path found with cost", cost)
        for n in path:
            print(str(n.get_id()))
    else:
        print("No path found")
    print("\n")

def main():
    """
    You are free (and encouraged) to change this function to add more test cases.
    
    You are provided with three test cases:
        - pathfinding in Austria, using the map shown in class. This is a relatively small graph, but it comes with an admissible heuristic. Below astar is called using that heuristic, 
          as well as with the default heuristic (which always returns 0). If you implement A* correctly, you should see a small difference in the number of visited/expanded nodes between the two heuristics.
        - pathfinding on an infinite graph, where each node corresponds to a natural number, which is connected to its predecessor, successor and twice its value, as well as half its value, if the number is even.
          e.g. 16 is connected to 15, 17, 32, and 8. The problem given is to find a path from 1 to 2050, for example by doubling the number until 2048 is reached and then adding 1 twice. There is also a heuristic 
          provided for this problem, but it is not admissible (think about why), but it should result in a path being found almost instantaneously. On the other hand, if the default heuristic is used, the search process 
          will take a noticeable amount (a couple of seconds).
        - pathfinding on the same infinite graph, but with infinitely many goal nodes. Each node corresponding to a number greater 1000 that is congruent to 63 mod 123 is a valid goal node. As before, a non-admissible
          heuristic is provided, which greatly accelerates the search process. 
    """
    target = "Bregenz"
    def atheuristic(n, edge):
        return graph.AustriaHeuristic[target][n.get_id()]
    def atgoal(n):
        return n.get_id() == target
    
    result = astar(graph.Austria["Eisenstadt"], atheuristic, atgoal)
    print_path(result)
    
    result = astar(graph.Austria["Eisenstadt"], default_heuristic, atgoal)
    print_path(result)
    
    target = 2050
    def infheuristic(n, edge):
        return abs(n.get_id() - target)
    def infgoal(n):
        return n.get_id() == target
    
    result = astar(graph.InfNode(1), infheuristic, infgoal)
    print_path(result)
    
    result = astar(graph.InfNode(1), default_heuristic, infgoal)
    print_path(result)
    
    def multiheuristic(n, edge):
        return abs(n.get_id()%123 - 63)
    def multigoal(n):
        return n.get_id() > 1000 and n.get_id()%123 == 63
    
    result = astar(graph.InfNode(1), infheuristic, multigoal)
    print_path(result)
    
    result = astar(graph.InfNode(1), default_heuristic, multigoal)
    print_path(result)
    

if __name__ == "__main__":
    main()