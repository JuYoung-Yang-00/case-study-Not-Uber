# lib.py
from datetime import datetime
from heapq import heappush, heappop
import json
import csv
from dataclasses import dataclass
from datetime import datetime
from typing import List
from kdtree import KDTree
from collections import defaultdict
import math

@dataclass
class Driver:
    requestTime: datetime
    sourceX: float
    sourceY: float

@dataclass
class Rider:
    requestTime: datetime
    sourceX: float
    sourceY: float
    destX: float
    destY: float

class DriverQueue:
    def __init__(self):
        self.queue: list[Driver] = []
    
    def popLongestWaitingDriver(self):
        self.queue.sort(key=lambda x: x.requestTime)
        return self.queue.pop(0)

class RiderQueue:
    def __init__(self):
        self.queue: list[Rider] = []

    def popLongestWaitingRider(self):
        self.queue.sort(key=lambda x: x.requestTime)
        return self.queue.pop(0)
    
############ load data
def load_data():
    print("loading data")

    driver_queue = DriverQueue()
    # load the driver data
    with open("./data/drivers.csv", 'r') as file:
        next(file)  # Skip the header line
        while True:
            line = file.readline()
            if not line:
                break  # Break the loop if no more data
            date_time_str, lat_str, lon_str = line.strip().split(',')
            request_time = datetime.strptime(date_time_str, '%m/%d/%Y %H:%M:%S')
            source_x = float(lon_str)
            source_y = float(lat_str)
            driver = Driver(requestTime=request_time, sourceX=source_x, sourceY=source_y)
            driver_queue.queue.append(driver)

    rider_queue = RiderQueue()
    # load the rider data
    with open("./data/passengers.csv", 'r') as file:
        next(file)  # Skip the header line
        while True:
            line = file.readline()
            if not line:
                break
            date_time_str, s_lat_str, s_lon_str, t_lat_str, t_lon_str = line.strip().split(',')
            request_time = datetime.strptime(date_time_str, '%m/%d/%Y %H:%M:%S')
            source_x = float(s_lon_str)
            source_y = float(s_lat_str)
            dest_x = float(t_lon_str)
            dest_y = float(t_lat_str)
            rider = Rider(requestTime=request_time, sourceX=source_x, sourceY=source_y, destX=dest_x, destY=dest_y)
            rider_queue.queue.append(rider)

    nodes = {}
    with open('./data/modified_node_data.json', 'r') as file:
        nodes_json = json.load(file)
        for node_id, node_latlon in nodes_json.items():
            nodes[int(node_id)] = (node_latlon['lon'], node_latlon['lat'])

    edges = []
    with open('./data/modified_edges.csv', 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        csv_reader.__next__()  # Skip the header row
        
        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Access the columns in the row
            start_id = int(row[0])
            end_id = int(row[1])
            length = float(row[2])
            weekdays_cost = [length/float(value) for value in row[3:27]]
            weekends_cost = [length/float(value) for value in row[27:]]

            edges.append((start_id, end_id, weekdays_cost, weekends_cost))

    print("finished loading data")

    adjacency_graph = defaultdict(lambda: defaultdict(dict))
    for start, end, weekdays_cost, weekends_cost in edges:
        adjacency_graph[start][end] = {
            "weekdays_cost": weekdays_cost,
            "weekends_cost": weekends_cost
        }
        adjacency_graph[end][start] = {
            "weekdays_cost": weekdays_cost,
            "weekends_cost": weekends_cost
        }


    return nodes, edges, adjacency_graph, driver_queue, rider_queue

### Nearest Node finder Implementation
class NearestNodeFinder:
    def __init__(self, nodes): 
        self.tree = KDTree(2)

        node_coordinates = []
        i = 0
        self.node_id_mapping = {}
        for node_id, (x, y) in nodes.items():
            node_coordinates.append((x, y))
            self.node_id_mapping[i] = node_id
            i += 1
        for i, node_coordinate in enumerate(node_coordinates):
            self.tree.insert(node_coordinate, i)
    
    def find_nearest_node(self, sourceX, sourceY, nodes):
        
        minDistance, (n_idx, _) = self.tree.find_min_distance([(sourceX, sourceY)])
        # print(self.node_id_mapping[n_idx], " has min distance ", minDistance)
        return self.node_id_mapping[n_idx] 


def a_star(start, goal, adj_graph, nodes) -> float:
    start = int(start)
    goal = int(goal)

    # Heuristic function (Euclidean distance)
    def heuristic(node1, node2):
        x1, y1 = nodes[node1]
        x2, y2 = nodes[node2]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # Initialize both open and closed sets
    open_set = []

    visited_dict = defaultdict(lambda: False)

    # push first node
    heappush(open_set, (0, start))

    # for path reconstruction
    came_from = {}

    # Cost from start node to itself is zero
    g_score = {node: float('inf') for node in nodes}
    g_score[start] = 0

    # heuristic store
    f_score = {node: float('inf') for node in nodes}
    f_score[start] = heuristic(start, goal)

    while open_set:

        # next node to expand
        current = heappop(open_set)[1]

        # if we found the goal, reconstruct the path and return it
        if current == goal:
            # # Reconstruct path
            # total_path = []
            # while current in came_from:
            #     total_path.append(current)
            #     current = came_from[current]
            # return (total_path[::-1], g_score[goal])  # Return reversed path
            return g_score[goal] # return cost

        # if not yet at goal...
        # investigate the adjacent nodes
        for neighbor in adj_graph[current]:
            
            tentative_g_score = g_score[current] + adj_graph[current][neighbor]['weekdays_cost'][0]  # Assuming graph[current][neighbor] is the distance to the neighbor

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                if visited_dict[neighbor] is False:
                    heappush(open_set, (f_score[neighbor], neighbor))
                    visited_dict[neighbor] = True

    return False  # Return False if there is no path