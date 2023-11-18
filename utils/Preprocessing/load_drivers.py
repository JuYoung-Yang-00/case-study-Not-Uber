import csv
from datetime import datetime
import heapq

from utils.findNearestVertex import *

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




# Load your node data from JSON file
with open('./data/node_data.json', 'r') as f:
    node_data = json.load(f)

def read_drivers_csv(file_name):
    drivers = []
    heapq.heapify(drivers)  # Initialize an empty heap
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)  # Skip the header
        for row in csv_reader:
            timestamp = datetime.strptime(row[0], '%m/%d/%Y %H:%M:%S')
            lat = float(row[1])
            lon = float(row[2])
            driverLocationVertexID = findNearestVertex(float(row[1]), float(row[2]), node_data)
            print(Driver(timestamp, lat, lon, driverLocationVertexID))
            heapq.heappush(drivers, Driver(timestamp, lat, lon, driverLocationVertexID))  # Add drivers to the heap
    print(f"drivers heap pq is loaded and is of length {len(drivers)}")
    return drivers