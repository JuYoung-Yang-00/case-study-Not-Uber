# lib.py
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict
import json
import time
import heapq
import csv
from utils.findNearestVertex import *


# @dataclass
# class Driver:
#     requestTime: datetime
#     sourceX: float
#     sourceY: float
#     sourceVertexId: int

# @dataclass
# class Rider:
#     requestTime: datetime
#     sourceX: float
#     sourceY: float
#     destX: float
#     destY: float
#     sourceVertexId: int
#     destVertexId: int

# class DriverQueue:
#     def __init__(self):
#         self.queue: list[Driver] = []
    
#     def popLongestWaitingDriver(self):
#         self.queue.sort(key=lambda x: x.requestTime)
#         return self.queue.pop(0)

# class RiderQueue:
#     def __init__(self):
#         self.queue: list[Rider] = []

#     def popLongestWaitingRider(self):
#         self.queue.sort(key=lambda x: x.requestTime)
#         return self.queue.pop(0)
    
class Driver:
    def __init__(self, timestamp, lat, lon, driverLocationVertexID):
        self.timestamp = timestamp
        self.lat = lat
        self.lon = lon
        self.driverLocationVertexID = driverLocationVertexID
    
    def __lt__(self, other):
        # This method defines how drivers are compared
        # It's necessary for the heap to understand which driver comes first
        return self.timestamp < other.timestamp

    def __str__(self):
        return f"Driver(Timestamp: {self.timestamp}, Latitude: {self.lat}, Longitude: {self.lon}, Driver Location Vertex ID: {self.driverLocationVertexID})"

class Passenger:
    def __init__(self, timestamp, sourceLat, sourceLon, destLat, destLon, pickUpLocationVertexID, dropOffLocationVertexID):
        self.timestamp = timestamp
        self.sourceLat = sourceLat
        self.sourceLon = sourceLon
        self.destLat = destLat
        self.destLon = destLon
        self.pickUpLocationVertexID = pickUpLocationVertexID
        self.dropOffLocationVertexID = dropOffLocationVertexID

    
    def __lt__(self, other):
        # This method defines how passengers are compared
        # It's necessary for the heap to understand which passenger comes first
        return self.timestamp < other.timestamp

    def __str__(self):
        return f"Passenger(Timestamp: {self.timestamp}, Source Latitude: {self.sourceLat}, Source Longitude: {self.sourceLon}, Destination Latitude: {self.destLat}, Destination Longitude: {self.destLon}, Pick Up Location Vertex ID: {self.pickUpLocationVertexID}, Drop Off Location Vertex ID: {self.dropOffLocationVertexID})"


############ load data
def load_data(drivers_filepath: str, riders_filepath: str, nodes_filepath: str, edges_filepath: str, driver_count: int, passenger_count: int, nearest_node_finder: str):
    print("loading data")

    nodes = {}
    with open(nodes_filepath, 'r') as file:
        nodes_json = json.load(file)
        for node_id, node_latlon in nodes_json.items():
            nodes[int(node_id)] = (node_latlon['lon'], node_latlon['lat'])
    
    if nearest_node_finder == 'KDTree':
        nnf = NearestNodeFinder(nodes)
    
    data_loading_start = time.time()
    drivers = []
    heapq.heapify(drivers)  # Initialize an empty heap
    with open(drivers_filepath, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)  # Skip the header
        i = 0
        for row in csv_reader:
            timestamp = datetime.strptime(row[0], '%m/%d/%Y %H:%M:%S')
            lat = float(row[1])
            lon = float(row[2])
            if nearest_node_finder == 'naive':
                driverLocationVertexID = findNearestVertex(float(row[1]), float(row[2]), nodes_json)
            elif nearest_node_finder == 'KDTree':
                driverLocationVertexID = nnf.find_nearest_node(lon, lat, nodes)
            print(Driver(timestamp, lat, lon, driverLocationVertexID))
            # drivers.append(Driver(timestamp, lat, lon, driverLocationVertexID))
            heapq.heappush(drivers, Driver(timestamp, lat, lon, driverLocationVertexID))  # Add drivers to the heap
            i += 1
            if driver_count != -1 and i == driver_count:
                break
    print(f"drivers heap pq is loaded and is of length {len(drivers)}")

    passengers = []
    heapq.heapify(passengers)  # Initialize an empty heap
    with open(riders_filepath, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)  # Skip the header
        i = 0
        for row in csv_reader:
            timestamp = datetime.strptime(row[0], '%m/%d/%Y %H:%M:%S')
            sourceLat = float(row[1])
            sourceLon = float(row[2])
            destLat = float(row[3])
            destLon = float(row[4])
            if nearest_node_finder == 'naive':
                pickUpLocationVertexID = findNearestVertex(float(row[1]), float(row[2]), nodes_json)
                dropOffLocationVertexID = findNearestVertex(float(row[3]), float(row[4]), nodes_json)
            elif nearest_node_finder == 'KDTree':
                pickUpLocationVertexID = nnf.find_nearest_node(sourceLon, sourceLat, nodes)
                dropOffLocationVertexID = nnf.find_nearest_node(destLon, destLat, nodes)
            print(Passenger(timestamp, sourceLat, sourceLon, destLat, destLon, pickUpLocationVertexID, dropOffLocationVertexID))
            heapq.heappush(passengers, Passenger(timestamp, sourceLat, sourceLon, destLat, destLon, pickUpLocationVertexID, dropOffLocationVertexID))  # Add passengers to the heap
            i+=1
            if passenger_count != -1 and i == passenger_count:
                break
    print(f"passengers heap pq is loaded and is of length {len(passengers)}")

    data_loading_end = time.time()
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

    data_loading_time = data_loading_end - data_loading_start
    return nodes, edges, adjacency_graph, drivers, passengers, data_loading_time