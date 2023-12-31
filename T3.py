from utils.Preprocessing.AllDataLoader import load_data
from utils.SearchAlgo.ShortestPathAlgos import a_star
from utils.execute_ride import *
import time
from datetime import timedelta, datetime
from utils.Preprocessing.load_drivers import *
from utils.Preprocessing.load_passengers import *
from utils.summarizeResult import *
import random


vertex_count = 2000
# 1. get nodes, edges, adjaceny graph, driver & passenger heap using a naive nearest vertex finder 
algo_start_time = time.time()
nodes, edges, adjacency_graph, driversHeap_PQ, passengersHeap_PQ, data_loading_time = load_data('data/drivers.csv', 'data/passengers.csv', f"data/modified_node_data_{vertex_count}.json", f'data/modified_edges_{vertex_count}.csv', -1, -1, 'naive')
matching_start_time = time.time() 


# 2. get nodes, edges, adjaceny graph 
# nodes, edges, adjacency_graph, driversHeap_PQ, passengersHeap_PQ = load_data('data/drivers.csv', 'data/passengers.csv', f"data/node_data.json", f'data/edges.csv', 100, 300, 'naive')
# 3. initializing metricsRecorded, which we'll use to talk about efficiency in the .pdf report we'll submit on Gradescope or something
metricsRecorded = []

def matchPassengerAndDrivers(passenger_heap_pq, driver_heap_pq, current_unmatched):
    """
    returns a list of passengers and drivers that are matched at the "current time"
    this function is triggered for every new passenger request
    
    A Note on 'current_unmatched':
    - Suppose there's a passenger who can't find a match (there's more passengers than there are drivers available)
    - These passengers will be added back to the passenger heap, but this means next time the heap is popped we will retrieve the same passenger... and find no match
    - current_unmatched allows us to effectively query the next passenger who requests a ride by adding 1 to the total number of unmatched passengers from the previous function call.
    - for current_unmatched > 1 we thus consider the newest passenger request as well as all passenger requests previously left unmatched. 
   
    Paramaters
    ---------
    passenger_heap_pq: list/heap
        a heapified list of passengers 
    driver_heap_pq: list/heap
        a heapified list of drivers 
    current_unmatched: int
        number of unmatched passengers to consider at this timestamp
    """

    ## pop passengers based on number of passengers unmatched at current timestamp, add to list
    avail_passengers = []
    for i in range(min(current_unmatched, len(passenger_heap_pq))):
        avail_passenger = heapq.heappop(passenger_heap_pq)
        avail_passengers.append(avail_passenger)
    ## passenger with latest timestamp => newest request => "current time"
    current_timestamp = max([passenger.timestamp for passenger in avail_passengers])
    print("Time Right Now: ", current_timestamp)
    ## find available drivers based on the current time  
    avail_drivers = find_availability(driver_heap_pq, current_timestamp)
    ## no drivers available at the moment, but all remaining passengers are unmatched <== we revert to matching them to the next N drivers
    if len(avail_drivers) == 0 and len(passenger_heap_pq) < current_unmatched: 
        avail_drivers = heapq.nsmallest(len(passenger_heap_pq), driver_heap_pq)
        len(avail_passengers)
        len(avail_drivers)
    ## find estimated time between each passenger <> driver pair
    times = find_time(avail_drivers, avail_passengers, nodes, edges, adjacency_graph)
    ## find as many passenger <> driver pairs with smallest pickup time between them
    passengerAndDrivers = find_matches(avail_drivers, avail_passengers, times)
    ## any unmatched drivers? add them back to original heap
    for unmatched_driver in avail_drivers:
        heapq.heappush(driver_heap_pq, unmatched_driver)
    ## any unmatched passengers? add them back to original heap
    for unmatched_passsenger in avail_passengers:
        heapq.heappush(passenger_heap_pq, unmatched_passsenger)
    ## we want to also consider these unmatched passengers in the next timestamp, so we their count to current_unmatched 
    current_unmatched = 1+len(avail_passengers)
    return passengerAndDrivers, current_unmatched
    
