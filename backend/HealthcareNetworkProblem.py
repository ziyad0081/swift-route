import random
import os
import osmnx as ox
import networkx as nx

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

    def __hash__(self):
        return hash(tuple(map(tuple, self.state)))
    
    
class HealthcareNetworkProblem:
    def __init__(self, initial_state, goal_state, G):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.G = G
    
    def is_goal_test(self, state):
        return state == self.goal_state
    
    def get_valid_actions(self, state):
        return list(self.G.neighbors(state)) 

    def apply_action(self, state, action):
        return action 
    
    def calculate_path_cost(self, parent_node, child_node):
  
        edge_length = self.G[parent_node][child_node][0].get('length')
        return edge_length

    def expand_node(self, node):
        state = node.state
        valid_actions = self.get_valid_actions(state)
        child_nodes = []
        for action in valid_actions:
            child_state = action  # Assuming action directly leads to the next state
            edge_length = self.G.edges[node.state, child_state][0]['length']
            child_cost = node.cost + edge_length
            child_node = Node(child_state, parent=node, action=action, cost=child_cost)
            child_nodes.append(child_node)
        return child_nodes


hospital_locations = {
    "0": {"lat": 36.76184927705564, "lng": 3.056220967141742},
    "1": {"lat": 36.778942158808825, "lng": 2.981616595880589},
    # Add other hospital locations here
}

# Choose a random hospital ID
random_hospital_id = random.choice(list(hospital_locations.keys()))

# Randomly choose user location within the range of hospital locations
user_location = (random.uniform(36.5, 37), random.uniform(2.8, 3.3))

# Ensure the user location is close to one of the hospital locations
min_distance = float('inf')
for hospital_id, hospital_loc in hospital_locations.items():
    distance = ((user_location[0] - hospital_loc['lat']) ** 2 + (user_location[1] - hospital_loc['lng']) ** 2) ** 0.5
    if distance < min_distance:
        min_distance = distance
        closest_hospital_id = hospital_id

# Example goal state (replace with your actual goal state)
goal_state = hospital_locations[random_hospital_id]

# Example initial state (replace with your actual initial state)
initial_state = (hospital_locations[closest_hospital_id]['lat'], hospital_locations[closest_hospital_id]['lng'])

# Create an instance of the HealthcareNetworkProblem class
problem = HealthcareNetworkProblem(initial_state, goal_state, G)

# Test the is_goal_test method
test_state = goal_state  # Goal state
print("Is test state a goal state?", problem.is_goal_test(test_state))  # Output: True

 # Test the get_valid_actions method
valid_actions = problem.get_valid_actions(initial_state)
print("Valid actions from initial state:", valid_actions) 

 # Test the apply_action method
action = valid_actions[0]  # Example action
new_state = problem.apply_action(initial_state, action)
print("New state after applying action:", new_state) 

# Test the expand_node method
node = Node(state=initial_state, parent=None, action=None, cost=0)
child_nodes = problem.expand_node(node)
print("Child nodes after expanding the initial node:")
for child_node in child_nodes:
    print(child_node.state, child_node.action, child_node.cost)