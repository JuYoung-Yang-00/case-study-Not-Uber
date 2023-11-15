"""
DEPRECATED - DO NOT USE THIS IT IS CRAP



from reading_in_drivers import *
from reading_in_passengers import *


# commented out - used when checking/building function initially
'''




passengers_csv_file_path = 'givenDataFromSakai/passengers.csv'

# loading all passengers
passengers_heap_PQ = read_passengers_csv(passengers_csv_file_path)
# sanity check
print(len(passengers_heap_PQ))
print(heapq.heappop(passengers_heap_PQ))
print(type(heapq.heappop(passengers_heap_PQ)))

'''

#drivers_csv_file_path = 'givenDataFromSakai/drivers.csv'

# loading all drivers
#drivers_heap_PQ = read_drivers_csv(drivers_csv_file_path)
# sanity check
#print(len(drivers_heap_PQ))
#print(heapq.heappop(drivers_heap_PQ))
#print(type(heapq.heappop(drivers_heap_PQ)))




# THE BELOW TWO FUNCTIONS WILL BE USED IN T1.py
def initializeDriversHeapPQ(drivers_csv_file_path):
    drivers_heap_PQ = read_drivers_csv(drivers_csv_file_path)
    print(f"drivers heap pq is loaded and is of length {len(drivers_heap_PQ)}")
    return drivers_heap_PQ

def initializePassengersHeapPQ(passengers_csv_file_path):
    passengers_heap_PQ = read_passengers_csv(passengers_csv_file_path)
    print(f"drivers heap pq is loaded and is of length {len(passengers_heap_PQ)}")
    return passengers_heap_PQ
"""