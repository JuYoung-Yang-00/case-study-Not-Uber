from utils.Preprocessing.lib import *
from utils.kdtree import KDTree

def T1():
    driverQueue.queue.sort(key=lambda x: x.requestTime)
    d = driverQueue.queue.pop(0)

    riderQueue.queue.sort(key=lambda x: x.requestTime)
    r = riderQueue.queue.pop(0)

    print(d,r)
    
T1()

def T2():
    tree = KDTree(2)

    driverPoints = []
    riderPoints = []
    for driver in driverQueue.queue:
        driverPoints.append((driver.sourceX, driver.sourceY))
    for rider in riderQueue.queue:
        riderPoints.append((rider.sourceX, rider.sourceY))
    
    for i, driver in enumerate(driverPoints):
        tree.insert(driver, i)
    minDistance, (d_idx, r_idx) = tree.find_min_distance(riderPoints)
    print(driverQueue.queue[d_idx], riderQueue.queue[r_idx], " has min distance ", minDistance)

print("now running T2")
T2()