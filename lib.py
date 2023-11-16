# lib.py
from datetime import datetime
import json
import csv
from dataclasses import dataclass
from datetime import datetime

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

driverQueue = DriverQueue()
# load the driver data
with open("./data/drivers.csv", 'r') as file:
    next(file)  # Skip the header line
    while True:
        line = file.readline()
        if not line:
            break  # Break the loop if no more data
        date_time_str, lat_str, lon_str = line.strip().split(',')
        request_time = datetime.strptime(date_time_str, '%m/%d/%Y %H:%M:%S')
        source_x = float(lat_str)
        source_y = float(lon_str)
        driver = Driver(requestTime=request_time, sourceX=source_x, sourceY=source_y)
        driverQueue.queue.append(driver)

riderQueue = RiderQueue()
# load the rider data
with open("./data/passengers.csv", 'r') as file:
    next(file)  # Skip the header line
    while True:
        line = file.readline()
        if not line:
            break
        date_time_str, s_lat_str, s_lon_str, t_lat_str, t_lon_str = line.strip().split(',')
        request_time = datetime.strptime(date_time_str, '%m/%d/%Y %H:%M:%S')
        source_x = float(s_lat_str)
        source_y = float(s_lon_str)
        dest_x = float(t_lat_str)
        dest_y = float(t_lon_str)
        rider = Rider(requestTime=request_time, sourceX=source_x, sourceY=source_y, destX=dest_x, destY=dest_y)
        riderQueue.queue.append(rider)

nodes = {}
with open('./data/node_data.json', 'r') as file:
    nodes = json.load(file)

edges = []
with open('./data/edges.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    csv_reader.__next__()  # Skip the header row
    
    # Iterate through each row in the CSV file
    for row in csv_reader:
        # Access the columns in the row
        start_id = int(row[0])
        end_id = int(row[1])
        length = float(row[2])
        weekdays = [float(value) for value in row[3:27]]
        weekends = [float(value) for value in row[27:]]

        edges.append((start_id, end_id, length, weekdays, weekends))



# import math
# import heapq
# from datetime import timedelta

# def calculate_travel_times(length, speeds):
#     return [length / speed if speed != 0 else float('inf') for speed in speeds]

# graph = {}

# for start, end, length, weekdays, weekends in edges:
#     start_str, end_str = str(start), str(end)
#     forward_weekday_times = calculate_travel_times(length, weekdays[:24])
#     forward_weekend_times = calculate_travel_times(length, weekends[:24])

#     if start_str not in graph:
#         graph[start_str] = []
#     graph[start_str].append((end_str, forward_weekday_times, forward_weekend_times))

#     reverse_weekday_times = calculate_travel_times(length, weekdays[24:])
#     reverse_weekend_times = calculate_travel_times(length, weekends[24:])

#     if end_str not in graph:
#         graph[end_str] = []
#     graph[end_str].append((start_str, reverse_weekday_times, reverse_weekend_times))

# print(f"Total number of nodes in the graph: {len(graph)}")

# def get_edge_weight(current_time, edge):
#     neighbor_id, weekday_times, weekend_times = edge
#     hour = current_time.hour


#     if current_time.weekday() < 5:  # Weekday
#         if hour < len(weekday_times):
#             travel_time = weekday_times[hour]
#         else:
#             return None  # Safeguard against index out of range
#     else:  # Weekend
#         if hour < len(weekend_times):
#             travel_time = weekend_times[hour]
#         else:
#             return None  # Safeguard against index out of range

#     return travel_time if travel_time != float('inf') else None



# print("Complete Graph:")
# for node, edges in graph.items():
#     print(f"Node {node}: {edges}")

# def check_bidirectional_edges(graph):
#     missing_edges = []
#     for start_node, edges in graph.items():
#         for edge in edges:
#             end_node = edge[0]
#             reverse_edge_found = False
#             for reverse_edge in graph.get(end_node, []):
#                 if reverse_edge[0] == start_node:
#                     reverse_edge_found = True
#                     break
#             if not reverse_edge_found:
#                 missing_edges.append((start_node, end_node))
#     return missing_edges

# # Check for missing edges after constructing the graph
# missing_edges = check_bidirectional_edges(graph)
# if missing_edges:
#     print("Missing reverse edges:", missing_edges)
# else:
#     print("All edges are bidirectional.")



