from collections import defaultdict
import json
import csv 

## 1. Load Data

# nodes is a list of tuples (node_id, longitude, latitude)
nodes = []

with open('./data/node_data.json', 'r') as file:
    node_json = json.load(file)
    for k, v in node_json.items():
        nodes.append((k, v['lon'], v['lat']))

# edges is a list of tuples (start_node_id, end_node_id, time_weekdays[], time_weekends[]))
edges = []
with open('./data/edges.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    csv_reader.__next__()  # Skip the header row
    
    # Iterate through each row in the CSV file
    for row in csv_reader:
        # Access the columns in the row
        start_id = int(row[0])
        end_id = int(row[1])
        length = float(row[2])
        cost_weekdays = [length/float(value) for value in row[3:27]]
        cost_weekends = [length/float(value) for value in row[27:]]

        edges.append((start_id, end_id, cost_weekdays, cost_weekends))

print("data loaded")
## 2. run a-star on all pairs

# Count the number of vertices in the graph
vertex_count = len(nodes)

print("vertex_count", vertex_count)
# Initialize the distance matrix with infinity


# Initialize the sparse matrix
cost_matrix = defaultdict(lambda: defaultdict(lambda: float('inf')))


# Update the distance matrix with the edge distances and speed
for i, edge in enumerate(edges):
    start_id, end_id, cost_weekdays, cost_weekends = edge

    # use the weekday_0 speed for now
    cost = cost_weekdays[0]

    # save the travel time across each edge
    cost_matrix[start_id][end_id] = cost

# Set the diagonal to zero
for i in range(vertex_count):
    cost_matrix[i][i] = 0

# Floyd-Warshall Algorithm

# using up to 0...k verticies
for k in range(vertex_count):

    # from node i to j
    for i in range(vertex_count):
        print("i,k", i, k)
        for j in range(vertex_count):
            if cost_matrix[i][k] + cost_matrix[k][j] < cost_matrix[i][j]:
                cost_matrix[i][j] = cost_matrix[i][k] + cost_matrix[k][j]

print("Floyd-Warshall Algorithm Complete")

# Open a new CSV file for writing
with open('./data/shortest_path_costs.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)

    # Optional: Write headers (Node IDs)
    headers = ['Node'] + [str(i) for i in range(vertex_count)]
    csv_writer.writerow(headers)

    # Write the data from the cost_matrix
    for i in range(vertex_count):
        row = [str(i)] + cost_matrix[i]
        csv_writer.writerow(row)

print("Shortest path costs saved to shortest_path_costs.csv")
