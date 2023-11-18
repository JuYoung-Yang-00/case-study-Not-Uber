from utils.Preprocessing.load_drivers import *
from utils.Preprocessing.load_passengers import *
from utils.Preprocessing.createGraph import *
from utils.execute_ride import *
from utils.summarizeResult import *
from utils.SearchAlgo.djikstra import *


# HELPER FUNCTION
def matchAPassengerAndDriver(passenger_heap_pq, driver_heap_pq):
    longestWaitingPassenger = heapq.heappop(passenger_heap_pq)
    matchedDriver = heapq.heappop(driver_heap_pq)
    '''
    tempDrivers = []  # To store drivers temporarily
    matchedDriver = None
    while driver_heap_pq and not matchedDriver:
        firstAvailableDriver = heapq.heappop(driver_heap_pq)
        if longestWaitingPassenger.timestamp <= firstAvailableDriver.timestamp:
            matchedDriver = firstAvailableDriver
        else:
            tempDrivers.append(firstAvailableDriver)

    # Push back the drivers that were popped out
    for driver in tempDrivers:
        heapq.heappush(driver_heap_pq, driver)
    '''

    if matchedDriver:
        print(len(passenger_heap_pq)) #should be 5001 after the very first match
        print(len(driver_heap_pq)) #should be 498 after the very first math
        toReturn = [longestWaitingPassenger, matchedDriver]
        #print(toReturn)
        return toReturn
    else:
        # Re-insert the passenger if no matching driver is found
        heapq.heappush(passenger_heap_pq, longestWaitingPassenger)
        return None



## THE T1 ALGO
def T1(passengersHeap_PQ, driversHeap_PQ):
    # passengersHeap_PQ, driversHeap_PQ, graphs, and metricsRecorded is already initialized
    n = 0
    while (passengersHeap_PQ): #is not empty
        pasengerAndDriver = matchAPassengerAndDriver(passengersHeap_PQ, driversHeap_PQ)
        executeRide(pasengerAndDriver)
        n = n+1
        print(f"{n} rides executed")
    

    # now that passengersHeap_PQ is empty,
    print(metricsRecorded)
    return metricsRecorded




simulation = T1(passengersHeap_PQ, driversHeap_PQ)
summarizeResult(simulation)