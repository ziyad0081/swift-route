import heapq
import os
import osmnx as ox
import networkx as nx
from osmnx import distance
from queue import PriorityQueue
NodeID = int

from HealthcareNetworkProblem import HealthcareNetworkProblem,Node
class AStarSearch:
    def __init__(self, problem):
        """
        Constructor for the AStarSearch class.

        Parameters:
        - problem: An instance of a problem class that implements the necessary methods for A* search.
        """
        self.problem = problem

    def search(self):
        """
            A* search algorithm implementation.

            Returns:
            - The goal node if a solution is found, None otherwise.
        """

        #initiale the frontier with the initial node
        initial_node = Node(self.problem.initial_state, cost=0)
        frontier = [(initial_node.cost + self.problem.heuristic(initial_node), initial_node)]
        heapq.heapify(frontier)

        #initial an empty set to keep track of explores nodes
        explored = {}


        #loop until the frontier is empty 
        while frontier:
            #pop the node with the lowest total cost from the frontier
            _, current_node = heapq.heappop(frontier) #_ to store the priority value that heapq.heappop() returns, 
            #but we're not going to use it. We're only interested in the current_node
            
            # Check if the current node is the goal state
            if self.problem.is_goal_test(current_node.state):
                return current_node
            
            # Check if the current node has already been explored
            if current_node.state in explored and explored[current_node.state] <= current_node.cost:
                continue

            # Mark the current node as explored and record its cost
            explored[current_node.state] = current_node.cost
            # Calculate the cost and heuristic for the child node
            for child_node in self.problem.expand_node(current_node):
                child_cost = child_node.cost
                child_heuristic = self.problem.heuristic(child_node)

                # Add the child node to the frontier if it's not already explored or has a lower cost
                if child_node.state not in explored or explored[child_node.state] > child_cost:
                    heapq.heappush(frontier, (child_cost + child_heuristic, child_node))

        return None

class UniformCostSearch:
    def __init__(self, problem):
        self.problem = problem

    def search(self):
        initial_node = Node(self.problem.initial_state, cost=0)
        frontier = [(initial_node.cost, initial_node)]
        heapq.heapify(frontier)
        explored = {}

        while frontier:
            current_cost, current_node = heapq.heappop(frontier)
            if self.problem.is_goal_test(current_node.state):
                return current_node
            if current_node.state in explored and explored[current_node.state] <= current_cost:
                continue
            explored[current_node.state] = current_cost
            for child_node in self.problem.expand_node(current_node):
                if child_node.state not in explored or explored[child_node.state] > child_node.cost:
                    heapq.heappush(frontier, (child_node.cost, child_node))

        return None
    
FILE_PATH = "algiers.graphml"
if os.path.exists(FILE_PATH):
    G = ox.load_graphml(FILE_PATH)
else:
    G = ox.graph_from_place("Algiers", network_type="drive")
    ox.save_graphml(G, filepath=FILE_PATH)

# Define initial and goal states
hospital_locations = (36.75463665801327, 3.0010462208468907)
user = (36.73650321779211, 3.28275427992133)

hospital = ox.nearest_nodes(G, hospital_locations[1], hospital_locations[0])
user = ox.nearest_nodes(G, user[1], user[0])

# Create a problem instance
problem = HealthcareNetworkProblem(initial_state=user, goal_state=hospital, transition_model=G)

# Run A* search
search_algorithm_a_star = AStarSearch(problem)
solution_a_star = search_algorithm_a_star.search()

if solution_a_star is not None:
    print("A* Search Solution found!")
    # Construct path
    path = []
    node = solution_a_star
    while node is not None:
        path.append(node.state)
        node = node.parent
    path.reverse()
    print("Path:", path)
else:
    print("A* Search No solution found.")

# Run Uniform Cost Search
search_algorithm_uniform_cost = UniformCostSearch(problem)
solution_uniform_cost = search_algorithm_uniform_cost.search()

if solution_uniform_cost is not None:
    print("Uniform Cost Search Solution found!")
    # Construct path
    path = []
    node = solution_uniform_cost
    while node is not None:
        path.append(node.state)
        node = node.parent
    path.reverse()
    print("Path:", path)
else:
    print("Uniform Cost Search No solution found.")


