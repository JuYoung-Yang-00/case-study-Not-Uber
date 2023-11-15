# create weekday 0~23hr and weekend 0~23hr graphs, total of 48 graphs


import pandas as pd
import networkx as nx
import json


# RETURNS THE 48 GRAPHS
def createGraphs():
    # Load node data
    with open('givenDataFromSakai/node_data.json', 'r') as file:
        node_data = json.load(file)

    # Load edge data
    edges_df = pd.read_csv('givenDataFromSakai/edges.csv')

    # Initialize a dictionary to store graphs
    graphs = {}

    # Create a graph for each time slot
    time_slots = edges_df.columns[3:]  # exclude start_id, end_id, length --> so, time_slots is weekday_0, weekday_1, etc...
    for slot in time_slots:
        G = nx.DiGraph()

        # for all nodes in node_data.json
        for node_id, coords in node_data.items():
            G.add_node(int(node_id), pos=(float(coords['lon']), float(coords['lat'])))
    
        # Add edges with weights, weights being time = distance (miles) / speed (mph) = unit in hours
        for _, row in edges_df.iterrows():
            start_id, end_id, length, speed = int(row['start_id']), int(row['end_id']), float(row['length']), float(row[slot])
            if speed > 0:  # To avoid division by zero
                weight = length / speed
                G.add_edge(start_id, end_id, weight=weight)
    
        graphs[slot] = G
        print(f"added {slot} graph to graphs, the dictionary that contains 48 graphs. the graph that just got added has {G.number_of_nodes()} vertices and {G.number_of_edges()} edges")
        print(f"graphs is now a dictionary of length {len(graphs)}")
    
    return graphs

        


# Now `graphs` contains 48 directed graphs for each time slot


#createGraphs()
