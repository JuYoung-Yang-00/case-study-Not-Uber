import json
import math

def euclidean_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the Euclidean distance between two points in a plane
    """
    return math.sqrt((lon1 - lon2)**2 + (lat1 - lat2)**2)

def findNearestVertex(latNumber, lonNumber, node_data):
    nearest_id = None
    shortest_distance = float('inf')
    
    for node_id, coords in node_data.items():
        lat, lon = float(coords[0]), float(coords[1])
        distance = euclidean_distance(lonNumber, latNumber, lon, lat)
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_id = int(node_id)
    
    return nearest_id



