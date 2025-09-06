#!/usr/bin/env python3
"""
UNILAG Campus Navigation Server
Enhanced with Dijkstra Algorithm Visualization
"""

import heapq
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=['http://localhost:8080', 'http://127.0.0.1:8080', 'http://localhost:3000'])

def load_campus_data():
    """Load campus data from JSON file"""
    try:
        data_file = '/Users/mac/Desktop/school/final-year/UNILAG-Campus-Navigation/backend/data/campus_nodes_edges.json'
        with open(data_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: campus_nodes_edges.json not found")
        return {"nodes": [], "edges": [], "coordinates": {}}
    except json.JSONDecodeError:
        print("Error: Invalid JSON in campus_nodes_edges.json")
        return {"nodes": [], "edges": [], "coordinates": {}}

def build_graph(edges):
    """Build adjacency list representation of the graph"""
    graph = {}
    for edge in edges:
        if len(edge) >= 3:
            node1, node2, weight = edge[0], edge[1], edge[2]
            
            if node1 not in graph:
                graph[node1] = []
            if node2 not in graph:
                graph[node2] = []
            
            graph[node1].append((node2, weight))
            graph[node2].append((node1, weight))
    
    return graph

import heapq
import math
import json
from copy import deepcopy

# Enhanced distance calculations and graph building
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

def calculate_bearing(lat1, lon1, lat2, lon2):
    """
    Calculate the bearing between two points
    Returns bearing in degrees
    """
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlon = lon2 - lon1
    
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    
    bearing = math.atan2(y, x)
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360
    
    return bearing

def build_enhanced_graph(nodes, coordinates):
    """
    Build a graph based on proximity and logical connections
    Uses Haversine distance for realistic weights - similar to geopy approach
    """
    from collections import defaultdict
    
    graph = {}
    max_connection_distance = 0.8  # Maximum 800m direct connection
    
    print(f"Building enhanced graph for {len(nodes)} nodes...")
    
    for idx, node1 in enumerate(nodes):
        if node1 not in coordinates:
            continue
            
        centre_lat, centre_lon = coordinates[node1]
        connections = {}
        
        # Check all other nodes for proximity (similar to df_temp filtering)
        for node2 in nodes:
            if node1 == node2 or node2 not in coordinates:
                continue
                
            lat2, lon2 = coordinates[node2]
            distance = haversine_distance(centre_lat, centre_lon, lat2, lon2)
            
            # Connect nodes that are within reasonable walking distance
            if distance < max_connection_distance:
                connections[node2] = distance
        
        # Only add node to graph if it has connections (similar to their filtering)
        if connections:
            graph[node1] = connections
    
    # Filter out nodes without connections (similar to their {k: v for k, v in graph.items() if v})
    graph = {k: v for k, v in graph.items() if v}
    nodes_with_connections = list(graph.keys())
    
    print(f"Graph built with {len(nodes_with_connections)} connected nodes")
    print(f"Total connections: {sum(len(neighbors) for neighbors in graph.values())}")
    
    return graph, nodes_with_connections

def enhanced_dijkstra_algorithm(start_node, end_node, graph, track_steps=True):
    """
    Enhanced Dijkstra algorithm similar to the reference implementation
    but with optional step tracking for visualization
    """
    import heapq
    
    # Get all nodes from graph
    nodes = list(graph.keys())
    
    if start_node not in nodes or end_node not in nodes:
        return {
            'path': [],
            'distance': None,
            'steps': [],
            'algorithm': 'enhanced_dijkstra',
            'error': 'Start or end node not in graph'
        }
    
    # Initialize (similar to their approach) - use 999999 instead of float('inf') for JSON compatibility
    unmarked_nodes = nodes.copy()
    INFINITY = 999999
    shortest_path = {node: INFINITY for node in unmarked_nodes}
    shortest_path[start_node] = 0
    previous_nodes = {}
    
    # For step tracking
    steps = []
    visited_order = []
    
    if track_steps:
        # Convert infinity values to null for JSON serialization
        distances_for_json = {k: (None if v == INFINITY else v) for k, v in shortest_path.items()}
        steps.append({
            'step': 0,
            'description': f'Initialize: Set distance to {start_node} = 0, all others = ∞',
            'current_node': start_node,
            'distances': distances_for_json,
            'visited': [],
            'queue': unmarked_nodes.copy(),
            'action': 'initialize'
        })
    
    step_count = 1
    
    while unmarked_nodes:
        # Find current node with minimum distance (similar to their min() approach)
        current_marked_node = min(unmarked_nodes, key=lambda node: shortest_path.get(node, INFINITY))
        
        if shortest_path[current_marked_node] == INFINITY:
            break  # No more reachable nodes
            
        visited_order.append(current_marked_node)
        
        if track_steps:
            # Convert infinity values for JSON
            distances_for_json = {k: (None if v == INFINITY else round(v, 3)) for k, v in shortest_path.items()}
            steps.append({
                'step': step_count,
                'description': f'Visit {current_marked_node} (distance: {shortest_path[current_marked_node]:.3f}km)',
                'current_node': current_marked_node,
                'distances': distances_for_json,
                'visited': list(visited_order),
                'queue': [n for n in unmarked_nodes if n != current_marked_node],
                'action': 'visit_node'
            })
            step_count += 1
        
        # Early termination if we reached the destination
        if current_marked_node == end_node:
            break
        
        # Check neighbors (similar to their neighbor_nodes approach)
        neighbor_nodes = graph.get(current_marked_node, {})
        
        for neighbor, edge_distance in neighbor_nodes.items():
            if neighbor in unmarked_nodes:
                # Calculate new distance (similar to their value_on_hold)
                value_on_hold = shortest_path[current_marked_node] + edge_distance
                
                if value_on_hold < shortest_path.get(neighbor, INFINITY):
                    shortest_path[neighbor] = value_on_hold
                    previous_nodes[neighbor] = current_marked_node
                    
                    if track_steps:
                        # Convert infinity values for JSON
                        distances_for_json = {k: (None if v == INFINITY else round(v, 3)) for k, v in shortest_path.items()}
                        steps.append({
                            'step': step_count,
                            'description': f'Relax edge {current_marked_node} → {neighbor}. New distance: {value_on_hold:.3f}km',
                            'current_node': current_marked_node,
                            'distances': distances_for_json,
                            'visited': list(visited_order),
                            'queue': [n for n in unmarked_nodes if n != current_marked_node],
                            'action': 'relax_edge',
                            'edge': (current_marked_node, neighbor)
                        })
                        step_count += 1
        
        unmarked_nodes.remove(current_marked_node)
    
    # Reconstruct path (similar to their path reconstruction)
    path = []
    if end_node in previous_nodes or end_node == start_node:
        node = end_node
        while node != start_node:
            path.append(node)
            if node in previous_nodes:
                node = previous_nodes[node]
            else:
                break  # Path not found
        path.append(start_node)
        path = list(reversed(path))
    
    final_distance = shortest_path.get(end_node, INFINITY)
    
    if track_steps and path:
        # Convert infinity values for JSON
        distances_for_json = {k: (None if v == INFINITY else round(v, 3)) for k, v in shortest_path.items()}
        steps.append({
            'step': step_count,
            'description': f'Algorithm complete! Shortest distance: {final_distance:.3f}km',
            'current_node': end_node,
            'distances': distances_for_json,
            'visited': list(visited_order),
            'queue': [],
            'action': 'complete',
            'final_path': path
        })
    
    return {
        'path': path if path and path[0] == start_node else [],
        'distance': final_distance if final_distance != INFINITY else None,
        'steps': steps,
        'algorithm': 'enhanced_dijkstra'
    }

def get_path_coordinates(path, coordinates):
    """
    Get coordinates for the path to draw on map
    """
    path_coords = []
    for node in path:
        if node in coordinates:
            lat, lon = coordinates[node]
            path_coords.append([lat, lon])
    return path_coords

def dijkstra_with_steps(graph, start_node, end_node):
    """Enhanced Dijkstra algorithm with step-by-step tracking and alternative paths"""
    # Initialize distances and tracking structures
    distances = {node: 999999 if node != start_node else 0 for node in graph}
    previous = {node: None for node in graph}
    unvisited = set(graph.keys())
    steps = []
    priority_queue = [(0, start_node)]
    visited_order = []
    
    # Step 0: Initialization
    steps.append({
        'step': 0,
        'description': f'Initialize algorithm. Set distance to {start_node} = 0, all others = ∞',
        'current_node': start_node,
        'distances': dict(distances),
        'visited': [],
        'queue': [start_node],
        'action': 'initialize'
    })
    
    step_count = 1
    
    while priority_queue and unvisited:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node not in unvisited:
            continue
            
        unvisited.remove(current_node)
        visited_order.append(current_node)
        
        # Record current step
        queue_nodes = [node for _, node in priority_queue if node in unvisited]
        steps.append({
            'step': step_count,
            'description': f'Visit {current_node} (distance: {current_distance}). Examining neighbors...',
            'current_node': current_node,
            'distances': dict(distances),
            'visited': list(visited_order),
            'queue': queue_nodes,
            'action': 'visit_node'
        })
        step_count += 1
        
        # Stop if we reached the destination
        if current_node == end_node:
            break
            
        # Check neighbors
        for neighbor_data in graph.get(current_node, []):
            if isinstance(neighbor_data, tuple):
                neighbor, weight = neighbor_data
            else:
                neighbor = neighbor_data
                weight = 1
                
            if neighbor in unvisited:
                # Calculate distance using the edge weight
                new_distance = distances[current_node] + weight
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))
                    
                    # Record relaxation step
                    steps.append({
                        'step': step_count,
                        'description': f'Relax edge {current_node} → {neighbor}. New distance: {new_distance}',
                        'current_node': current_node,
                        'distances': dict(distances),
                        'visited': list(visited_order),
                        'queue': [node for _, node in priority_queue if node in unvisited],
                        'action': 'relax_edge',
                        'edge': (current_node, neighbor)
                    })
                    step_count += 1
    
    # Reconstruct path
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    # Final step
    if path and path[0] == start_node:
        steps.append({
            'step': step_count,
            'description': f'Algorithm complete! Shortest path found with distance {distances[end_node]}',
            'current_node': end_node,
            'distances': dict(distances),
            'visited': list(visited_order),
            'queue': [],
            'action': 'complete',
            'final_path': path
        })
    
    return {
        'path': path if path and path[0] == start_node else [],
        'distance': distances[end_node] if distances[end_node] != 999999 else None,
        'steps': steps,
        'algorithm': 'dijkstra'
    }

