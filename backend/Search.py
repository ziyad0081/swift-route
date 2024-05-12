import base64
import osmnx as ox
from osmnx import utils_geo
import matplotlib.pyplot as plt
import time
import tracemalloc
from typing import Literal
from HealthcareNetworkProblem import HealthcareNetworkProblem, Node
from SearchStrategies import *
from HCSolver import LocalSearchSolver
SearchProblem = HealthcareNetworkProblem

class Search:
    def __init__(self, problem:SearchProblem, search_method:Literal["A*","UCS","BFS","IDS","HC","KLBM","SA"]):
        self.problem = problem
        self.method = search_method

    def RunSearch(self,generateViz:bool=False):
        SearchObject = None
        match self.method:
            case "A*":
                SearchObject = AStarSearch(self.problem)
            case "UCS":
                SearchObject = UniformCostSearch(self.problem)
            case "BFS":
                SearchObject = BreadthFirstSearch(self.problem)
            case "IDS":
                SearchObject = IterativeDeepeningSearch(self.problem)
            case _:
                SearchObject = LocalSearchSolver(self.problem,self.method)

        return self.SearchWrapper(SearchObject, generateViz)


    def SearchWrapper(self,SearchObj, generateViz:bool=False):
        """
        Search Performance Evaluation wrapper function for Search strategies implementing necessary methods .

        Args:
        -----
        SearchObj (SearchStrategy): An instance of AStarSearch or UniformCostSearch algorithm.

        Returns:
        --------
            - dict : A dictionary containing search and performance measure results  : (time, memory, node expansion, solution cost)

        Note :
        -----
        Alongside returned dictionary, the function generates search space images in ./search_result/detailed.png and ./search_result/overall.png 
        """
        returned_obj = {}
        start_time = time.time()
        tracemalloc.start()

        solution,node_expansion, is_goal,visited = SearchObj.search()

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
        else:
            returned_obj["error"] = "Selected Algorithm found no path to goal node"
            return returned_obj
        if generateViz:
            node_clrs = []
            node_size = []
            visited = set(visited)
            
            for node in self.problem.transition_model.nodes():
                if node in visited:
                    if node == self.problem.initial_state or node == self.problem.goal_state:
                        node_clrs.append('green')
                        node_size.append(20)
                    else :
                        node_clrs.append('r')
                        node_size.append(5)
                else:
                    node_clrs.append('w')
                    node_size.append(1)
            
            edge_color=[
            'b' if (u in path and v in path and path.index(u) == path.index(v) - 1) or
                    (v in path and u in path and path.index(v) == path.index(u) - 1)
            else 'w' 
            for u, v in self.problem.transition_model.edges(data=False)
            ]
            origin_node = self.problem.transition_model.nodes()[self.problem.initial_state]
            
            bbox = utils_geo.bbox_from_point(point=(origin_node["y"], origin_node["x"]), dist=4000)
            
            #generating images
            if not os.path.exists("search_result"):
                os.mkdir("search_result")
            ox.plot_graph(G=self.problem.transition_model, node_size=node_size ,node_color=node_clrs,edge_color=edge_color,save=True,dpi=600,close=True,show=False,bbox=bbox,filepath="search_result/detailed.png")
            ox.plot_graph(G=self.problem.transition_model, node_size=1 ,node_color=node_clrs,save=True,dpi=200,close=True,show=False,filepath="search_result/overall.png")
            
            #Reading images and sending them in the payload:
            with open("search_result/overall.png",'rb') as f:
                overall_data = f.read()

            overall_64 = base64.b64encode(overall_data).decode('utf-8')
            
            with open("search_result/detailed.png",'rb') as f:
                detailed_data = f.read()

            detailed_64 = base64.b64encode(detailed_data).decode('utf-8')
            returned_obj["overall_img"] = overall_64
            returned_obj["detailed_img"] = detailed_64
        #constructing payload
        
        
        returned_obj["path"] = path[::-1]
        returned_obj["expanded_nodes"] = node_expansion
        returned_obj["found_goal"] = is_goal
        returned_obj["search_time"] = time_diff
        returned_obj["solution_cost"] = sol_cost
        returned_obj["peak_mem"] = peak/(1024**2)
        
        return returned_obj