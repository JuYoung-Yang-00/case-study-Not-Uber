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
    for i in range(10):
        line = file.readline()
        if not line:
            break
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
    for i in range(10):
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
