import heapq
import os
import time
import tracemalloc
import osmnx as ox
import networkx as nx
from osmnx import distance
from queue import PriorityQueue
from HealthcareNetworkProblem import HealthcareNetworkProblem,Node
NodeID = int
Solution = Node


class AStarSearch:
    def __init__(self, problem):
        self.problem = problem

    def search(self):
        """
            A* search algorithm implementation.
        """

        #initiale the frontier with the initial node
        initial_node = Node(self.problem.initial_state, cost=0)
        frontier = [(initial_node.cost + self.problem.heuristic(initial_node), initial_node)]
        heapq.heapify(frontier)

        #initial an empty set to keep track of explores nodes
        explored = {}
        expanded_nodes = 0

        #loop until the frontier is empty 
        while frontier:
            #pop the node with the lowest total cost from the frontier
            _, current_node = heapq.heappop(frontier) #_ to store the priority value that heapq.heappop() returns, 
            #but we're not going to use it. We're only interested in the current_node
            
            # Check if the current node is the goal state
            if self.problem.is_goal_test(current_node.state):
                return current_node,expanded_nodes,True,explored
            
            # Check if the current node has already been explored
            if current_node.state in explored and explored[current_node.state] <= current_node.cost:
                continue

            # Mark the current node as explored and record its cost
            explored[current_node.state] = current_node.cost
            # Calculate the cost and heuristic for the child node
            for child_node in self.problem.expand_node(current_node, heuristic=True):
                child_cost = child_node.cost
                child_heuristic = self.problem.heuristic(child_node)
            
                # Add the child node to the frontier if it's not already explored or has a lower cost
                if child_node.state not in explored or explored[child_node.state] > child_cost:
                    heapq.heappush(frontier, (child_cost + child_heuristic, child_node))
            expanded_nodes += 1
        return None

class UniformCostSearch:
    """
    A class implementing Uniform Cost Search algorithm on problems implementing necessary methods.
    """
    def __init__(self, problem):
        self.problem = problem

    def search(self):

        initial_node = Node(self.problem.initial_state, cost=0)
        frontier = [(initial_node.cost, initial_node)]
        heapq.heapify(frontier)
        explored = {}
        node_expansions = 0
        while frontier:
            try:

                current_cost, current_node = heapq.heappop(frontier)
            except TypeError:
                current_cost, current_node = heapq.heappop(frontier)
            if self.problem.is_goal_test(current_node.state):
                return current_node,node_expansions,True,explored
            if current_node.state in explored and explored[current_node.state] <= current_cost:
                continue
            explored[current_node.state] = current_cost
            node_expansions += 1
            for child_node in self.problem.expand_node(current_node):
                c_cost = child_node.cost
                if child_node.state not in explored or explored[child_node.state] > child_node.cost:
                    heapq.heappush(frontier, (c_cost, child_node))

        return None,0,False,explored
    

class IterativeDeepeningSearch:
    """
    A class implementing the Iterative Deepening search algorithm on problems implementing necessary methods.

    This class must be initialized with a maximum depth.
    """
    def __init__(self, problem: HealthcareNetworkProblem, max_depth_limit: int = 500):
        self.problem = problem
        self.max_depth_limit = max_depth_limit
        self.node_expansion = 0
    
    def search(self):
        self.node_expansion = 0
        visited = {}
        for depth in range(self.max_depth_limit):
            solution, node_expansion, is_goal, _visited = self.depth_limited_search(depth)
            for key in _visited.keys():
                visited[key] = True
            if solution is not None:
                return solution, node_expansion, is_goal, visited
        return None,0,False,visited

    def depth_limited_search(self, depth_limit: int):
        frontier = [(Node(self.problem.initial_state,parent=None, action=None, cost=0),0)]
        visited = {}
        while frontier:
            current_node, current_depth = frontier.pop()
            if current_depth == depth_limit:
                continue
            children = self.problem.expand_node(current_node)
            self.node_expansion += 1
            for child in children:
                if child.state not in visited and (child,current_depth+1) not in frontier:
                    visited[child.state] = True
                    if self.problem.is_goal_test(child.state):
                        return child, self.node_expansion, True, visited
                    frontier.append((child, current_depth+1))
        return None,0,False,visited
class BreadthFirstSearch:
    """
    A class implementing the breadth-first search algorithm on problems implementing necessary methods.
    """
    def __init__(self, problem:HealthcareNetworkProblem) -> None:
        self.problem = problem

    """
        Executes the breadth-first search algorithm to find a solution to the problem.

        Returns:
        --------

        tuple: A tuple containing the solution node, the number of node expansions, and a boolean indicating if a solution was found.
    """

    def search(self) -> Solution | None:
        frontier = [Node(self.problem.initial_state,parent=None, action=None, cost=0)]
        expansion_counter = 0
        visited = {}
        while frontier:
            current_node = frontier.pop(0)

            children = self.problem.expand_node(current_node)
            expansion_counter += 1
            
            for child in children:
                if child.state not in visited and child not in frontier:
                    if self.problem.is_goal_test(child.state):
                        return child, expansion_counter, True, visited
                    frontier.append(child)

        return None




