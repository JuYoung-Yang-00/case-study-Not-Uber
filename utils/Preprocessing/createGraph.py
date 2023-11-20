import csv

def calculate_travel_times(length, speeds):
    # Avoid division by zero in case of speed being zero
    return [length / speed if speed > 0 else float('inf') for speed in speeds] #hours





#creating the actual graph
def createGraph():
    edges = []
    graph = {}
    with open('./data/edges.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
    
        # Iterate through each row in the CSV file
        n = 0
        for row in csv_reader:
            # Access the columns in the row
            start_id = int(row[0])
            end_id = int(row[1])
            length = float(row[2])
            weekdays = [float(value) for value in row[3:27]]
            weekends = [float(value) for value in row[27:]]

            edges.append((start_id, end_id, length, weekdays, weekends))
            n = n+1
            # print(f"edge # {n} appended to edges[]")


    
    for start, end, length, weekdays, weekends in edges:
        if start not in graph:
            graph[start] = []
        weekday_times = calculate_travel_times(length, weekdays)
        weekend_times = calculate_travel_times(length, weekends)
        graph[start].append((end, weekday_times, weekend_times))

        
    
    print(f"GRAPH is created now, which has {len(graph)} nodes")
    # returns graph, the adjacency list in dictionary form
    return graph




