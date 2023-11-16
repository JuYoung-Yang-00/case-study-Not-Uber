"""

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



import math
import heapq


"""
'''
nodes = {}
with open('./data/node_data.json', 'r') as file:
    nodes = json.load(file)
'''




import csv



def calculate_travel_times(length, speeds):
    # Avoid division by zero in case of speed being zero
    return [length / speed if speed > 0 else float('inf') for speed in speeds] #hours


def get_edge_weight(current_time, edge):
    hour = current_time.hour
    if current_time.weekday() < 5:  # Weekday
        travel_time = edge[1][hour]
    else:  # Weekend
        travel_time = edge[2][hour]
    return travel_time


#creating the actual graph
def createGraph():
    edges = []
    graph = {}
    with open('givenDataFromSakai/edges.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
    
        # Iterate through each row in the CSV file
        n = 0
        for row in csv_reader:
            # Access the columns in the row
            start_id = int(row[0])
            end_id = int(row[1])
            length = float(row[2])
            weekdays = [float(value) for value in row[3:27]]
            weekends = [float(value) for value in row[27:]]

            edges.append((start_id, end_id, length, weekdays, weekends))
            n = n+1
            print(f"edge # {n} appended to edges[]")


    
    for start, end, length, weekdays, weekends in edges:
        if start not in graph:
            graph[start] = []
        weekday_times = calculate_travel_times(length, weekdays)
        weekend_times = calculate_travel_times(length, weekends)
        graph[start].append((end, weekday_times, weekend_times))

        
    
    print(f"GRAPH is created now, which has {len(graph)} nodes")
    return graph

