from lib import *
import math
import heapq
from datetime import datetime, timedelta


# Execute Ride Assignments

nodes, edges, adjacency_graph, driver_queue, rider_queue = load_data()

results = [[None for _ in range(len(driver_queue.queue))] for _ in range(len(rider_queue.queue))]
nnf = NearestNodeFinder(nodes)

for driver_idx, driver in enumerate(driver_queue.queue):
    for rider_idx, rider in enumerate(rider_queue.queue):
            
        driver = driver_queue.popLongestWaitingDriver()
        rider = rider_queue.popLongestWaitingRider()  # Corrected riderQueue to rider_queue

        driver_node = nnf.find_nearest_node(driver.sourceX, driver.sourceY, nodes)
        pickup_node = nnf.find_nearest_node(rider.sourceX, rider.sourceY, nodes)
        dropoff_node = nnf.find_nearest_node(rider.destX, rider.destY, nodes)

        # print(f"Assigning ride: Driver at Node {driver_node}, Pickup at Node {pickup_node}, Dropoff at Node {dropoff_node}")

        # Calculate travel times using A*
        pickup_duration = a_star(driver_node, pickup_node, adjacency_graph, nodes)
        dropoff_duration = a_star(pickup_node, dropoff_node, adjacency_graph, nodes)

        results[rider_idx][driver_idx] = {
            "driver": driver,
            "rider": rider,
            "time_to_pickup": pickup_duration,
            "time_to_dropoff": dropoff_duration,
        }
        print("result for driver {} and rider {}, {}".format(driver_idx, rider_idx, results[rider_idx][driver_idx]))

# Output the assignments and travel times for review
for assignment in ride_assignments:
    driver = assignment["driver"]
    rider = assignment["rider"]
    print(f"Driver at ({driver.sourceX}, {driver.sourceY}) assigned to Rider from ({rider.sourceX}, {rider.sourceY}) to ({rider.destX}, {rider.destY}) at {rider.requestTime}")
    print(f"Time to pickup: {assignment['time_to_pickup']} minutes, Time to dropoff: {assignment['time_to_dropoff']} minutes")