from heapq import heappush, heappop
from collections import defaultdict
import math

import heapq

def dijkstra(start, goal, adj_graph):

    # dictionary to store the shortest path to each vertex
    shortest_paths = {vertex: float('infinity') for vertex in adj_graph}
    shortest_paths[start] = 0

    # has (cost, node_id)
    priority_queue = [(0, start)]

    while priority_queue:

        # pop next node to visit from priority queue
        cost, current = heapq.heappop(priority_queue)

        # Early termination if the end node is reached
        if current == goal:
            break

        # for each neighbor node...
        for neighbor in adj_graph[current]:

            # add the cost
            add_cost = adj_graph[current][neighbor]['weekdays_cost'][0]  # Adjusted to use separate lists
            neighbor_cost = cost + add_cost

            # if the neighbor has a shorter path to the goal, update the path
            if neighbor_cost < shortest_paths[neighbor]:
                shortest_paths[neighbor] = neighbor_cost
                heapq.heappush(priority_queue, (neighbor_cost, neighbor))
    
    return shortest_paths[goal]

def a_star(start, goal, adj_graph, nodes) -> float:
    start = int(start)
    goal = int(goal)

    # Heuristic function (Euclidean distance)
    def heuristic(node1, node2):
        x1, y1 = nodes[node1]
        x2, y2 = nodes[node2]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # Initialize both open and closed sets
    priority_queue = []

    # initialize visited nodes dict
    visited_dict = defaultdict(lambda: False)

    # push first node
    heappush(priority_queue, (0, start))

    # for path reconstruction
    came_from = {}

    # Cost from start node to itself is zero
    g_score = {node: float('inf') for node in nodes}
    g_score[start] = 0

    # heuristic store
    f_score = {node: float('inf') for node in nodes}
    f_score[start] = heuristic(start, goal)

    while priority_queue:

        # next node to expand
        current = heappop(priority_queue)[1]

        # if we found the goal, reconstruct the path and return it
        if current == goal:
            # # Reconstruct path
            # total_path = []
            # while current in came_from:
            #     total_path.append(current)
            #     current = came_from[current]
            # return (total_path[::-1], g_score[goal])  # Return reversed path
            return g_score[goal] # return cost

        # if not yet at goal...
        # investigate the adjacent nodes
        for neighbor in adj_graph[current]:
            
            # calculate the tentative actual score
            tentative_g_score = g_score[current] + adj_graph[current][neighbor]['weekdays_cost'][0]

            # if 
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                if visited_dict[neighbor] is False:
                    heappush(priority_queue, (f_score[neighbor], neighbor))
                    visited_dict[neighbor] = True

    return False  # Return False if there is no path