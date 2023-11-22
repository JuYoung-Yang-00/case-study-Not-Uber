import csv
from datetime import datetime
import heapq

import json

from utils.findNearestVertex import *



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



# Load your node data from JSON file
with open('./data/node_data.json', 'r') as f:
    node_data = json.load(f)


def read_passengers_csv(file_name, count):
    passengers = []
    heapq.heapify(passengers)  # Initialize an empty heap
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)  # Skip the header
        i = 0
        for row in csv_reader:
            timestamp = datetime.strptime(row[0], '%m/%d/%Y %H:%M:%S')
            sourceLat = float(row[1])
            sourceLon = float(row[2])
            destLat = float(row[3])
            destLon = float(row[4])
            pickUpLocationVertexID = findNearestVertex(float(row[1]), float(row[2]), node_data)
            dropOffLocationVertexID = findNearestVertex(float(row[3]), float(row[4]), node_data)
            print(Passenger(timestamp, sourceLat, sourceLon, destLat, destLon, pickUpLocationVertexID, dropOffLocationVertexID))
            heapq.heappush(passengers, Passenger(timestamp, sourceLat, sourceLon, destLat, destLon, pickUpLocationVertexID, dropOffLocationVertexID))  # Add passengers to the heap
            i+=1
            if i == count:
                break

    print(f"passengers heap pq is loaded and is of length {len(passengers)}")
    return passengers