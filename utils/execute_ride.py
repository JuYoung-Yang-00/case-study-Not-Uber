
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



def executeRide(listReturnedFrom_matchAPassengerAndDriver, graphToUse, metricsRecorded, driversHeap_PQ):
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


    latest = max(theDriver.timestamp, thePassenger.timestamp)
    day_of_week = latest.weekday()
    hour = latest.hour

    
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
    # from T1 import graphToUse, metricsRecorded, driversHeap_PQ
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
    metricsRecorded.append({"timeItTookForDriverToGetToPassenger": timeItTookForDriverToGetToPassenger, "timeItTookFromPickupToDropoff": timeItTookFromPickupToDropoff, "timeItTookForPassengerToGoFromUnmatchedToDroppedOff": timeItTookForPassengerToGoFromUnmatchedToDroppedOff})




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

    # Calculate if the driver will work based on time category
    if should_driver_work(theDriver, timeItTookForDriverToGetToPassenger, timeItTookFromPickupToDropoff):
        new_timestamp = theDriver.timestamp + timedelta(hours=timeItTookForDriverToGetToPassenger) + timedelta(hours=timeItTookFromPickupToDropoff)

        # Push the driver back to the queue with the new timestamp and the drop-off location of the last passenger
        print("Driver continued working!!!!YAY!!!!")
        heapq.heappush(driversHeap_PQ, Driver(new_timestamp, thePassenger.destLat, thePassenger.destLon, passengerWillBeDroppedOffHereNodeID))
    else:
        print("Driver quit working BROOOO")


    # # last step of executeRide: at this point, theDriver has taken thePassenger to the drop-off vertex -> create a new Driver() with updated timestamp,  same lon (shouldn't matter), same lat (shouldn't matter), and updated driverLocationVertexID -> insert that Driver() to driversHeap_PQ
    # heapq.heappush(driversHeap_PQ, Driver(theDriver.timestamp+timedelta(hours=timeItTookForDriverToGetToPassenger)+timedelta(hours=timeItTookFromPickupToDropoff), thePassenger.destLat, thePassenger.destLon, passengerWillBeDroppedOffHereNodeID))
