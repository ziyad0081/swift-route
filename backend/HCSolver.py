import math
import random
import time
from HealthcareNetworkProblem import HealthcareNetworkProblem, Node
import heapq
import tracemalloc
from memory_profiler import memory_usage
Problem = HealthcareNetworkProblem
Solution = Node
Path = list[int]

class LocalSearchSolver:
    """
    LocalSearchSolver implements some local search algorithms for optimization problem formulation

    Attributes:
    -----------
    - problem (Problem): A problem meeting HealthcareNetworkProblem definition skeleton

    Methods:
    --------
    - HillClimbingSearch(): Performs hill climbing search on the given problem.
    - KLocalBeamSearch(population:int, max_no_imprv:int): Performs K-Local Beam search on the given problem with the specified population size.

    Methods Return:
    --------------
    - tuple : containing 
        - The best found node. (optimally a solution) 
        - Number of expanded nodes 
        - Boolean indicating if the node returned is a goal

    """
    
    def __init__(self, problem:Problem, method) -> None:
        self.problem = problem
        self.method = method

    def search(self) -> Solution|None:
        match self.method:
            case "HC":
                return self.HillClimbingSearch()
            case "KLBS":
                return self.KLocalBeamSearch()
            case "SA":
                return self.SimulatedAnnealing()

    def HillClimbingSearch(self) -> Solution|None:
        """
        This function performs a hybrid Stochastic Hill climbing search algorithm on the problem given as argument in class initialization        
        """

        #Initialize initial state in the state space
        current_node = Node(state=self.problem.initial_state,parent=None,action=None, cost=0) 
        node_expansion = 0
        visited = {}
        downhill_counter = 10
        while(1):
            #if current node is a goal, just return it
            visited[current_node.state] = True
            if self.problem.is_goal_test(current_node.state):
                return current_node, node_expansion, True, visited
            
            #Get all node neighbours
            successors = self.problem.expand_node(current_node)
            
            node_expansion += 1
            
            #Take only better neighbours
            current_node_eval = self.problem.heuristic(current_node)
            better_successors_pool = list(filter(lambda successor: self.problem.heuristic(successor) <= current_node_eval, successors ))
            try:
                #We get the best element in the better successors
                best_in_better = min(better_successors_pool, key=lambda successor: self.problem.heuristic(successor))
                
                #if the best element's eval is very small (less than 150m) we take it instead in fear of deviating away from an easy goal (as the distance is very small and we can risk taking greedy moves)
                if(self.problem.heuristic(best_in_better) < 150):
                    best_successor = best_in_better
                else: #, we proceed with taking a random move among the best ones
                    best_successor = random.choice(better_successors_pool) #Choose a better neighbour at random
            except (IndexError,ValueError):
                #if there are no better moves , we take the best downhill moves in hope of exploring new places that might lead to goal
                try:

                    if(downhill_counter > 0):
                        best_successor = random.choice(successors)
                        downhill_counter -= 1 #yet we do it only down_hill counter times
                except IndexError:
                    best_successor = current_node # If the list is empty just take the current node as the best next
            
            #get neighbour's evaluation
            best_successor_eval = self.problem.heuristic(best_successor)
            
            
            #Return none if no improvement is achieved by moving to a neighbour (local maximum)
            if current_node_eval <= best_successor_eval and downhill_counter < 1 or (current_node_eval == best_successor_eval and downhill_counter >= 1) :
                return current_node, node_expansion, False,visited
            else:
                #if there is improvement , reiterate with the best neighbour or we are allowed some downhill moves
                current_node = best_successor

    

        returned_obj = {}
        start_time = time.time()
        tracemalloc.start()

        solution,node_expansion, is_goal = self.SimulatedAnnealing()
        current, peak = tracemalloc.get_traced_memory()

        tracemalloc.stop()
        end_time = time.time()
        time_diff = end_time - start_time
        path = []
        sol_cost = 0
        
        if isinstance(solution, Node):
            dummy_iterator = solution
            while(dummy_iterator is not None):
                path.append(dummy_iterator.state)
                dummy_iterator = dummy_iterator.parent

        returned_obj["path"] = path[::-1]
        returned_obj["expanded_nodes"] = node_expansion
        returned_obj["found_goal"] = is_goal
        returned_obj["search_time"] = time_diff
        returned_obj["solution_cost"] = solution.cost
        returned_obj["peak_mem"] = peak/(1024**2)
        return returned_obj
    def KLocalBeamSearch(self, population:int=30,MAX_NO_IMPRV:int=200,MAX_ITER:int=700) -> tuple[Solution,int] | None:
        """
        K-LocalBeamSearch algorithm that can be applied on problems having necessary methods

        Args:
        ----
        - Population (int):Determines the maximum beam size to carry between iterations (Default 10)
        - MAX_NO_IMPRV (int):Determines the maximum allowed consecutive generations without improvement in terms of evaluation (Higher values potentially lead to longer runtimes, Default 50 iterations)
        - MAX_ITER (int): The total maximum number of iterations the function is allowed to run. (Default to 500) 
        
        """
        
        #Initialize the population to one available initial state.
        current_pool = [Node(state=self.problem.initial_state,parent=None,action=None, cost=0)]
        node_expansion_counter = 0
        visited = {}
        no_improvement_count = 0 #This variable will serve the role of a watchdog incase no improvement is being made across too many generations (local maximum)
        iter_count = 0
        while(1):
            successors_pool = []
            iter_count+=1
            #Generating all neighbours of current population
            for individual in current_pool:
                visited[individual.state] = True
                node_expansion_counter += 1
                successors_pool.extend(self.problem.expand_node(individual))
            
            #Getting the score of the best individual in the current population
            best_in_current_population = min(current_pool, key= lambda ind:self.problem.heuristic(ind))
            
            #Setting the current pool to the best atmost k-neighbours (could be less)
            current_pool = heapq.nsmallest(min(population,len(successors_pool)),successors_pool,key= lambda successor:self.problem.heuristic(successor))
            
            #checking if the best individual is a goal state 
            if(self.problem.is_goal_test(current_pool[0].state)):
                print("here" , flush=True)
                return current_pool[0],node_expansion_counter,True,visited
            
            #if the best from previous generation is better than the best in current generation then no improvement has been made
            if(self.problem.heuristic(best_in_current_population) <= self.problem.heuristic(current_pool[0])):
                no_improvement_count += 1
            
            #else, reset the watchdog
            else:
                no_improvement_count = 0
            
            #if we record no improvement across MAX_NO_IMPRV or we reached maximum iterations we stop the search and return the best individual
            if(no_improvement_count > MAX_NO_IMPRV or iter_count == MAX_ITER ):
                
                return current_pool[0],node_expansion_counter,False,visited
            
    def SimulatedAnnealing(self,initial_temperature:int=1000, cooling_rate:float=0.99, cold_threshold:float=0.1):
        
        current_individual = Node(state=self.problem.initial_state,parent=None,action=None, cost=0)
        current_tempurature = initial_temperature
        node_expansion = 0
        visited = {}
        while current_tempurature > cold_threshold:
            visited[current_individual.state] = True
            if self.problem.is_goal_test(current_individual.state):
                return current_individual,node_expansion,True
            current_individual_neighbours = self.problem.expand_node(current_individual)
            node_expansion+=1
            if len(current_individual_neighbours) == 0:
                return current_individual,node_expansion,False
            
            random_neighbour = random.choice(current_individual_neighbours)

            energy_diff = self.problem.heuristic(random_neighbour) -  self.problem.heuristic(current_individual)

            if energy_diff < 0 or random.random() < math.exp(-energy_diff / current_tempurature):
                current_individual = random_neighbour

            current_tempurature *= cooling_rate
        
        
        return current_individual,node_expansion,self.problem.is_goal_test(current_individual.state),visited
        
        
        
            
            