def find_all_possible_paths(graph, start_node, end_node, max_depth=6, max_paths=50):
    """
    Find possible paths using depth-first search approach with strict limits
    Limited to prevent infinite loops and excessive computation
    """
    if start_node not in graph or end_node not in graph:
        return []
    
    all_paths = []
    
    def dfs_paths(current, end, path, visited, depth):
        # Strict limits to prevent hanging
        if depth > max_depth or len(all_paths) >= max_paths:
            return
        
        if current == end:
            # Found a complete path
            total_distance = 0
            valid_path = True
            
            for i in range(len(path) - 1):
                curr_node = path[i]
                next_node = path[i + 1]
                if curr_node in graph and next_node in graph[curr_node]:
                    total_distance += graph[curr_node][next_node]
                else:
                    valid_path = False
                    break
            
            if valid_path and len(all_paths) < max_paths:
                all_paths.append((path[:], total_distance))
            return
        
        # Explore neighbors
        neighbors = list(graph.get(current, {}).keys())
        # Limit neighbors to prevent exponential explosion
        neighbors = neighbors[:8]  # Max 8 neighbors per node
        
        for neighbor in neighbors:
            if neighbor not in visited:
                new_visited = visited.copy()
                new_visited.add(neighbor)
                dfs_paths(neighbor, end, path + [neighbor], new_visited, depth + 1)
    
    # Start DFS
    try:
        initial_visited = {start_node}
        dfs_paths(start_node, end_node, [start_node], initial_visited, 0)
    except Exception as e:
        print(f"Error in DFS path finding: {e}")
        # Fallback: just return the shortest path
        result = enhanced_dijkstra_algorithm(start_node, end_node, graph, track_steps=False)
        if result['path']:
            return [(result['path'], result['distance'])]
    
    # Sort by distance and limit results
    all_paths.sort(key=lambda x: x[1])
    return all_paths[:min(max_paths, len(all_paths))]

