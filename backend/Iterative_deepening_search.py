import os
import osmnx as ox
from osmnx import distance
import networkx as nx
from HealthcareNetworkProblem import HealthcareNetworkProblem, Node



NodeID = int

FILE_PATH = "algiers.graphml"
if os.path.exists(FILE_PATH):
    G = ox.load_graphml(FILE_PATH)
else:
    G = ox.graph_from_place("Algiers", network_type="drive")
    ox.save_graphml(G, filepath=FILE_PATH)




class IterativeDeepeningSearch:
    def __init__(self, problem: HealthcareNetworkProblem, max_depth_limit: int = 500):
        self.problem = problem
        self.max_depth_limit = max_depth_limit
        self.node_expansion = 0
    def search(self):
        self.node_expansion = 0
        for depth in range(self.max_depth_limit):
            result = self.depth_limited_search(self.problem.initial_state, depth)
            if result is not None:
                return result
        return None

    def depth_limited_search(self, state: NodeID, depth_limit: int):
        return self.recursive_dls(Node(state), depth_limit, 0)

    def recursive_dls(self, node: Node, depth_limit: int, current_depth: int):
        visited = set() 
        if self.problem.is_goal_test(node.state):
            return node,self.node_expansion,True
        elif current_depth == depth_limit:
            return None
        else:
            visited.add(node.state)
            self.node_expansion += 1
            for child in self.problem.expand_node(node):
                if child.state not in visited:
                    result = self.recursive_dls(child, depth_limit, current_depth + 1)
                    if result is not None:
                        return result,self.node_expansion,True
            return None
        

class BreadthFirstSearch:
    def __init__(self, problem:HealthcareNetworkProblem):
        self.problem = problem

    def search(self):
        frontier = [Node(self.problem.initial_state,parent=None, action=None, cost=0)]
        expansion_counter = 0
        while frontier:
            current_node = frontier.pop(0)

            children = self.problem.expand_node(current_node)
            expansion_counter += 1
            
            for child in children:
                if self.problem.is_goal_test(child.state):
                    return child,expansion_counter,True
                frontier.append(child)
        return None


# hospital_locations = (36.78144029121514, 2.981447383316992)
# user = (36.687997972279334, 2.869543352130313)


# hospital_node = ox.nearest_nodes(G, hospital_locations[1], hospital_locations[0])
# user_node = ox.nearest_nodes(G, user[1], user[0])


# problem = HealthcareNetworkProblem(user_node, hospital_node, G)


# ids = IterativeDeepeningSearch(problem, max_depth_limit=300)  


# result_node = ids.search()


# if result_node is not None:
#     path = []
#     while result_node is not None:
#         path.append(result_node.state)
#         result_node = result_node.parent
#     path.reverse()
#     print("Path found:", path)
# else:
#     print("Goal not found within the depth limit.")