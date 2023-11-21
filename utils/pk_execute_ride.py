
from utils.Preprocessing.load_drivers import *
from utils.Preprocessing.load_passengers import *
from utils.Preprocessing.createGraph import *
from utils.SearchAlgo.djikstra import *
import random
from datetime import timedelta

# Dictionary of probabilities that a driver works based on time category
driver_working_probabilities = {
        "weekday_0_8": 0.9,  
        "weekday_9_12": 0.95, 
        "weekday_13_20": 0.98,
        "weekday_21_24": 0.95,
        "weekend_0_8": 0.8, 
        "weekend_9_12": 0.85,
        "weekend_13_20": 0.9,
        "weekend_21_24": 0.85 
}

# executeRide returns a list of length 2
# first item: list of length-3-dictionaries of metrics
# second item: the driver class object that will be pushed back into the drivers pq, if the driver continues to work
def executeRide(driver, rider, adj_graph):

    driverStartingNodeID = theDriver.driverLocationVertexID
    passengerWillBePickedUpHereNodeID = thePassenger.pickUpLocationVertexID
    passengerWillBeDroppedOffHereNodeID = thePassenger.dropOffLocationVertexID

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
        timeItTookForPassengerToGoFromUnmatchedToDroppedOff = timeItTookForDriverToGetToPassenger + timeItTookFromPickupToDropoff
    # passenger became available before the driveer became avilable
    else:
        timeItTookForPassengerToGoFromUnmatchedToDroppedOff = ( (theDriver.timestamp - thePassenger.timestamp).total_seconds() / 3600 ) + timeItTookForDriverToGetToPassenger + timeItTookFromPickupToDropoff
    
    # add the length-3 dictionary to metricsRecorded
    metricsRecordedList.append({"timeItTookForDriverToGetToPassenger": timeItTookForDriverToGetToPassenger, "timeItTookFromPickupToDropoff": timeItTookFromPickupToDropoff, "timeItTookForPassengerToGoFromUnmatchedToDroppedOff": timeItTookForPassengerToGoFromUnmatchedToDroppedOff})
    
    # Calculate if the driver will work based on time category
    if should_driver_work(theDriver, timeItTookForDriverToGetToPassenger, timeItTookFromPickupToDropoff):
        new_timestamp = theDriver.timestamp + timedelta(hours=timeItTookForDriverToGetToPassenger) + timedelta(hours=timeItTookFromPickupToDropoff)

        # Push the driver back to the queue with the new timestamp and the drop-off location of the last passenger
        print("Driver continued working!!!!YAY!!!!")
        driverToAddBackToDriversHeapPQ = Driver(new_timestamp, thePassenger.destLat, thePassenger.destLon, passengerWillBeDroppedOffHereNodeID)
        
    else:
        driverToAddBackToDriversHeapPQ = None
        print("Driver quit working BROOOO")

    return [metricsRecordedList, driverToAddBackToDriversHeapPQ]

    # # last step of executeRide: at this point, theDriver has taken thePassenger to the drop-off vertex -> create a new Driver() with updated timestamp,  same lon (shouldn't matter), same lat (shouldn't matter), and updated driverLocationVertexID -> insert that Driver() to driversHeap_PQ
    # heapq.heappush(driversHeap_PQ, Driver(theDriver.timestamp+timedelta(hours=timeItTookForDriverToGetToPassenger)+timedelta(hours=timeItTookFromPickupToDropoff), thePassenger.destLat, thePassenger.destLon, passengerWillBeDroppedOffHereNodeID))






def should_driver_work(driver, timeItTookForDriverToGetToPassenger, timeItTookFromPickupToDropoff):
        drop_off_time = driver.timestamp + timedelta(hours=timeItTookForDriverToGetToPassenger) + timedelta(hours=timeItTookFromPickupToDropoff)
        day_of_week = drop_off_time.weekday()
        hour = drop_off_time.hour

        if day_of_week < 5:  
            if hour < 9:
                time_category = "weekday_0_8"
            elif hour < 13:
                time_category = "weekday_9_12"
            elif hour < 21:
                time_category = "weekday_13_20"
            else:
                time_category = "weekday_21_24"
        else: 
            if hour < 9:
                time_category = "weekend_0_8"
            elif hour < 13:
                time_category = "weekend_9_12"
            elif hour < 21:
                time_category = "weekend_13_20"
            else:
                time_category = "weekend_21_24"

        if random.random() < driver_working_probabilities[time_category]:
            return True
        else:
            return False