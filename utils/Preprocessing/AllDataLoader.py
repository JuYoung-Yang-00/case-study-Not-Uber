# lib.py
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict
import json
import csv

@dataclass
class Driver:
    requestTime: datetime
    sourceX: float
    sourceY: float
    sourceVertexId: int

@dataclass
class Rider:
    requestTime: datetime
    sourceX: float
    sourceY: float
    destX: float
    destY: float
    sourceVertexId: int
    destVertexId: int

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
def load_data(drivers_filepath: str, riders_filepath: str, nodes_filepath: str, edges_filepath: str):
    print("loading data")

    driver_queue = DriverQueue()
    # load the driver data
    with open(drivers_filepath, 'r') as file:
        next(file)  # Skip the header line
        while True:
            line = file.readline()
            if not line:
                break  # Break the loop if no more data
            date_time_str, lat_str, lon_str = line.strip().split(',')
            request_time = datetime.strptime(date_time_str, '%m/%d/%Y %H:%M:%S')
            source_x = float(lon_str)
            source_y = float(lat_str)
            driver = Driver(requestTime=request_time, sourceX=source_x, sourceY=source_y, sourceVertexId=None)
            driver_queue.queue.append(driver)

    rider_queue = RiderQueue()
    # load the rider data
    with open(riders_filepath, 'r') as file:
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
            rider = Rider(requestTime=request_time, sourceX=source_x, sourceY=source_y, destX=dest_x, destY=dest_y, destVertexId=None, sourceVertexId=None)
            rider_queue.queue.append(rider)

    nodes = {}
    with open(nodes_filepath, 'r') as file:
        nodes_json = json.load(file)
        for node_id, node_latlon in nodes_json.items():
            nodes[int(node_id)] = (node_latlon['lon'], node_latlon['lat'])

    edges = []
    with open(edges_filepath, 'r') as file:
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