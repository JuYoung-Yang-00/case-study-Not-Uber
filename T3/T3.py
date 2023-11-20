from dataloader import load_data
from ShortestPath import dijkstra
from findNearestVertex import findNearestVertex
import time

'''
Finds the shortest passenger wait time.
- Uses iterative O(n) algorithm to find the closest vertex to each driver and rider-pickup, rider-destination
- Uses Dijkstra O( V+E logV) algorithm to find the traversal path from driver to rider-pickup
'''

# Run for vertex count 1000, 2000, ..., 10000
for vertex_count in range(1000,30000,1000):

    # load data
    nodes, edges, adjacency_graph, driver_queue, rider_queue = load_data('data/drivers.csv', 'data/passengers.csv', f"data/modified_node_data_{vertex_count}.json", f'data/modified_edges_{vertex_count}.csv')

    # 2-D array to store driver rider match results
    n_drivers = 10 
    n_riders = 10
    results = [[None for _ in range(n_drivers)] for _ in range(n_riders)]

    # start measuring time
    start_time = time.time()

    # do matching for first n_drivers and first n_riders
    for driver_idx, driver in enumerate(driver_queue.queue[0:n_drivers]):
        for rider_idx, rider in enumerate(rider_queue.queue[0:n_riders]):

            # find nearest vertex for the driver, rider pickup and rider destination
            driver_node = findNearestVertex(driver.sourceX, driver.sourceY, nodes)
            pickup_node = findNearestVertex(rider.sourceX, rider.sourceY, nodes)
            dropoff_node = findNearestVertex(rider.destX, rider.destY, nodes)

            # Calculate travel times using dijkstra 
            pickup_duration = dijkstra(driver_node, pickup_node, adjacency_graph)
            dropoff_duration = dijkstra(pickup_node, dropoff_node, adjacency_graph)

            # store the results in the 2-d array of results
            results[rider_idx][driver_idx] = (driver, rider, pickup_duration)
        
        # print("driver {} of {}".format(driver_idx, n_drivers-1))

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"vertex_count: {vertex_count}, driver count: {n_drivers}, rider count: {n_riders}, {elapsed_time} seconds to complete.")

# Output the assignments and travel times for review
# for results_row in results:
#     for result in results_row:
#         print(result)
