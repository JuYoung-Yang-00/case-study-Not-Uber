import heapq

def dijkstra_shortest_path(graph, start, end, day_of_week, hour):
    # Determine the index for time selection
    time_index = hour

    shortest_paths = {vertex: float('infinity') for vertex in graph}
    shortest_paths[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        # Early termination if the end node is reached
        if current_vertex == end:
            break

        for neighbor, weekday_times, weekend_times in graph[current_vertex]:
            # Select the correct time based on the index
            time = weekday_times[time_index] if day_of_week < 5 else weekend_times[time_index]  # Adjusted to use separate lists
            distance = current_distance + time

            if distance < shortest_paths[neighbor]:
                shortest_paths[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return shortest_paths[end]
