# T1.py
from utils.Preprocessing.lib import *
import math
import heapq
from datetime import datetime, timedelta

# Helper Functions
def calculate_euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def find_nearest_node(lat, lon, nodes):
    min_distance = float('inf')
    nearest_node = None

    for node_id, node_info in nodes.items():
        distance = calculate_euclidean_distance((lat, lon), (node_info['lat'], node_info['lon']))
        if distance < min_distance:
            min_distance = distance
            nearest_node = node_id
    nearest_node = str(nearest_node)
    print(f"Nearest node to ({lat}, {lon}) is {nearest_node} with distance {min_distance}")
    
    return nearest_node

def euclidean_distance(node_id1, node_id2, nodes):
    x1, y1 = nodes[node_id1]['lat'], nodes[node_id1]['lon']
    x2, y2 = nodes[node_id2]['lat'], nodes[node_id2]['lon']
    res = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    # print(f"The calculated euclidean distance from node {node_id1} to node {node_id2} is {res}")
    return res

def a_star(start_id, target_id, graph, start_time, nodes):
    open_set = []
    heapq.heappush(open_set, (0, start_id, start_time, 0))
    came_from = {}
    g_score = {node: float('inf') for node in nodes}
    g_score[start_id] = 0

    while open_set:
        _, current, current_time, current_g = heapq.heappop(open_set)

        if current == target_id:
            return current_g

        if current not in graph:
            continue

        for neighbor_data in graph[current]:
            neighbor_id, _, _ = neighbor_data
            edge_weight = get_edge_weight(current_time, neighbor_data)
            if edge_weight is None:  
                continue

            tentative_g_score = current_g + edge_weight
            if tentative_g_score < g_score.get(neighbor_id, float('inf')):
                came_from[neighbor_id] = current
                g_score[neighbor_id] = tentative_g_score
                new_time = current_time + timedelta(minutes=edge_weight)
                f_score = tentative_g_score + euclidean_distance(neighbor_id, target_id, nodes)
                heapq.heappush(open_set, (f_score, neighbor_id, new_time, tentative_g_score))

    return float('inf')


# Assigning Rides and Calculating Path
def assign_rides_and_calculate_paths(driver_queue, rider_queue, graph, nodes):
    results = []

    while driver_queue.queue and rider_queue.queue:
        driver = driver_queue.popLongestWaitingDriver()
        rider = rider_queue.popLongestWaitingRider()  # Corrected riderQueue to rider_queue

        driver_node = find_nearest_node(driver.sourceX, driver.sourceY, nodes)
        pickup_node = find_nearest_node(rider.sourceX, rider.sourceY, nodes)
        dropoff_node = find_nearest_node(rider.destX, rider.destY, nodes)

        print(f"Assigning ride: Driver at Node {driver_node}, Pickup at Node {pickup_node}, Dropoff at Node {dropoff_node}")

        # Calculate travel times using A*
        time_to_pickup = a_star(driver_node, pickup_node, graph, driver.requestTime, nodes)
        time_to_dropoff = a_star(pickup_node, dropoff_node, graph, rider.requestTime, nodes)

        results.append({
            "driver": driver,
            "rider": rider,
            "time_to_pickup": time_to_pickup,
            "time_to_dropoff": time_to_dropoff
        })

    return results

# Execute Ride Assignments
ride_assignments = assign_rides_and_calculate_paths(driverQueue, riderQueue, graph, nodes)

# Output the assignments and travel times for review
for assignment in ride_assignments:
    driver = assignment["driver"]
    rider = assignment["rider"]
    print(f"Driver at ({driver.sourceX}, {driver.sourceY}) assigned to Rider from ({rider.sourceX}, {rider.sourceY}) to ({rider.destX}, {rider.destY}) at {rider.requestTime}")
    print(f"Time to pickup: {assignment['time_to_pickup']} minutes, Time to dropoff: {assignment['time_to_dropoff']} minutes")
