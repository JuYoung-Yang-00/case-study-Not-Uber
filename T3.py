from utils.NearestNodeFinder import NearestNodeFinder
from utils.Preprocessing.AllDataLoader import load_data
from utils.SearchAlgo.PkShortestPathAlgos import dijkstra, a_star
import time
from datetime import timedelta, datetime

from utils.pkFindNearestVertex import findNearestVertex


def time_to_integer(dt):
    # Check if the date is a weekend (Saturday or Sunday)
    if dt.weekday() >= 5:  # 5 for Saturday, 6 for Sunday
        return 24 + dt.hour
    else:
        return dt.hour

'''
Finds the shortest passenger wait time.
- Uses iterative O(n) algorithm to find the closest vertex to each driver and rider-pickup, rider-destination
- Uses Dijkstra O( V+E logV) algorithm to find the traversal path from driver to rider-pickup
'''

def matching(driver_queue, rider_queue, nodes, edges, adjacency_graph):


    results = [[None for _ in range(len(driver_queue.queue))] for _ in range(len(rider_queue.queue))]

    # do matching for first n_drivers and first n_riders
    for rider_idx, rider in enumerate(rider_queue.queue):
        for driver_idx, driver in enumerate(driver_queue.queue):

            # get nearest vertex for the driver, rider pickup and rider destination
            driver_node = driver.sourceVertexId
            pickup_node = rider.sourceVertexId
            dropoff_node = rider.destVertexId

            # find the current time index - taking the later of the driver or rider.
            time_index = time_to_integer(max(driver.requestTime, rider.requestTime))

            # Calculate travel times using dijkstra 
            pickup_duration = a_star(driver_node, pickup_node, adjacency_graph, nodes, time_index)
            dropoff_duration = a_star(pickup_node, dropoff_node, adjacency_graph, nodes, time_index)

            # store the results in the 2-d array of results
            results[rider_idx][driver_idx] = (driver, rider, pickup_duration, dropoff_duration, driver_node, pickup_node, dropoff_node)
            print(f"for rider {rider_idx}, driver {driver_idx} of {len(driver_queue.queue)}")
        
    return results

# Run for vertex count 1000, 2000, ..., 10000
for vertex_count in range(1000,30000,1000):

    # load data
    nodes, edges, adjacency_graph, driver_queue, rider_queue = load_data('data/drivers.csv', 'data/passengers.csv', f"data/node_data.json", f'data/edges.csv')

    # use 0-10 for testing
    driver_queue.queue = driver_queue.queue[0:5]
    rider_queue.queue = rider_queue.queue[0:5]
    print("calculating nearest verticies from drivers and riders...")

    nnf = NearestNodeFinder(nodes)

    # precompute nearest verticies for all drivers, riders
    for i in range(len(driver_queue.queue)):
        x = driver_queue.queue[i].sourceX
        y = driver_queue.queue[i].sourceY
        driver_queue.queue[i].sourceVertexId = nnf.find_nearest_node(x, y, nodes)

    for i in range(len(rider_queue.queue)):
        x = rider_queue.queue[i].sourceX
        y = rider_queue.queue[i].sourceY
        rider_queue.queue[i].sourceVertexId = nnf.find_nearest_node(x, y, nodes)
        x = rider_queue.queue[i].destX
        y = rider_queue.queue[i].destY
        rider_queue.queue[i].destVertexId = nnf.find_nearest_node(x, y, nodes)

    # 2-D array to store driver rider match results

    # start measuring time
    start_time = time.time()

    # full matching results
    results = matching(driver_queue=driver_queue, rider_queue=rider_queue, nodes=nodes, edges=edges, adjacency_graph=adjacency_graph)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"vertex_count: {vertex_count}, {elapsed_time} seconds to complete.")

    # flatten the results array
    results = [item for sublist in results for item in sublist]
    
    # the best driver for this rider, is the one with the shortest pickup duration
    results.sort(key=lambda x: x[2])

    for result in results:

        best_driver, for_rider, pickup_duration, dropoff_duration, driver_node, pickup_node, dropoff_node = result

        # Find the later of the two request times
        latest_request_time = max(for_rider.requestTime, best_driver.requestTime)

        # Convert pickup_duration and dropoff_duration from minutes to timedelta
        pickup_duration_timedelta = timedelta(minutes=pickup_duration)
        dropoff_duration_timedelta = timedelta(minutes=dropoff_duration)

        # Calculate total rider duration
        rider_dropoff_time = latest_request_time + pickup_duration_timedelta + dropoff_duration_timedelta
        total_rider_duration = (rider_dropoff_time - for_rider.requestTime).total_seconds() / 60

        print(f"rider {for_rider.requestTime} to {best_driver.requestTime} with dropoff-time - pickup-time: {(dropoff_duration - pickup_duration)*60} minutes; total rider time: {total_rider_duration}; {driver_node} -> {pickup_node} -> {dropoff_node}")

