import os
import osmnx as ox
import networkx as nx
from osmnx import distance

NodeID = int

FILE_PATH = "algiers.graphml"
if os.path.exists(FILE_PATH):
    G = ox.load_graphml(FILE_PATH)
else:
    G = ox.graph_from_place("Algiers", network_type="drive")
    ox.save_graphml(G, filepath=FILE_PATH)



class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __eq__(self, other):
        return self.state == other.state
    
    
class HealthcareNetworkProblem:
    def __init__(self, initial_state:NodeID , goal_state:NodeID, transition_model):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.transition_model = transition_model
    def reinitialize_states(self, initial_state:NodeID, goal_state:NodeID ) -> None :
        self.initial_state = initial_state
        self.goal_state = goal_state
    
    def is_goal_test(self, state:NodeID):
        return state == self.goal_state
    
    def get_valid_actions(self, state:NodeID):
        return list(self.transition_model.neighbors(state)) 

    def apply_action(self, state:NodeID, action:NodeID):
        return action 

    def expand_node(self, node:Node):
        state = node.state
        valid_actions = self.get_valid_actions(state)
        child_nodes = []
        for action in valid_actions:
            child_state = action  # Assuming action directly leads to the next state
            edge_length = self.transition_model[node.state][child_state][0]['length']
            child_cost = node.cost + edge_length
            child_node = Node(child_state, parent=node, action=action, cost=child_cost)
            child_nodes.append(child_node)
        return child_nodes
    def heuristic(self,node:Node):
        hospital_coords = (G.nodes[self.goal_state]["y"],G.nodes[self.goal_state]["x"])
        node_id = node.state
        node_coords = (G.nodes[node_id]["y"],G.nodes[node_id]["x"])
        return distance.great_circle(lat1=node_coords[0],lon1=node_coords[1],lat2=hospital_coords[0],lon2=hospital_coords[1])
