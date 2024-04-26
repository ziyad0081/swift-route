from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from osmnx import distance
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt # type: ignore
import numpy as np
import os
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

@app.route("/get_nearest", methods=['POST'])
def ReturnNearestHospital():
    req_data = request.get_json()["data"]
    user_lat,user_lng, user_serv  = req_data["lat"],req_data["lng"],req_data["serv"]
    possible_hospitals_by_service = [hospital['hospital_id'] for hospital in services[user_serv]]
    possible_hospitals_by_name = [hospitals[i] for i in possible_hospitals_by_service]
    closest_hospital = min(possible_hospitals_by_name, key=lambda hospital: distance.great_circle(user_lat, user_lng, hospital["lat"], hospital["lng"]))
    close_lat , close_lng = closest_hospital["lat"], closest_hospital["lng"]
    hospital_node = ox.nearest_nodes(G,close_lng, close_lat)
    user_node = ox.nearest_nodes(G, user_lng, user_lat)
    route = ox.shortest_path(G,user_node,hospital_node)
    route_json = [{'lat': G.nodes[node]['y'], 'lng': G.nodes[node]['x']} for node in [route[0]]]
    for i in range(len(route)-1):
        if 'geometry' in G[route[i]][route[i+1]][0]:
            linestr_coords =  G[route[i]][route[i+1]][0]['geometry']
            edge_geo = list(linestr_coords.coords)
            for point in edge_geo:
                route_json.append({'lat': point[1], 'lng': point[0]})
            route_json.append({'lat': G.nodes[route[i+1]]['y'], 'lng': G.nodes[route[i+1]]['x']})
    # route_json = [{'lat': G.nodes[node]['y'], 'lng': G.nodes[node]['x']} for node in route]
    returned_info = {"hos_name" : closest_hospital["name"], 
                     "iter" : route_json}
    return json.dumps(returned_info)

if __name__ == '__main__':
    app.run(debug=True)
    
