import networkx as nx
import json
import os
from typing import List, Tuple, Dict, Any

class CampusGraph:
    """
    UNILAG Campus Navigation Graph Implementation
    Using NetworkX and Dijkstra's algorithm for shortest path computation
    """
    
    def __init__(self, data_file: str = None):
        """Initialize the campus graph from JSON data"""
        self.graph = nx.DiGraph()
        self.coordinates = {}
        
        # Default data file path
        if data_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_file = os.path.join(current_dir, 'data', 'campus_nodes_edges.json')
        
        self.load_campus_data(data_file)
    
    def load_campus_data(self, data_file: str):
        """Load campus nodes, edges, and coordinates from JSON file"""
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            # Add nodes
            for node in data['nodes']:
                self.graph.add_node(node)
            
            # Add edges with weights (bidirectional)
            for edge in data['edges']:
                start, end, weight = edge[0], edge[1], edge[2]
                self.graph.add_edge(start, end, weight=weight)
                self.graph.add_edge(end, start, weight=weight)  # Make bidirectional
            
            # Store coordinates for map visualization
            self.coordinates = data.get('coordinates', {})
            
            print(f"✅ Campus graph loaded successfully!")
            print(f"📍 Nodes: {len(self.graph.nodes())}")
            print(f"🛤️  Edges: {len(self.graph.edges())}")
            
        except FileNotFoundError:
            print(f"❌ Error: Data file '{data_file}' not found!")
        except json.JSONDecodeError:
            print(f"❌ Error: Invalid JSON format in '{data_file}'!")
    
    def shortest_path(self, start: str, end: str) -> Tuple[List[str], float]:
        """
        Find the shortest path between two nodes using Dijkstra's algorithm
        
        Args:
            start: Starting node
            end: Destination node
            
        Returns:
            Tuple of (path_list, total_distance)
        """
        try:
            path = nx.dijkstra_path(self.graph, source=start, target=end, weight='weight')
            distance = nx.dijkstra_path_length(self.graph, source=start, target=end, weight='weight')
            return path, distance
        except nx.NetworkXNoPath:
            print(f"❌ No path found between '{start}' and '{end}'")
            return [], float('inf')
        except nx.NodeNotFound as e:
            print(f"❌ Node not found: {e}")
            return [], float('inf')
    
    def k_shortest_paths(self, start: str, end: str, k: int = 3) -> List[Tuple[List[str], float]]:
        """
        Find k shortest paths between two nodes
        
        Args:
            start: Starting node
            end: Destination node  
            k: Number of paths to find
            
        Returns:
            List of tuples [(path, distance), ...]
        """
        paths = []
        temp_graph = self.graph.copy()
        
        try:
            for i in range(k):
                try:
                    path = nx.dijkstra_path(temp_graph, source=start, target=end, weight='weight')
                    distance = nx.dijkstra_path_length(temp_graph, source=start, target=end, weight='weight')
                    
                    # Avoid duplicate paths
                    if (path, distance) not in paths:
                        paths.append((path, distance))
                    
                    # Remove an edge from the path to find alternative routes
                    if len(path) > 1:
                        # Remove the edge with highest weight in the path
                        max_weight = 0
                        edge_to_remove = None
                        
                        for j in range(len(path) - 1):
                            u, v = path[j], path[j + 1]
                            if temp_graph.has_edge(u, v):
                                weight = temp_graph[u][v]['weight']
                                if weight > max_weight:
                                    max_weight = weight
                                    edge_to_remove = (u, v)
                        
                        if edge_to_remove:
                            temp_graph.remove_edge(edge_to_remove[0], edge_to_remove[1])
                    else:
                        break
                        
                except nx.NetworkXNoPath:
                    break
                    
        except nx.NodeNotFound as e:
            print(f"❌ Node not found: {e}")
            
        return paths
    
    def update_edge_weight(self, start: str, end: str, new_weight: float):
        """
        Update the weight of an edge (for dynamic path updates)
        
        Args:
            start: Starting node of edge
            end: Ending node of edge
            new_weight: New weight value
        """
        if self.graph.has_edge(start, end):
            self.graph[start][end]['weight'] = new_weight
            print(f"✅ Updated edge '{start}' → '{end}' weight to {new_weight}")
        else:
            print(f"❌ Edge '{start}' → '{end}' not found!")
    
    def apply_dynamic_updates(self, updates: List[Tuple[str, str, float]]):
        """
        Apply multiple edge weight updates (e.g., for road closures, traffic)
        
        Args:
            updates: List of tuples [(start_node, end_node, new_weight), ...]
        """
        print("🔄 Applying dynamic updates...")
        for start, end, weight in updates:
            self.update_edge_weight(start, end, weight)
            # Update reverse edge too (bidirectional)
            self.update_edge_weight(end, start, weight)
    
    def get_all_nodes(self) -> List[str]:
        """Get list of all nodes in the graph"""
        return list(self.graph.nodes())
    
    def get_node_coordinates(self, node: str) -> Tuple[float, float]:
        """Get coordinates for a specific node"""
        return self.coordinates.get(node, (0, 0))
    
    def get_all_coordinates(self) -> Dict[str, Tuple[float, float]]:
        """Get all node coordinates"""
        return self.coordinates
    
    def display_graph_info(self):
        """Display basic information about the graph"""
        print("\n🏫 UNILAG Campus Navigation Graph")
        print("=" * 40)
        print(f"📍 Total Nodes: {len(self.graph.nodes())}")
        print(f"🛤️  Total Edges: {len(self.graph.edges())}")
        print(f"\n📋 Available Locations:")
        for i, node in enumerate(sorted(self.graph.nodes()), 1):
            print(f"   {i:2d}. {node}")


# Example usage and testing
if __name__ == "__main__":
    # Initialize campus graph
    campus = CampusGraph()
    
    # Display graph information
    campus.display_graph_info()
    
    # Test shortest path
    print("\n🔍 Testing Shortest Path:")
    print("-" * 30)
    start, end = "Main Gate", "Senate Building"
    path, distance = campus.shortest_path(start, end)
    print(f"From: {start}")
    print(f"To: {end}")
    print(f"Shortest Path: {' → '.join(path)}")
    print(f"Total Distance: {distance} minutes")
    
    # Test multiple paths
    print(f"\n🔍 Testing Alternative Paths:")
    print("-" * 30)
    paths = campus.k_shortest_paths(start, end, k=3)
    for i, (path, distance) in enumerate(paths, 1):
        print(f"Path {i}: {' → '.join(path)} (Distance: {distance} minutes)")
    
    # Test dynamic updates
    print(f"\n🔄 Testing Dynamic Updates:")
    print("-" * 30)
    print("Simulating road closure: Faculty of Science ↔ Library (weight: 5 → 50)")
    campus.apply_dynamic_updates([("Faculty of Science", "Library", 50)])
    
    # Recalculate path after update
    new_path, new_distance = campus.shortest_path(start, end)
    print(f"New Shortest Path: {' → '.join(new_path)}")
    print(f"New Distance: {new_distance} minutes")
