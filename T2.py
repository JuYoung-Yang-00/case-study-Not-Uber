from utils.Preprocessing.load_drivers import *
from utils.Preprocessing.load_passengers import *
from utils.Preprocessing.createGraph import *
from utils.execute_ride import *
from utils.summarizeResult import *
from utils.SearchAlgo.djikstra import *
from utils.findNearestVertex import euclidean_distance


# 1. load data and initialize passenger priority queue and driver priority queue using loading_drivers_and_passengers.py)
passengersHeap_PQ = read_passengers_csv('./data/passengers.csv')
driversHeap_PQ = read_drivers_csv('./data/drivers.csv')

#2. load the graph
graphToUse = createGraph()

# 3. initializing metricsRecorded, which we'll use to talk about efficiency in the .pdf report we'll submit on Gradescope or something
metricsRecorded = [] # each item in metricsRecorded should contain a list that is: [timeItTookForDriverToGetToPassenger, timeItTookFromPickupToDropoff, timeItTookForPassengerToGoFromUnmatchedToDroppedOff]

def matchPassengerAndDrivers(passenger_heap_pq, driver_heap_pq, current_unmatched):
    """
    returns a list of passengers and drivers that are matched at the "current time"
    this function is triggered for every new passenger request
    
    A Note on 'current_unmatched':
    - Suppose there's a passenger who can't find a match (there's more passengers than there are drivers available)
    - These passengers will be added back to the passenger heap, but this means next time the heap is popped we will retrieve the same passenger... and find no match
    - current_unmatched allows us to effectiely query the next passenger who requests a ride by adding 1 to the total number of unmatched passengers from the previous function call.
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
    for i in range(current_unmatched):
        avail_passenger = heapq.heappop(passenger_heap_pq)
        avail_passengers.append(avail_passenger)
    ## passenger with latest timestamp => newest request => "current time"
    current_timestamp = avail_passengers[-1].timestamp
    ## find available drivers based on the current time  
    avail_drivers = find_availability(driver_heap_pq, current_timestamp)
    ## find Euclidean distance between each passenger <> driver pair
    distances = find_distances(avail_drivers, avail_passengers)
    ## find passenger <> driver pairs with smallest Euclidean distance between them
    passengerAndDrivers = find_matches(avail_drivers, avail_passengers, distances)
    ## any unmatched drivers? add them back to original heap
    for unmatched_driver in avail_drivers:
        heapq.heappush(driver_heap_pq, unmatched_driver)
    ## any unmatched passengers? add them back to original heap
    for unmatched_passsenger in avail_passengers:
        heapq.heappush(passenger_heap_pq, unmatched_passsenger)
    ## we want to also consider these unmatched passengers in the next timestamp so we add this to current_unmatched 
    current_unmatched = 1+len(avail_passengers)
    ## if all passengers were matched then we only have to consider the next request. 
    return passengerAndDrivers, current_unmatched
    
## THE T2 ALGO
def T2(passengersHeap_PQ, driversHeap_PQ):
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
            executeRide(pair, graphToUse, metricsRecorded, driversHeap_PQ)
            n = n+1
        print(f"{n} rides executed thus far")
    
    # now that passengersHeap_PQ is empty, 
    print(metricsRecorded)
    return metricsRecorded

## Helper function to find available drivers
def find_availability(drivers, timestamp):
    avail_drivers = []
    while True:
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

## Helper function to compute distances between passenger <> driver pair
def find_distances(drivers, passengers):
    distances = []
    heapq.heapify(distances)
    ## for each passenger
    for passenger in passengers:
        ## get their coordinate
        passenger_coord = (passenger.sourceLat, passenger.sourceLon)
        ## for each driver
        for driver in drivers:
            ## get their coordinate
            driver_coord = (driver.lat, driver.lon)
            # find their euclidean distance
            distance = euclidean_distance(passenger_coord[1], passenger_coord[0], driver_coord[1], driver_coord[0])
            ## add to min heap
            heapq.heappush(distances, (distance,(passenger, driver)))
    return distances

## Helper function to find passenger <> driver pairs with minimum straight-line distance
def find_matches(avail_drivers, avail_passengers, distances):
    passengerAndDrivers = []
    while avail_drivers and avail_passengers:
        ## pop the minimum distance pair
        min_distance = heapq.heappop(distances)
        passengerDriverPair = min_distance[1]
        ## the driver passenger pair is valid (BOTH are still available)
        if passengerDriverPair[0] in avail_passengers and passengerDriverPair[1] in avail_drivers:
            ## well now they're not available!
            avail_passengers.remove(passengerDriverPair[0])
            avail_drivers.remove(passengerDriverPair[1])
            ## add them to return list
            passengerAndDrivers.append([passengerDriverPair[0], passengerDriverPair[1]])
    return passengerAndDrivers

simulation, n, starting_number = T2(passengersHeap_PQ, driversHeap_PQ)
print(len(simulation), n, starting_number)
summarizeResult(simulation, 'T2')