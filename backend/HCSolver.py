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
    """
    
    def __init__(self, problem:Problem) -> None:
        self.problem = problem
        
    def HillClimbingSearch(self) -> Solution|None:
        """
        This function performs hill climbing search on the problem given as argument in class initialization

        Parameters:
        - No parameters

        Returns:
        - A sequence of MultiDiGraph NodeIDs representing the route 
        """

        #Initialize initial state in the state space
        current_node = Node(state=self.problem.initial_state,parent=None,action=None, cost=0) 
        node_expansion = 0
        while(1):
            #if current node is a goal, just return it
            if self.problem.is_goal_test(current_node.state):
                return current_node, node_expansion, True
            
            #Get all node neighbours
            successors = self.problem.expand_node(current_node)
            node_expansion += 1
            #choose the best
            best_successor = min(successors, key= lambda successor:self.problem.heuristic(successor))
            
            #get both the current state's evaluation and its best neighbour's
            best_successor_eval = self.problem.heuristic(best_successor)
            current_node_eval = self.problem.heuristic(current_node)
            
            #Return none if no improvement is achieved by moving to a neighbour (local maximum)
            if current_node_eval <= best_successor_eval:
                return current_node, node_expansion, False
            else:
                #if there is improvement , reiterate with the best neighbour
                current_node = best_successor

    def HillClimbingSearchWrapper(self) -> Path|None:
        
        returned_obj = {}
        start_time = time.time()
        tracemalloc.start()
        solution, node_expansion, is_goal = self.HillClimbingSearch()
        current, peak = tracemalloc.get_traced_memory()

        tracemalloc.stop()
        end_time = time.time()
        time_diff = end_time - start_time
        path = []
        sol_cost = 0

        if isinstance(solution, Node):
            dummy_iterator = solution
            sol_cost = solution.cost
            while(dummy_iterator is not None):
                path.append(dummy_iterator.state)
                dummy_iterator = dummy_iterator.parent
        
        returned_obj["path"] = path[::-1]
        returned_obj["expanded_nodes"] = node_expansion
        returned_obj["found_goal"] = is_goal
        returned_obj["search_time"] = time_diff
        returned_obj["solution_cost"] = sol_cost
        returned_obj["peak_mem"] = peak/(1024**2)
        return returned_obj
    
    def KLocalBeamSearchWrapper(self, population:int,MAX_NO_IMPRV:int=50) -> dict|None:
        
        """
        This function performs K-Local Beam search on the problem given as argument in class initialization

        Parameters:
        ----------
        - population (int): The size of population to carry between generations
        - max_no_improvment (int): Allowed consequtive generations without improvement

        Returns:
        -------
        - A sequence of MultiDiGraph NodeIDs representing the route.
        - Time taken during search in seconds.
        - Peak memory usage during search in MB
        """
        returned_obj = {}
        start_time = time.time()
        tracemalloc.start()
        solution, node_expansion,is_goal  = self.KLocalBeamSearch(population)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time = time.time()
        time_diff = end_time - start_time
        path = []
        sol_cost = 0
        if isinstance(solution, Node):
            sol_cost = solution.cost
            dummy_iterator = solution
            while(dummy_iterator is not None):
                path.append(dummy_iterator.state)
                dummy_iterator = dummy_iterator.parent
        
        returned_obj["path"] = path[::-1]
        returned_obj["expanded_nodes"] = node_expansion
        returned_obj["found_goal"] = is_goal
        returned_obj["search_time"] = time_diff
        returned_obj["solution_cost"] = sol_cost
        returned_obj["peak_mem"] = peak/(1024**2)
        return returned_obj
    def SimulatedAnnealingWrapper(self,initial_temperature:int=1000, cooling_rate:float=0.99, cold_threshold:float=0.1) -> Path|None:

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
    def KLocalBeamSearch(self, population:int,MAX_NO_IMPRV:int=50,MAX_ITER:int=200) -> tuple[Solution,int] | None:
        
        
        #Initialize the population to one available initial state.
        current_pool = [Node(state=self.problem.initial_state,parent=None,action=None, cost=0)]
        node_expansion_counter = 0
        
        no_improvement_count = 0 #This variable will serve the role of a watchdog incase no improvement is being made across too many generations (local maximum)
        iter_count = 0
        while(1):
            successors_pool = []
            iter_count+=1
            #Generating all neighbours of current population
            for individual in current_pool:
                node_expansion_counter += 1
                successors_pool.extend(self.problem.expand_node(individual))
            
            #Getting the score of the best individual in the current population
            best_in_current_population = min(current_pool, key= lambda ind:self.problem.heuristic(ind))
            
            #Setting the current pool to the best atmost k-neighbours (could be less)
            current_pool = heapq.nsmallest(min(population,len(successors_pool)),successors_pool,key= lambda successor:self.problem.heuristic(successor))
            
            #checking if the best individual is a goal state 
            if(self.problem.is_goal_test(current_pool[0].state)):
                print("here" , flush=True)
                return current_pool[0],node_expansion_counter,True
            
            #if the best from previous generation is better than the best in current generation then no improvement has been made
            if(self.problem.heuristic(best_in_current_population) <= self.problem.heuristic(current_pool[0])):
                no_improvement_count += 1
            
            #else, reset the watchdog
            else:
                no_improvement_count = 0
            
            #if we record no improvement across MAX_NO_IMPRV or we reached maximum iterations we stop the search and return the best individual
            if(no_improvement_count > MAX_NO_IMPRV or iter_count == MAX_ITER ):
                
                return current_pool[0],node_expansion_counter,False
    
    def SimulatedAnnealing(self,initial_temperature:int=1000, cooling_rate:float=0.99, cold_threshold:float=0.1):
        
        current_individual = Node(state=self.problem.initial_state,parent=None,action=None, cost=0)
        current_tempurature = initial_temperature
        node_expansion = 0
        while current_tempurature > cold_threshold:
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
        
        
        return current_individual,node_expansion,self.problem.is_goal_test(current_individual.state)
        
        
        
            
            