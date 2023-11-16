# T1.py
from lib import *
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
    return nearest_node

def euclidean_distance(node_id1, node_id2, nodes):
    x1, y1 = nodes[node_id1]['lat'], nodes[node_id1]['lon']
    x2, y2 = nodes[node_id2]['lat'], nodes[node_id2]['lon']
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

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
    total_time_to_pickup = 0
    total_drive_time = 0
    total_wait_and_drive_time = 0
    total_driver_drive_time = 0
    num_rides = 0

    while driver_queue.queue and rider_queue.queue:
        driver = driver_queue.popLongestWaitingDriver()
        rider = rider_queue.popLongestWaitingRider()

        driver_node = find_nearest_node(driver.sourceX, driver.sourceY, nodes)
        pickup_node = find_nearest_node(rider.sourceX, rider.sourceY, nodes)
        dropoff_node = find_nearest_node(rider.destX, rider.destY, nodes)

        # Calculate travel times using A*
        time_to_pickup = a_star(driver_node, pickup_node, graph, driver.requestTime, nodes)
        time_to_dropoff = a_star(pickup_node, dropoff_node, graph, rider.requestTime, nodes)

        wait_time = (rider.requestTime - driver.requestTime).total_seconds() / 60
        total_drive_time += time_to_dropoff
        total_time_to_pickup += time_to_pickup
        total_wait_and_drive_time += wait_time + time_to_dropoff
        total_driver_drive_time += time_to_dropoff - time_to_pickup

        num_rides += 1

        results.append({
            "driver": driver,
            "rider": rider,
            "time_to_pickup": time_to_pickup,
            "time_to_dropoff": time_to_dropoff
        })

    average_time_to_pickup = total_time_to_pickup / num_rides if num_rides > 0 else 0
    average_drive_time = total_drive_time / num_rides if num_rides > 0 else 0
    average_total_time = total_wait_and_drive_time / num_rides if num_rides > 0 else 0
    average_driver_drive_time = total_driver_drive_time / num_rides if num_rides > 0 else 0

    return results, average_time_to_pickup, average_drive_time, average_total_time, average_driver_drive_time

# Execute Ride Assignments
ride_assignments, avg_time_to_pickup, avg_drive_time, avg_total_time, avg_driver_drive_time = assign_rides_and_calculate_paths(driverQueue, riderQueue, graph, nodes)

# Output the assignments and travel times for review
for assignment in ride_assignments:
    driver = assignment["driver"]
    rider = assignment["rider"]
    print(f"Driver at ({driver.sourceX}, {driver.sourceY}) assigned to Rider from ({rider.sourceX}, {rider.sourceY}) to ({rider.destX}, {rider.destY}) at {rider.requestTime}")
    print(f"Time to pickup: {assignment['time_to_pickup']} minutes, Time to dropoff: {assignment['time_to_dropoff']} minutes")

# Print the averages
print(f"\nAverage Times:")
print(f"Average time for passengers to be picked up: {avg_time_to_pickup} minutes")
print(f"Average drive time for passengers: {avg_drive_time} minutes")
print(f"Average total time for passengers (waiting to dropped off): {avg_total_time} minutes")
print(f"Average drive time for drivers (from passenger pickup to dropoff): {avg_driver_drive_time} minutes")
