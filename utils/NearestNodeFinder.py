
class Node:
    def __init__(self, point, index, left=None, right=None):
        self.point = point
        self.index = index
        self.left = left
        self.right = right

class KDTree:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.root = None

    def insert(self, point, index):
        self.root = self._insert_recursive(self.root, point, index, 0)

    def _insert_recursive(self, node, point, index, depth):
        if node is None:
            return Node(point, index)

        cd = depth % self.dimensions

        if point[cd] < node.point[cd]:
            node.left = self._insert_recursive(node.left, point, index, depth + 1)
        else:
            node.right = self._insert_recursive(node.right, point, index, depth + 1)

        return node

    def find_min_distance(self, points):
        if not self.root or not points:
            return float('inf'), (-1, -1)

        min_dist = float('inf')
        closest_pair = (-1, -1)
        for i, point in enumerate(points):
            dist, idx = self._find_min_distance_recursive(self.root, point, 0)
            if dist < min_dist:
                min_dist = dist
                closest_pair = (idx, i)

        return min_dist, closest_pair

    def _find_min_distance_recursive(self, node, point, depth):
        if node is None:
            return float('inf'), -1

        cd = depth % self.dimensions
        dist = self._euclidean_distance(node.point, point)
        next_best = node.left if point[cd] < node.point[cd] else node.right
        other_side = node.right if next_best is node.left else node.left

        min_dist, idx = self._find_min_distance_recursive(next_best, point, depth + 1)
        if dist < min_dist:
            min_dist = dist
            idx = node.index

        if abs(point[cd] - node.point[cd]) < min_dist:
            d, other_idx = self._find_min_distance_recursive(other_side, point, depth + 1)
            if d < min_dist:
                min_dist = d
                idx = other_idx

        return min_dist, idx

    @staticmethod
    def _euclidean_distance(p1, p2):
        return sum((x - y) ** 2 for x, y in zip(p1, p2)) ** 0.5


### Nearest Node finder Implementation
class NearestNodeFinder:
    def __init__(self, nodes): 
        self.tree = KDTree(2)

        node_coordinates = []
        i = 0
        self.node_id_mapping = {}
        for node_id, (x, y) in nodes.items():
            node_coordinates.append((x, y))
            self.node_id_mapping[i] = node_id
            i += 1
        for i, node_coordinate in enumerate(node_coordinates):
            self.tree.insert(node_coordinate, i)
    
    def find_nearest_node(self, sourceX, sourceY, nodes):
        
        minDistance, (n_idx, _) = self.tree.find_min_distance([(sourceX, sourceY)])
        # print(self.node_id_mapping[n_idx], " has min distance ", minDistance)
        return self.node_id_mapping[n_idx] 