def create_comprehensive_analysis(paths_with_distances, start_node, end_node):
    """
    Create comprehensive route analysis in the format requested by user
    """
    if not paths_with_distances:
        return {}
    
    # Get shortest and longest paths
    shortest_path, shortest_distance = paths_with_distances[0]
    longest_path, longest_distance = paths_with_distances[-1]
    total_routes = len(paths_with_distances)
    
    # Calculate difference
    difference_km = longest_distance - shortest_distance
    difference_m = difference_km * 1000
    
    # Create the analysis in user's requested format
    analysis = {
        'dijkstra_choice': f"🎯 DIJKSTRA'S OPTIMAL CHOICE: {shortest_distance:.2f}km",
        'total_routes_found': f"📊 FOUND: {total_routes} total possible routes",
        'shortest_route': f"🟢 Shortest: {shortest_distance:.2f}km (Selected by Dijkstra)",
        'longest_route': f"🔴 Longest: {longest_distance:.2f}km (+{difference_m:.0f}m longer)",
        'why_optimal': f"🧠 WHY OPTIMAL: Dijkstra guarantees the shortest distance of {shortest_distance:.2f}km using real-world coordinates and haversine distance calculations"
    }
    
    return analysis

def yen_k_shortest_paths(graph, start_node, end_node, k=3):
    """Enhanced Yen's algorithm for finding k shortest paths with comprehensive analysis"""
    # Find all possible paths first
    all_paths = find_all_possible_paths(graph, start_node, end_node)
    
    if not all_paths:
        return []
    
    # Limit to k paths for performance
    selected_paths = all_paths[:min(k, len(all_paths))]
    
    # Convert to the expected format
    result = []
    for path, distance in selected_paths:
        route_info = {
            'path': path,
            'distance': distance,
            'steps': [],
            'algorithm': 'Enhanced Path Finding with DFS'
        }
        result.append(route_info)
    
    return result

