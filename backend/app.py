from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from osmnx import distance
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt # type: ignore
import numpy as np
import os
from HCSolver import LocalSearchSolver
from HealthcareNetworkProblem import HealthcareNetworkProblem
FILE_PATH = "algiers.graphml"
if os.path.exists(FILE_PATH):
    G = ox.load_graphml(FILE_PATH)
else:
    G = ox.graph_from_place("Algiers", network_type="drive")
    ox.save_graphml(G, filepath=FILE_PATH)

app = Flask(__name__)
CORS(app)
#This file will contain the api needed to connect the path finding algorithms to the front end , don't worry about it.
with open(os.path.join(os.getcwd(),'src','assets','data','hospitals.json')) as f:
    services = json.load(f)["services"]
with open(os.path.join(os.getcwd(),'src','assets','data','hospital_info.json')) as g:
    hospitals = json.load(g)

P = HealthcareNetworkProblem(None,None,G)

hc = LocalSearchSolver(P)

@app.route("/debug", methods=['POST'])
def DebugingEndPoint():
    #USED FOR DEBUGGING , WILL BE REMOVED LATER.
    req_data = request.get_json()["data"]
    user_lat,user_lng, user_serv  = req_data["lat"],req_data["lng"],req_data["serv"]
    possible_hospitals_by_service = [hospital['hospital_id'] for hospital in services[user_serv]]
    possible_hospitals_by_name = [hospitals[i] for i in possible_hospitals_by_service]
    closest_hospital = min(possible_hospitals_by_name, key=lambda hospital: distance.great_circle(user_lat, user_lng, hospital["lat"], hospital["lng"]))
    close_lat , close_lng = closest_hospital["lat"], closest_hospital["lng"]
    hospital_node = ox.nearest_nodes(G,close_lng, close_lat)
    user_node = ox.nearest_nodes(G, user_lng, user_lat)
    max_nodes = len(list(G.nodes()))
    P.reinitialize_states(user_node, hospital_node)
    
    route = hc.SimulatedAnnealingWrapper()
    return json.dumps(route)


@app.route("/get_nearest", methods=['POST'])
def ReturnNearestHospital():
    #recieve request body
    req_data = request.get_json()["data"]
    #get user coordinates and requested service
    user_lat,user_lng, user_serv  = req_data["lat"],req_data["lng"],req_data["serv"]

    #get all fitting candidate hospital ids (ones providing user_serv)
    possible_hospitals_by_service = [hospital['hospital_id'] for hospital in services[user_serv]]

    #get hospital names via id
    possible_hospitals_by_name = [hospitals[i] for i in possible_hospitals_by_service]

    #estimate closest of candidates by heuristic
    closest_hospital = min(possible_hospitals_by_name, key=lambda hospital: distance.great_circle(user_lat, user_lng, hospital["lat"], hospital["lng"]))

    #retrieved closest hospital coordinates
    close_lat , close_lng = closest_hospital["lat"], closest_hospital["lng"]

    #initiate goal and initial nodes
    hospital_node = ox.nearest_nodes(G,close_lng, close_lat) #goal_node
    user_node = ox.nearest_nodes(G, user_lng, user_lat) #initial_node
    max_nodes = len(list(G.nodes())) #nodes count in the graph (used in search statistics)

    P.reinitialize_states(user_node, hospital_node) #initialize problem with our states
    
    route_info = hc.KLocalBeamSearchWrapper(5) #This call here is the only thing that will differ between search algorithms

    route = route_info.get("path") #get the path from returned dict

    route_info.pop("path") #removed it to return the rest without redundancy

    route_info["max_nodes"] = max_nodes  #add the graph nodes count from before

    #This section processes route graph nodes and constructs all possible road geometries for edges (so as not to make all roads a straight line) 
    route_json = [{'lat': G.nodes[node]['y'], 'lng': G.nodes[node]['x']} for node in [route[0]]]
    for i in range(len(route)-1):
        if 'geometry' in G[route[i]][route[i+1]][0]:
            linestr_coords =  G[route[i]][route[i+1]][0]['geometry']
            edge_geo = list(linestr_coords.coords)
            for point in edge_geo:
                route_json.append({'lat': point[1], 'lng': point[0]})
            route_json.append({'lat': G.nodes[route[i+1]]['y'], 'lng': G.nodes[route[i+1]]['x']})
    
    #this object holds all information to be returned to the frontend 
    returned_info = {"hos_name" : closest_hospital["name"], 
                     "iter" : route_json,
                     "details" : route_info}
    #return json to frontend
    return json.dumps(returned_info)

if __name__ == '__main__':
    app.run(debug=True)

