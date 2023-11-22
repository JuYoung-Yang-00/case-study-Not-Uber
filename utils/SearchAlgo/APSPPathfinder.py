from collections import defaultdict
import csv


class Precompute_Pathfinder:
    def __init__(self, shortest_path_filepath) -> None:
        self.path_costs = defaultdict(dict)
        self._load_shortest_paths(shortest_path_filepath)
        print("done loading shortest paths")

    def _load_shortest_paths(self, filepath):
        data_dict = {}
        with open(filepath, "r") as file:
            reader = csv.reader(file)
            header = next(reader)[
                1:
            ]  # Skip the first header element as it's the column label

            for row in reader:
                node_id = row[0]
                node_data = row[1:]
                row_dict = {}
                for i, data in enumerate(node_data):
                    row_dict[int(header[i])] = float(data)
                data_dict[int(node_id)] = row_dict

        self.data_dict = data_dict

    def lookup_shortest_path(self, node1: int, node2: int):
        return self.data_dict[node1][node2]