## THE T3 ALGO
def T3(passengersHeap_PQ, driversHeap_PQ, metricsRecorded):
    # passengersHeap_PQ, driversHeap_PQ, graphs, and metricsRecorded is already initialized
    n = 0 ## # matches
    current_unmatched = 1 ## initialize current_unmatched
    while (passengersHeap_PQ): #is not empty
        print("STARTING THIS MATCHING ROUND")
        print("Passengers Left: ", len(passengersHeap_PQ))
        print("Drivers Left: ", len(driversHeap_PQ))
        print("Number of Passengers Available for Match: ", current_unmatched)
        ## match passenger and driver, retrieve list
        passengerAndDrivers, current_unmatched = matchPassengerAndDrivers(passengersHeap_PQ, driversHeap_PQ, current_unmatched)
        print("Number of Passenger/Drivers Actually Matched: ", len(passengerAndDrivers))
        ## for each pair, execute ride
        for pair in passengerAndDrivers:
            rideResult = T3_executeRide(pair, metricsRecorded)
            metricsRecorded = rideResult[0]
            continuing_drivers = rideResult[1]
            n = n+1
            if continuing_drivers is not None:
                heapq.heappush(driversHeap_PQ, continuing_drivers)
                print("a driver got added back to driver heap pq")
        print(f"{n} rides executed thus far")

    # now that passengersHeap_PQ is empty, 
    print(metricsRecorded)
    return metricsRecorded

## Helper function to find available drivers
def find_availability(drivers, timestamp):
    avail_drivers = []
    while True and len(drivers) != 0:
        ## pop potential matching driver
        candidate_driver = heapq.heappop(drivers)
        ## driver has timestamp less than or equal to current timestamp 
        if candidate_driver.timestamp <= timestamp:
            ## push to list of drivers
            avail_drivers.append(candidate_driver)
        else: 
            ## candidate driver is available after current time, add back to list; heaps are sorted by time, we can break
            heapq.heappush(drivers, candidate_driver)
            break 
    return avail_drivers

def find_time(drivers, passengers, nodes, edges, adjacency_graph):
    times = []
    heapq.heapify(times)
    ## for each passenger
    for passenger in passengers:
        ## get their coordinate
        pickup_node = passenger.pickUpLocationVertexID
        dropoff_node = passenger.dropOffLocationVertexID
        ## for each driver
        for driver in drivers:
            ## get their coordinate
            driver_node = driver.driverLocationVertexID
            # find the current time index - taking the later of the driver or rider.
            time_index = time_to_integer(max(driver.timestamp, passenger.timestamp))
            # Calculate travel times using dijkstra 
            pickup_duration = a_star(driver_node, pickup_node, adjacency_graph, nodes, time_index)
            dropoff_duration = a_star(pickup_node, dropoff_node, adjacency_graph, nodes, time_index)
            ## add to min heap
            heapq.heappush(times, (pickup_duration,(passenger, driver, dropoff_duration)))
    return times


def find_matches(avail_drivers, avail_passengers, times):
    passengerAndDrivers = []
    while avail_drivers and avail_passengers:
        ## pop the minimum pickup duration pair
        min_times = heapq.heappop(times)
        ## information about pair
        pickup_duration = min_times[0]
        dropoff_duration = min_times[1][2]
        passenger = min_times[1][0]
        driver = min_times[1][1]
        ## the driver passenger pair is valid (BOTH are still available)
        if passenger in avail_passengers and driver in avail_drivers:
            ## well now they're not available!
            avail_passengers.remove(passenger)
            avail_drivers.remove(driver)
            ## add them to return list
            passengerAndDrivers.append([passenger, driver,pickup_duration,dropoff_duration])
    return passengerAndDrivers

def time_to_integer(dt):
    # Check if the date is a weekend (Saturday or Sunday)
    if dt.weekday() >= 5:  # 5 for Saturday, 6 for Sunday
        return 24 + dt.hour
    else:
        return dt.hour

simulation = T3(passengersHeap_PQ, driversHeap_PQ, metricsRecorded)
end_time = time.time()
total_time = end_time - algo_start_time
matching_time = end_time - matching_start_time
summarizeResult(simulation, 'T3')
print('Time for Data to Load: ', data_loading_time)
print('Time for Matching Algorithm: ', matching_time)
print('ALGORITHM ENDED, TIME ELAPSED: ', total_time)
