from typing import List, Tuple, Dict, Any
from .graph import CampusGraph
import json

class PathFinder:
    """
    Advanced path finding operations for UNILAG Campus Navigation
    Includes multi-path routing, dynamic updates, and route optimization
    """
    
    def __init__(self, campus_graph: CampusGraph):
        """Initialize PathFinder with a CampusGraph instance"""
        self.campus = campus_graph
        
    def find_optimal_routes(self, start: str, end: str, num_routes: int = 3) -> Dict[str, Any]:
        """
        Find optimal routes with detailed information
        
        Args:
            start: Starting location
            end: Destination location
            num_routes: Number of alternative routes to find
            
        Returns:
            Dictionary containing route information
        """
        routes = self.campus.k_shortest_paths(start, end, k=num_routes)
        
        result = {
            "start": start,
            "destination": end,
            "routes": [],
            "coordinates": {}
        }
        
        for i, (path, distance) in enumerate(routes):
            route_info = {
                "route_id": i + 1,
                "path": path,
                "distance": distance,
                "estimated_time": round(distance * 1.2, 1),  # Assume walking speed factor
                "coordinates": [self.campus.get_node_coordinates(node) for node in path],
                "turns": len(path) - 1
            }
            result["routes"].append(route_info)
        
        # Add all node coordinates for map rendering
        result["coordinates"] = self.campus.get_all_coordinates()
        
        return result
    
    def simulate_traffic_conditions(self, traffic_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Simulate different traffic/construction conditions
        
        Args:
            traffic_updates: List of traffic condition dictionaries
                            [{"from": "node1", "to": "node2", "condition": "heavy_traffic|construction|closed", "multiplier": 2.5}]
                            
        Returns:
            Dictionary with update status
        """
        condition_multipliers = {
            "light_traffic": 1.2,
            "heavy_traffic": 2.5, 
            "construction": 3.0,
            "closed": 100.0  # Very high weight to effectively close the route
        }
        
        updates = []
        status = []
        
        for update in traffic_updates:
            from_node = update["from"]
            to_node = update["to"]
            condition = update.get("condition", "heavy_traffic")
            custom_multiplier = update.get("multiplier")
            
            # Get original edge weight
            if self.campus.graph.has_edge(from_node, to_node):
                original_weight = self.campus.graph[from_node][to_node]["weight"]
                
                # Calculate new weight
                if custom_multiplier:
                    new_weight = original_weight * custom_multiplier
                else:
                    new_weight = original_weight * condition_multipliers.get(condition, 2.0)
                
                updates.append((from_node, to_node, new_weight))
                status.append({
                    "edge": f"{from_node} ↔ {to_node}",
                    "condition": condition,
                    "original_weight": original_weight,
                    "new_weight": new_weight,
                    "status": "updated"
                })
            else:
                status.append({
                    "edge": f"{from_node} ↔ {to_node}",
                    "condition": condition,
                    "status": "edge_not_found"
                })
        
        # Apply updates
        if updates:
            self.campus.apply_dynamic_updates(updates)
        
        return {
            "updates_applied": len(updates),
            "update_details": status,
            "timestamp": "2025-09-05T10:00:00Z"
        }
    
    def get_route_alternatives_with_preferences(self, start: str, end: str, 
                                               preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get route alternatives based on user preferences
        
        Args:
            start: Starting location
            end: Destination location
            preferences: Dictionary with user preferences
                        {"avoid": ["heavy_traffic_areas"], "prefer": ["scenic_routes"], "max_time": 30}
        
        Returns:
            Customized route recommendations
        """
        if preferences is None:
            preferences = {}
        
        # Get standard routes
        standard_routes = self.find_optimal_routes(start, end, num_routes=3)
        
        # Apply preference filtering (simplified implementation)
        filtered_routes = []
        
        for route in standard_routes["routes"]:
            route_score = self._calculate_route_score(route, preferences)
            route["preference_score"] = route_score
            route["recommendation"] = self._get_route_recommendation(route, preferences)
            filtered_routes.append(route)
        
        # Sort by preference score (higher is better)
        filtered_routes.sort(key=lambda x: x["preference_score"], reverse=True)
        
        return {
            "start": start,
            "destination": end,
            "preferences_applied": preferences,
            "recommended_routes": filtered_routes,
            "coordinates": standard_routes["coordinates"]
        }
    
    def _calculate_route_score(self, route: Dict[str, Any], preferences: Dict[str, Any]) -> float:
        """Calculate a preference-based score for a route"""
        base_score = 100.0
        
        # Penalize longer routes
        if route["distance"] > preferences.get("max_time", 30):
            base_score -= 20
        
        # Penalize routes with many turns
        if route["turns"] > 5:
            base_score -= 10
        
        # Boost shorter routes
        if route["distance"] < 15:
            base_score += 15
        
        return max(0, base_score)
    
    def _get_route_recommendation(self, route: Dict[str, Any], preferences: Dict[str, Any]) -> str:
        """Generate a text recommendation for a route"""
        if route["distance"] < 10:
            return "⚡ Fastest route - Recommended for quick trips"
        elif route["turns"] <= 2:
            return "🚶 Simple route - Easy to follow with minimal turns"
        elif route["distance"] < 20:
            return "⚖️ Balanced route - Good compromise between time and simplicity"
        else:
            return "🌿 Scenic route - Longer but may offer better views"
    
    def get_emergency_routes(self, start: str, emergency_locations: List[str]) -> Dict[str, Any]:
        """
        Find fastest routes to emergency locations (Medical Center, Security, etc.)
        
        Args:
            start: Current location
            emergency_locations: List of emergency destination nodes
            
        Returns:
            Emergency route information
        """
        emergency_routes = {}
        
        for location in emergency_locations:
            if location in self.campus.get_all_nodes():
                path, distance = self.campus.shortest_path(start, location)
                if path:
                    emergency_routes[location] = {
                        "path": path,
                        "distance": distance,
                        "estimated_time": round(distance * 1.5, 1),  # Faster walking for emergency
                        "coordinates": [self.campus.get_node_coordinates(node) for node in path]
                    }
        
        # Sort by distance (closest first)
        sorted_routes = dict(sorted(emergency_routes.items(), key=lambda x: x[1]["distance"]))
        
        return {
            "current_location": start,
            "emergency_routes": sorted_routes,
            "nearest_emergency": list(sorted_routes.keys())[0] if sorted_routes else None
        }

    def export_route_data(self, route_data: Dict[str, Any], filename: str = None) -> str:
        """
        Export route data to JSON file for external use
        
        Args:
            route_data: Route data dictionary
            filename: Optional filename (auto-generated if None)
            
        Returns:
            Filename of exported data
        """
        if filename is None:
            filename = f"route_export_{route_data.get('start', 'unknown')}_{route_data.get('destination', 'unknown')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(route_data, f, indent=2)
            return filename
        except Exception as e:
            print(f"❌ Error exporting route data: {e}")
            return None


# Example usage and testing
if __name__ == "__main__":
    from graph import CampusGraph
    
    # Initialize
    campus = CampusGraph()
    pathfinder = PathFinder(campus)
    
    # Test optimal routes
    print("🔍 Finding Optimal Routes:")
    print("=" * 40)
    routes = pathfinder.find_optimal_routes("Main Gate", "Medical Center", num_routes=3)
    
    for route in routes["routes"]:
        print(f"\nRoute {route['route_id']}:")
        print(f"  Path: {' → '.join(route['path'])}")
        print(f"  Distance: {route['distance']} minutes")
        print(f"  Estimated Time: {route['estimated_time']} minutes")
        print(f"  Turns: {route['turns']}")
    
    # Test traffic simulation
    print(f"\n🚧 Simulating Traffic Conditions:")
    print("=" * 40)
    
    traffic_updates = [
        {"from": "Library", "to": "Sports Complex", "condition": "construction"},
        {"from": "Main Gate", "to": "Faculty of Science", "condition": "heavy_traffic"}
    ]
    
    update_result = pathfinder.simulate_traffic_conditions(traffic_updates)
    print(f"Updates applied: {update_result['updates_applied']}")
    for detail in update_result["update_details"]:
        print(f"  {detail['edge']}: {detail['condition']} (Status: {detail['status']})")
    
    # Test emergency routes
    print(f"\n🚨 Emergency Routes:")
    print("=" * 40)
    emergency_result = pathfinder.get_emergency_routes("Faculty of Arts", ["Medical Center", "Admin Building", "Security Post"])
    print(f"From: {emergency_result['current_location']}")
    print(f"Nearest emergency location: {emergency_result.get('nearest_emergency', 'None found')}")
    
    for location, route_info in emergency_result["emergency_routes"].items():
        print(f"\nTo {location}:")
        print(f"  Path: {' → '.join(route_info['path'])}")
        print(f"  Distance: {route_info['distance']} minutes")
