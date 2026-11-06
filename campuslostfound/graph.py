class CampusGraph:
    def __init__(self):
        # Adjacency list mapping how campus buildings are connected
        self.graph = {
            "Main Block": ["Library", "Cafeteria"],
            "Library": ["Main Block", "Computer Lab"],
            "Cafeteria": ["Main Block", "Sports Ground"],
            "Computer Lab": ["Library"],
            "Sports Ground": ["Cafeteria"]
        }

    # BFS Traversal to find all nearby locations spreading outward
    def get_nearby_locations(self, start_location):
        if start_location not in self.graph:
            return [start_location] 

        visited = set()
        queue = [start_location] 
        search_order = []

        while queue:
            current = queue.pop(0)
            if current not in visited:
                visited.add(current)
                search_order.append(current)
                
                # Add all adjacent, unvisited buildings to the queue
                for neighbor in self.graph.get(current, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return search_order