import math
import heapq
from datetime import datetime, timedelta
from utils.Preprocessing.load_drivers import *
from utils.Preprocessing.load_passengers import *
from utils.Preprocessing.createGraph import *
from utils.execute_ride import *
from utils.summarizeResult import *
from utils.SearchAlgo.djikstra import *


# 1. load data and initialize passenger priority queue and driver priority queue using loading_drivers_and_passengers.py)
passengersHeap_PQ = read_passengers_csv('./data/passengers.csv')
driversHeap_PQ = read_drivers_csv('./data/drivers.csv')

#2. load the graph
graphToUse = createGraph()

# 3. initializing metricsRecorded, which we'll use to talk about efficiency in the .pdf report we'll submit on Gradescope or something
metricsRecorded = [] # each item in metricsRecorded should contain a list that is: [timeItTookForDriverToGetToPassenger, timeItTookFromPickupToDropoff, timeItTookForPassengerToGoFromUnmatchedToDroppedOff]


# HELPER FUNCTION
def matchAPassengerAndDriver(passenger_heap_pq, driver_heap_pq):
    longestWaitingPassenger = heapq.heappop(passenger_heap_pq)
    matchedDriver = heapq.heappop(driver_heap_pq)
 

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
def T1(passengersHeap_PQ, driversHeap_PQ, metricsRecorded):
    metricsRecordedUpdated = metricsRecorded
    # passengersHeap_PQ, driversHeap_PQ, graphs, and metricsRecorded is already initialized
    n = 0
    while (passengersHeap_PQ): #is not empty
        passengerAndDriver = matchAPassengerAndDriver(passengersHeap_PQ, driversHeap_PQ)
        executeRideResult = executeRide(passengerAndDriver, graphToUse, metricsRecordedUpdated)
        metricsRecordedUpdated = executeRideResult[0]
        driverToBeAddedBackToPQ = executeRideResult[1]
        n = n+1
        print(f"{n} rides executed")
        if driverToBeAddedBackToPQ is not None:
            heapq.heappush(driversHeap_PQ, driverToBeAddedBackToPQ)
            print("a driver got added back to driver heap pq")
    

    # now that passengersHeap_PQ is empty,
    print(metricsRecordedUpdated)
    return metricsRecordedUpdated


simulation = T1(passengersHeap_PQ, driversHeap_PQ, metricsRecorded)
summarizeResult(simulation)