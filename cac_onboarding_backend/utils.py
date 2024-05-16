
import math
import heapq

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

def dijkstra(graph, start, end):
    # Initialize distances with infinity and set start node distance to 0
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Priority queue to keep track of nodes with their distances
    priority_queue = [(0, start)]

    # Previous nodes to reconstruct the path
    previous = {}

    while priority_queue:
        # Pop the node with the smallest distance
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we have already visited this node, skip it
        if current_distance > distances[current_node]:
            continue

        # If we reach the end node, reconstruct the path and return it
        if current_node == end:
            path = []
            while current_node in previous:
                path.append(current_node)
                current_node = previous[current_node]
            path.append(start)
            return path[::-1]

        # Iterate through neighbors of the current node
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            # If new distance is shorter, update distance and previous node
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # If end node is unreachable
    return None



def calculate_cost(duration):
    # Example transformation: cost = duration * 0.5
    return duration * 0.5


from geopy.geocoders import Nominatim