@app.route('/')
def index():
    """Serve main HTML page"""
    return send_from_directory('/Users/mac/Desktop/school/final-year/UNILAG-Campus-Navigation/frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve static files"""
    return send_from_directory('/Users/mac/Desktop/school/final-year/UNILAG-Campus-Navigation/frontend', path)

@app.route('/api/campus-data')
def get_campus_data():
    """Return campus nodes, edges, and coordinates"""
    data = load_campus_data()
    return jsonify(data)

@app.route('/api/shortest-path', methods=['POST'])
def find_shortest_path():
    """Find shortest path with enhanced algorithm similar to reference implementation"""
    try:
        request_data = request.get_json()
        start_location = request_data.get('start')
        end_location = request_data.get('end')
        
        if not start_location or not end_location:
            return jsonify({'error': 'Both start and end locations are required'}), 400
        
        # Load campus data
        campus_data = load_campus_data()
        
        # Verify locations exist
        if start_location not in campus_data['nodes'] or end_location not in campus_data['nodes']:
            return jsonify({'error': 'One or both locations not found in campus data'}), 400
        
        # Build enhanced graph similar to reference create_graph function
        print(f"Building enhanced graph for route from {start_location} to {end_location}")
        enhanced_graph, connected_nodes = build_enhanced_graph(campus_data['nodes'], campus_data['coordinates'])
        
        if start_location not in enhanced_graph:
            return jsonify({'error': f'No connections found for {start_location}'}), 404
        
        if end_location not in enhanced_graph:
            return jsonify({'error': f'No connections found for {end_location}'}), 404
        
        # Find shortest path using enhanced algorithm similar to reference dijkstra_algorithm
        result = enhanced_dijkstra_algorithm(start_location, end_location, enhanced_graph, track_steps=True)
        
        if not result['path'] or len(result['path']) == 0 or result['path'][0] != start_location:
            return jsonify({
                'error': 'No path found between the specified locations',
                'path': [],
                'total_distance': 0,
                'algorithm_steps': []
            }), 404
        
        # Find all possible paths for comprehensive analysis (with timeout protection)
        print(f"Finding comprehensive analysis for {start_location} to {end_location}")
        try:
            all_paths = find_all_possible_paths(enhanced_graph, start_location, end_location, max_depth=5, max_paths=20)
            comprehensive_analysis = create_comprehensive_analysis(all_paths, start_location, end_location)
            print(f"Found {len(all_paths)} possible paths for analysis")
        except Exception as e:
            print(f"Error in comprehensive analysis: {e}, using fallback")
            all_paths = [(result['path'], result['distance'])]
            comprehensive_analysis = {}
        
        # Get coordinates for the path
        coordinates = campus_data['coordinates']
        path_coordinates = get_path_coordinates(result['path'], coordinates)
        
        # Calculate metrics
        total_distance_km = result['distance']
        total_distance_m = total_distance_km * 1000
        walking_time = max(1, int(total_distance_m / 80))  # Assume 80m/min walking speed
        academic_buildings = len([p for p in result['path'] if any(keyword in p for keyword in ['Faculty', 'Department', 'School', 'College'])])
        
        print(f"The shortest distance is {total_distance_km:.2f}km (similar to reference output)")
        
        return jsonify({
            'path': result['path'],
            'path_coordinates': path_coordinates,
            'total_distance': round(total_distance_m, 2),
            'total_distance_km': round(total_distance_km, 3),
            'walking_time_minutes': walking_time,
            'academic_buildings_passed': academic_buildings,
            'algorithm_steps': result['steps'],
            'nodes_explored': len([step for step in result['steps'] if step.get('action') == 'visit_node']),
            'connected_nodes_count': len(connected_nodes),
            'comprehensive_analysis': comprehensive_analysis,
            'all_possible_paths': len(all_paths),
            'optimization_info': {
                'algorithm': 'Enhanced Dijkstra (Reference-Style Implementation)',
                'guaranteed_optimal': True,
                'why_optimal': 'Uses proximity-based graph building and classic Dijkstra approach',
                'time_complexity': 'O(V²) - similar to reference implementation',
                'distance_metric': 'Haversine distance (equivalent to geopy.distance.geodesic)',
                'reference_similarity': 'Based on pandas-style graph building with proximity filtering'
            }
        })
        
    except Exception as e:
        print(f"Error in find_shortest_path: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/alternative-routes', methods=['POST'])
def find_alternative_routes():
    """Find all possible alternative routes using comprehensive path analysis"""
    try:
        data = request.json
        start_location = data.get('start')
        end_location = data.get('end') 
        k = data.get('k', 5)  # Number of alternative routes to show
        
        if not start_location or not end_location:
            return jsonify({'error': 'Start and end locations are required'}), 400
        
        # Load campus data and build enhanced graph
        campus_data = load_campus_data()
        enhanced_graph, connected_nodes = build_enhanced_graph(campus_data['nodes'], campus_data['coordinates'])
        
        if start_location not in enhanced_graph or end_location not in enhanced_graph:
            return jsonify({'error': 'Start or end location not connected in graph'}), 404
        
        # Find all possible paths using comprehensive approach
        all_paths = find_all_possible_paths(enhanced_graph, start_location, end_location)
        
        if not all_paths:
            return jsonify({'error': 'No alternative routes found'}), 404
        
        # Get comprehensive analysis
        comprehensive_analysis = create_comprehensive_analysis(all_paths, start_location, end_location)
        
        # Limit to k most diverse routes
        selected_paths = all_paths[:min(k, len(all_paths))]
        
        # Prepare route information
        routes = []
        coordinates = campus_data['coordinates']
        
        for i, (path, distance) in enumerate(selected_paths):
            route_info = {
                'path': path,
                'distance': round(distance, 3),
                'distance_km': round(distance, 3),
                'distance_m': round(distance * 1000, 2),
                'walking_time_minutes': max(1, int(distance * 1000 / 80)),
                'path_coordinates': get_path_coordinates(path, coordinates),
                'route_rank': i + 1,
                'is_optimal': i == 0,
                'algorithm': 'Enhanced Path Finding with DFS'
            }
            routes.append(route_info)
        
        return jsonify({
            'routes': routes,
            'comprehensive_analysis': comprehensive_analysis,
            'total_possible_paths': len(all_paths),
            'showing_top': len(selected_paths),
            'connected_nodes': len(connected_nodes),
            'algorithm': 'Comprehensive Path Analysis with DFS Exploration'
        })
    
    except Exception as e:
        print(f"Error in find_alternative_routes: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/emergency-route', methods=['POST'])
def find_emergency_route():
    """Find emergency route to nearest appropriate destination"""
    try:
        data = request.json
        start_location = data.get('start')
        emergency_type = data.get('emergency_type', 'medical')
        
        if not start_location:
            return jsonify({'error': 'Start location is required'}), 400
        
        # Load campus data and build graph
        campus_data = load_campus_data()
        graph = build_graph(campus_data['edges'])
        
        # Emergency destinations based on type
        emergency_destinations = {
            'medical': ['Health Centre', 'Medical Centre', 'Administrative Block'],
            'security': ['Security Post', 'Main Gate', 'Administrative Block'],
            'fire': ['Main Gate', 'Security Post', 'Administrative Block'],
            'evacuation': ['Main Gate', 'Sports Complex', 'University Library']
        }
        
        destinations = emergency_destinations.get(emergency_type, ['Main Gate'])
        best_route = None
        shortest_distance = float('inf')
        
        # Find the closest emergency destination
        for dest in destinations:
            if dest in graph:
                result = dijkstra_with_steps(graph, start_location, dest)
                if result['path'] and result['distance'] < shortest_distance:
                    shortest_distance = result['distance']
                    coordinates = campus_data['coordinates']
                    path_coordinates = []
                    for location in result['path']:
                        if location in coordinates:
                            path_coordinates.append(coordinates[location])
                    
                    best_route = {
                        'path': result['path'],
                        'total_distance': int(result['distance']),
                        'path_coordinates': path_coordinates,
                        'algorithm_steps': result['steps'],
                        'emergency_type': emergency_type,
                        'destination_type': dest,
                        'priority': 'HIGH',
                        'estimated_time': max(1, int(result['distance'] / 120))  # Faster walking for emergency
                    }
        
        if not best_route:
            return jsonify({'error': 'No emergency route found'}), 404
        
        return jsonify(best_route)
    
    except Exception as e:
        print(f"Error in find_emergency_route: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/nodes', methods=['GET'])
def get_all_nodes():
    """Get all available campus nodes/locations"""
    try:
        campus_data = load_campus_data()
        return jsonify({
            'nodes': campus_data.get('nodes', []),
            'count': len(campus_data.get('nodes', [])),
            'coordinates': campus_data.get('coordinates', {})
        })
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Starting UNILAG Campus Navigation Server...")
    print("📍 Loading campus data...")
    
    # Verify data file exists
    data_file = '/Users/mac/Desktop/school/final-year/UNILAG-Campus-Navigation/backend/data/campus_nodes_edges.json'
    if os.path.exists(data_file):
        data = load_campus_data()
        print(f"✅ Loaded {len(data.get('nodes', []))} campus locations")
        print(f"✅ Loaded {len(data.get('edges', []))} connections")
        print(f"✅ Loaded {len(data.get('coordinates', {}))} coordinate mappings")
    else:
        print(f"❌ Error: {data_file} not found")
    
    print("🌐 Server starting on http://localhost:5001")
    app.run(debug=True, port=5001)
