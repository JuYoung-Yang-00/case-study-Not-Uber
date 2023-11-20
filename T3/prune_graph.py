# lib.py
import json
import csv
from collections import defaultdict

class GraphReducer:
    
############ load data
    def __init__(self, node_filepath: str, edges_filepath: str):

        print("loading data")

        nodes = {}
        with open(node_filepath, 'r') as file:
            nodes_json = json.load(file)
            for node_id, node_latlon in nodes_json.items():
                nodes[int(node_id)] = (node_latlon['lon'], node_latlon['lat'])
        self.nodes = nodes

        edges = []
        with open(edges_filepath, 'r') as file:
            # Create a CSV reader object
            csv_reader = csv.reader(file)
            csv_reader.__next__()  # Skip the header row
            
            # Iterate through each row in the CSV file
            for row in csv_reader:
                # Access the columns in the row
                start_id = int(row[0])
                end_id = int(row[1])
                length = float(row[2])
                weekdays_cost = [float(value) for value in row[3:27]]
                weekends_cost = [float(value) for value in row[27:]]

                edges.append((start_id, end_id, length, weekdays_cost, weekends_cost))
        self.edges = edges

        print("finished loading data")

        adjacency_graph = defaultdict(lambda: defaultdict(dict))
        for start, end, length, weekdays_cost, weekends_cost in edges:
            adjacency_graph[start][end] = {
                "weekdays_cost": weekdays_cost,
                "weekends_cost": weekends_cost
            }
            adjacency_graph[end][start] = {
                "weekdays_cost": weekdays_cost,
                "weekends_cost": weekends_cost
            }
        self.adj_graph = adjacency_graph

        
    def remove_vertices_and_edges(self, vertex_count):
        print("keeping ", vertex_count, " vertices")

        # dfs traversal to find which vertex to keep
        vertices_to_keep = self._dfs_traverse_count(vertex_count)
        vertices_to_remove = self.nodes.keys() - vertices_to_keep

        # copy reduced nodes and edges into a different var
        self.reduced_nodes = self.nodes.copy()
        self.reduced_edges = self.edges.copy()

        # remove vertices
        for vertex in vertices_to_remove:
            del self.reduced_nodes[vertex]

        # remove edges that contain removed vertices
        self.reduced_edges = [(start, end, length, weekdays_cost, weekends_cost) for start, end, length, weekdays_cost, weekends_cost in self.reduced_edges
                if start not in vertices_to_remove and end not in vertices_to_remove]

        if self._is_graph_connected() is not True:
            raise Exception("Modified graph is not connected!")


    def _dfs_traverse_count(self, n):

        visited = set()
        stack = [next(iter(self.adj_graph))]  # Start with any node
        count = 0

        while stack and count < n:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                count += 1
                stack.extend(set(self.adj_graph[node].keys()) - visited)

        return visited

    def save_data(self, nodes_filepath: str, edges_filepath: str):
        # Save nodes to JSON
        with open(nodes_filepath, 'w') as file:
            json.dump({str(node_id): {"lon": lon, "lat": lat} for node_id, (lon, lat) in self.reduced_nodes.items()}, file)

        # Save edges to CSV
        with open(edges_filepath, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['start_id', 'end_id', 'length', *['weekday_' + str(i) for i in range(24)], *['weekend_' + str(i) for i in range(24)]])
            for start, end, length, weekdays_cost, weekends_cost in self.reduced_edges:
                csv_writer.writerow([start, end, length, *weekdays_cost, *weekends_cost])

    def _is_graph_connected(self):
        if not self.nodes:
            return True

        graph = defaultdict(set)
        for start, end, _, _, _ in self.edges:
            graph[start].add(end)
            graph[end].add(start)

        visited = set()
        stack = [next(iter(self.nodes))]  # Start with any node

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(graph[node] - visited)

        return len(visited) == len(self.nodes)

gr = GraphReducer(node_filepath='./data/node_data.json', edges_filepath='./data/edges.csv')

# for 1000, 2000, ..., 10,000
for n in range(1000, 10000, 1000):

    # Remove vertices and edges while maintaining connectivity
    gr.remove_vertices_and_edges(n)

    # Save modified data
    gr.save_data(nodes_filepath='./data/modified_node_data_'+str(n)+'.json', edges_filepath='./data/modified_edges_'+str(n)+'.csv')
