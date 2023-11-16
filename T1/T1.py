from reading_in_drivers import *
from reading_in_passengers import *
from createGraph import *
from datetime import timedelta
import csv

from djikstra import *

# 1. load data and initialize passenger priority queue and driver priority queue using loading_drivers_and_passengers.py)
passengersHeap_PQ = read_passengers_csv('givenDataFromSakai/passengers.csv')
driversHeap_PQ = read_drivers_csv('givenDataFromSakai/drivers.csv')

#2. load the graph
graphToUse = createGraph()

# 3. initializing metricsRecorded, which we'll use to talk about efficiency in the .pdf report we'll submit on Gradescope or something
metricsRecorded = [] # each item in metricsRecorded should contain a list that is: [timeItTookForDriverToGetToPassenger, timeItTookFromPickupToDropoff, timeItTookForPassengerToGoFromUnmatchedToDroppedOff]


# HELPER FUNCTION
def matchAPassengerAndDriver(passenger_heap_pq, driver_heap_pq):
    longestWaitingPassenger = heapq.heappop(passenger_heap_pq)

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






# HELPER FUNCTION
def executeRide(listReturnedFrom_matchAPassengerAndDriver):
    thePassenger = listReturnedFrom_matchAPassengerAndDriver[0] # is a Passenger Class
    theDriver = listReturnedFrom_matchAPassengerAndDriver[1] # is a Driver Class
    # thePassenger's properties: timestamp, sourceLat, sourceLon, destLat, destLon, pickUpLocationVertexID, dropOffLocationVertexID
    # theDriver's properties: timestamp, lat, lon, driverLocationVertexID

    '''
    # Extract day of the week and hour from the timestamp
    day_of_week = theDriver.timestamp.weekday()  # Monday is 0 and Sunday is 6
    hour = theDriver.timestamp.hour # getting .hour shouldn't need parentheses while getting weekday does need 'em
    if day_of_week < 5:  # Weekdays (Monday to Friday)
        timeCategory = f"weekday_{hour}"
    else:  # Weekends (Saturday and Sunday)
        timeCategory = f"weekend_{hour}"

    graphToUse = graphs[timeCategory]
    '''



    day_of_week = theDriver.timestamp.weekday()
    hour = theDriver.timestamp.hour

    
    driverStartingNodeID = theDriver.driverLocationVertexID
    passengerWillBePickedUpHereNodeID = thePassenger.pickUpLocationVertexID
    passengerWillBeDroppedOffHereNodeID = thePassenger.dropOffLocationVertexID

    '''
    # calculate and store how long it will take for theDriver to get to thePassenger, in units of hours
    timeItTookForDriverToGetToPassenger = nx.shortest_path_length(
        graphToUse, 
        source=driverStartingNodeID, 
        target=passengerWillBePickedUpHereNodeID, 
        weight='weight'
    )



    # calculate and store how long it will take for theDriver to get from pickup vertex to drop-off vertex, while passenger's in the car, in units of hours
    timeItTookFromPickupToDropoff = nx.shortest_path_length(
        graphToUse, 
        source=passengerWillBePickedUpHereNodeID, 
        target=passengerWillBeDroppedOffHereNodeID, 
        weight='weight'
    )
    '''

    # Calculate the travel times
    timeItTookForDriverToGetToPassenger = dijkstra_shortest_path(
        graphToUse, 
        driverStartingNodeID, 
        passengerWillBePickedUpHereNodeID,
        day_of_week,
        hour
    )

    timeItTookFromPickupToDropoff = dijkstra_shortest_path(
        graphToUse, 
        passengerWillBePickedUpHereNodeID, 
        passengerWillBeDroppedOffHereNodeID,
        day_of_week,
        hour
    )
    


    # passenger became available later than driver became available
    if thePassenger.timestamp - theDriver.timestamp > timedelta(0):
        timeItTookForPassengerToGoFromUnmatchedToDroppedOff = timeItTookForDriverToGetToPassenger + timeItTookFromPickupToDropoff # all in unit of hours
    else:
        timeItTookForPassengerToGoFromUnmatchedToDroppedOff = ( (theDriver.timestamp - thePassenger.timestamp).total_seconds() / 3600 ) + timeItTookForDriverToGetToPassenger + timeItTookFromPickupToDropoff
    
    



    # add the length-3 dictionary to metricsRecorded
    metricsRecorded.append({"timeItTookForDriverToGetToPassenger": timeItTookForDriverToGetToPassenger, "timeItTookFromPickupToDropoff": timeItTookFromPickupToDropoff, "timeItTookForPassengerToGoFromUnmatchedToDroppedOff": timeItTookForPassengerToGoFromUnmatchedToDroppedOff})




    # last step of executeRide: at this point, theDriver has taken thePassenger to the drop-off vertex -> create a new Driver() with updated timestamp,  same lon (shouldn't matter), same lat (shouldn't matter), and updated driverLocationVertexID -> insert that Driver() to driversHeap_PQ
    heapq.heappush(driversHeap_PQ, Driver(theDriver.timestamp+timedelta(hours=timeItTookForDriverToGetToPassenger)+timedelta(hours=timeItTookFromPickupToDropoff), thePassenger.destLat, thePassenger.destLon, passengerWillBeDroppedOffHereNodeID))








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




#T1(passengersHeap_PQ, driversHeap_PQ)



def summarizeT1result(outputOfTheT1Algo):
    # outputOfTheT1Algo = list -> each item in the list is a dictonary that looks something like:
    # {'timeItTookForDriverToGetToPassenger': 0.06343763989668617, 'timeItTookFromPickupToDropoff': 0.1664803757009768, 'timeItTookForPassengerToGoFromUnmatchedToDroppedOff': 0.2321906828198852}

    # things to aggregate/summarize:
    # D1 = minimize the amount of time (in minutes) between when they appear as an unmatched passenger, and when they are dropped off at their destination.
    D1list = []



    # D2 = Drivers want to maximize ride profit, defined as the number of minutes they spend driving passengers from pickup to drop-off locations minus the number of minutes they spend driving to pickup passengers
    # so, when D2 is NEGATIVE, that means driver took longer to get to the pick-up location than it took to drive the passenger in their car
    D2list = []


    for item in outputOfTheT1Algo:
        D1list.append(item['timeItTookForPassengerToGoFromUnmatchedToDroppedOff'] * 60) # converting to minutes
        D2list.append((item['timeItTookFromPickupToDropoff'] - item['timeItTookForDriverToGetToPassenger']) * 60) # converting to minutes

    with open('T1_summary.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # Write headers
        writer.writerow(['D1: timeItTookForPassengerToGoFromUnmatchedToDroppedOff (mins)', 
                         'D2: number of minutes they spend driving passengers from pickup to drop-off locations minus the number of minutes they spend driving to pickup passengers'])

         # Write data rows
        for d1, d2 in zip(D1list, D2list):
            writer.writerow([d1, d2])





simulation = T1(passengersHeap_PQ, driversHeap_PQ)
summarizeT1result(simulation)