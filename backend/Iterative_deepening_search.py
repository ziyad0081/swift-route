import os
import osmnx as ox
from osmnx import distance
import networkx as nx
from backend import HealthcareNetworkProblem
from backend import Node


NodeID = int

FILE_PATH = "algiers.graphml"
if os.path.exists(FILE_PATH):
    G = ox.load_graphml(FILE_PATH)
else:
    G = ox.graph_from_place("Algiers", network_type="drive")
    ox.save_graphml(G, filepath=FILE_PATH)




class IterativeDeepeningSearch:
    def __init__(self, problem: HealthcareNetworkProblem, max_depth_limit: int = 100):
        self.problem = problem
        self.max_depth_limit = max_depth_limit
        self.visited = set() 
    def search(self):
        for depth in range(self.max_depth_limit):
            self.visited.clear()  
            result = self.depth_limited_search(self.problem.initial_state, depth)
            if result is not None:
                return result
        return None

    def depth_limited_search(self, state: NodeID, depth_limit: int):
        return self.recursive_dls(Node(state), depth_limit, 0)

    def recursive_dls(self, node: Node, depth_limit: int, current_depth: int):
        if self.problem.is_goal_test(node.state):
            return node
        elif current_depth == depth_limit:
            return None
        else:
            self.visited.add(node.state)
            for child in self.problem.expand_node(node):
                if child.state not in self.visited:
                    result = self.recursive_dls(child, depth_limit, current_depth + 1)
                    if result is not None:
                        return result
            return None


hospital_locations = (36.78144029121514, 2.981447383316992)
user = (36.687997972279334, 2.869543352130313)


hospital_node = ox.nearest_nodes(G, hospital_locations[1], hospital_locations[0])
user_node = ox.nearest_nodes(G, user[1], user[0])


problem = HealthcareNetworkProblem(user_node, hospital_node, G)


ids = IterativeDeepeningSearch(problem, max_depth_limit=300)  


result_node = ids.search()


if result_node is not None:
    path = []
    while result_node is not None:
        path.append(result_node.state)
        result_node = result_node.parent
    path.reverse()
    print("Path found:", path)
else:
    print("Goal not found within the depth limit.")