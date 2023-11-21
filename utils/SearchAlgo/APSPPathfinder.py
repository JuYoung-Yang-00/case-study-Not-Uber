from collections import defaultdict
import csv

class Precompute_Pathfinder:
    def __init__(self, shortest_path_filepath) -> None:
        self.path_costs = defaultdict(dict)
        self._load_shortest_paths(shortest_path_filepath)

    def _load_shortest_paths(self, filepath):
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)[1:]  # Skip the first header element as it's the column label

            for row in reader:
                node_id = row[0]
                for idx, cost in enumerate(row[1:]):
                    self.path_costs[node_id][headers[idx]] = float(cost)

    def lookup_shortest_path(self, node1: int, node2: int):
        if node1 in self.path_costs and node2 in self.path_costs[node1]:
            return self.path_costs[node1][node2]
        else:
            return None  # Or raise an exception if that's more appropriate for your use case

