import pandas as pd
import numpy as np

# Load Data with Pandas
nodes_df = pd.read_json('./data/node_data.json')
edges_df = pd.read_csv('./data/edges.csv')

# Data processing
nodes_array = nodes_df.to_numpy()
edges_array = edges_df.to_numpy()

vertex_count = len(nodes_array)

# Initialize cost matrix with infinity
cost_matrix = np.full((vertex_count, vertex_count), np.inf)

# Populate the matrix
for edge in edges_array:
    start_id, end_id = int(edge[0]), int(edge[1])
    length = float(edge[2])
    speed_weekdays = edge[3:27].astype(float)
    cost_weekdays = length / speed_weekdays[0]  # assuming the first speed value
    cost_matrix[start_id, end_id] = cost_weekdays

np.fill_diagonal(cost_matrix, 0)

# Floyd-Warshall Algorithm Optimized with Numpy
for k in range(vertex_count):
    for i in range(vertex_count):
        cost_matrix[i] = np.minimum(cost_matrix[i], cost_matrix[i, k] + cost_matrix[k])

# Save to CSV
pd.DataFrame(cost_matrix).to_csv('./data/shortest_path_costs.csv', index=False)