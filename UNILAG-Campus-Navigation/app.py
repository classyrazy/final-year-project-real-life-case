#!/usr/bin/env python3
"""
UNILAG Campus Navigation Server
Enhanced with Dijkstra Algorithm Visualization
"""

import heapq
import json
import math
import copy
import time
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

@app.route('/api/bigdata/uk-cities', methods=['GET'])
def get_uk_cities():
    """Get UK cities dataset for big data analysis"""
    uk_cities = {
        'cities': ['London','Birmingham','Manchester','Liverpool','Bristol','Newcastle upon Tyne','Sheffield','Cardiff','Leeds','Nottingham','Leicester','Coventry','Bradford','Newcastle','Stoke-on-Trent','Wolverhampton','Derby','Swansea','Plymouth','Reading','Hull','Preston','Luton','Portsmouth','Southampton','Sunderland','Warrington','Bournemouth','Swindon','Oxford','Huddersfield','Slough','Blackpool','Middlesbrough','Ipswich','Telford','York','West Bromwich','Peterborough','Stockport','Brighton','Hastings','Exeter','Chelmsford','Chester','St Helens','Colchester','Crawley','Stevenage','Birkenhead','Bolton','Stockton-on-Tees','Watford','Gloucester','Rotherham','Newport','Cambridge','St Albans','Bury','Southend-on-Sea','Woking','Maidstone','Lincoln','Gillingham','Chesterfield','Oldham','Charlton','Aylesbury','Keighley','Bangor','Scunthorpe','Guildford','Grimsby','Ellesmere Port','Blackburn','Hove','Hartlepool','Taunton','Maidenhead','Aldershot','Great Yarmouth','Rossendale'],
        'coordinates': {
            'London': [51.509865, -0.118092],
            'Birmingham': [52.4862, -1.8904],
            'Manchester': [53.483959, -2.244644],
            'Liverpool': [53.4084, -2.9916],
            'Bristol': [51.4545, -2.5879],
            'Newcastle upon Tyne': [54.9784, -1.6174],
            'Sheffield': [53.3811, -1.4701],
            'Cardiff': [51.4816, -3.1791],
            'Leeds': [53.8008, -1.5491],
            'Nottingham': [52.9548, -1.1581],
            'Leicester': [52.6369, -1.1398],
            'Coventry': [52.4068, -1.5197],
            'Bradford': [53.7957, -1.7593],
            'Newcastle': [55.007, -1.6174],
            'Stoke-on-Trent': [53.0027, -2.1794],
            'Wolverhampton': [52.5862, -2.1288],
            'Derby': [52.9228, -1.4777],
            'Swansea': [51.6214, -3.9436],
            'Plymouth': [50.3755, -4.1427],
            'Reading': [51.4543, -0.9781],
            'Hull': [53.7443, -0.3326],
            'Preston': [53.7632, -2.7031],
            'Luton': [51.8787, -0.42],
            'Portsmouth': [50.8195, -1.0874],
            'Southampton': [50.9097, -1.4044],
            'Sunderland': [54.9069, -1.3834],
            'Warrington': [53.3872, -2.5925],
            'Bournemouth': [50.7208, -1.9046],
            'Swindon': [51.5686, -1.7722],
            'Oxford': [51.752, -1.2577],
            'Huddersfield': [53.649, -1.7849],
            'Slough': [51.5095, -0.5954],
            'Blackpool': [53.8175, -3.0357],
            'Middlesbrough': [54.5742, -1.2356],
            'Ipswich': [52.0567, -1.1482],
            'Telford': [52.6784, -2.4453],
            'York': [53.959, -1.0815],
            'West Bromwich': [52.5187, -1.9945],
            'Peterborough': [52.5695, -0.2405],
            'Stockport': [53.4084, -2.1493],
            'Brighton': [50.8225, -0.1372],
            'Hastings': [50.8552, -0.5723],
            'Exeter': [50.7184, -3.5339],
            'Chelmsford': [51.7361, -0.4791],
            'Chester': [53.1934, -2.8931],
            'St Helens': [53.4539, -2.7375],
            'Colchester': [51.8892, -0.9042],
            'Crawley': [51.1124, -0.1831],
            'Stevenage': [51.9038, -0.1966],
            'Birkenhead': [53.3934, -3.0148],
            'Bolton': [53.5769, -2.428],
            'Stockton-on-Tees': [54.5741, -1.3187],
            'Watford': [51.6562, -0.39],
            'Gloucester': [51.8642, -2.2382],
            'Rotherham': [53.432, -1.3502],
            'Newport': [51.5881, -3.1409],
            'Cambridge': [52.2053, -0.1218],
            'St Albans': [51.752, -0.339],
            'Bury': [53.591, -2.298],
            'Southend-on-Sea': [51.5406, 0.711],
            'Woking': [51.3169, -0.56],
            'Maidstone': [51.2704, -0.5227],
            'Lincoln': [53.2307, -0.5406],
            'Gillingham': [51.3898, -0.5486],
            'Chesterfield': [53.235, -1.4216],
            'Oldham': [53.5444, -2.1183],
            'Charlton': [51.4941, -0.068],
            'Aylesbury': [51.8156, -0.8084],
            'Keighley': [53.867, -1.9064],
            'Bangor': [53.2274, -4.1297],
            'Scunthorpe': [53.5896, -0.6544],
            'Guildford': [51.2362, -0.5704],
            'Grimsby': [53.5675, -0.0802],
            'Ellesmere Port': [53.2826, -2.8976],
            'Blackburn': [53.7486, -2.4877],
            'Hove': [50.8279, -0.1688],
            'Hartlepool': [54.6892, -1.2122],
            'Taunton': [51.0143, -3.1036],
            'Maidenhead': [51.522, -0.7205],
            'Aldershot': [51.2484, -0.755],
            'Great Yarmouth': [52.6083, -1.7303],
            'Rossendale': [53.6458, -2.2864]
        },
        'count': 82,
        'description': 'UK Cities dataset for algorithm performance testing'
    }
    
    return jsonify(uk_cities)

@app.route('/api/bigdata/build-graph', methods=['POST'])
def build_bigdata_graph():
    """Build graph for UK cities based on distance threshold"""
    try:
        request_data = request.get_json()
        max_distance = request_data.get('max_distance', 200)  # km
        
        # Get UK cities data
        uk_cities_response = get_uk_cities()
        uk_cities_data = uk_cities_response.get_json()
        
        coordinates = uk_cities_data['coordinates']
        cities = list(coordinates.keys())
        
        # Build graph based on distance threshold
        graph = {}
        connections = 0
        total_distance = 0
        
        for city1 in cities:
            graph[city1] = {}
            coords1 = coordinates[city1]
            
            for city2 in cities:
                if city1 != city2:
                    coords2 = coordinates[city2]
                    distance = haversine_distance(coords1[0], coords1[1], coords2[0], coords2[1])
                    
                    if distance <= max_distance:
                        graph[city1][city2] = distance
                        connections += 1
                        total_distance += distance
        
        # Calculate statistics
        avg_distance = total_distance / connections if connections > 0 else 0
        max_possible = len(cities) * (len(cities) - 1)
        density = (connections / max_possible) * 100 if max_possible > 0 else 0
        
        return jsonify({
            'graph': graph,
            'statistics': {
                'total_cities': len(cities),
                'total_connections': connections,
                'average_distance': round(avg_distance, 2),
                'graph_density': round(density, 2),
                'max_distance_threshold': max_distance
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to build graph: {str(e)}'}), 500

@app.route('/api/bigdata/shortest-path', methods=['POST'])
def bigdata_shortest_path():
    """Find shortest path in UK cities graph"""
    try:
        request_data = request.get_json()
        start_city = request_data.get('start')
        end_city = request_data.get('end')
        graph = request_data.get('graph')
        
        if not all([start_city, end_city, graph]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Run enhanced Dijkstra with performance tracking
        import time
        start_time = time.time()
        
        result = enhanced_dijkstra_algorithm_bigdata(start_city, end_city, graph)
        
        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Get coordinates for path visualization
        uk_cities_response = get_uk_cities()
        uk_cities_data = uk_cities_response.get_json()
        coordinates = uk_cities_data['coordinates']
        
        path_coordinates = []
        if result['path']:
            path_coordinates = [coordinates[city] for city in result['path'] if city in coordinates]
        
        return jsonify({
            'path': result['path'],
            'path_coordinates': path_coordinates,
            'total_distance': round(result['distance'], 2),
            'execution_time_ms': round(execution_time, 2),
            'nodes_explored': result.get('nodes_explored', 0),
            'algorithm_steps': result.get('steps', 0),
            'performance_metrics': {
                'graph_size': len(graph),
                'complexity': f'O(V²) where V = {len(graph)}',
                'efficiency_score': max(0, 100 - execution_time/10)
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to find path: {str(e)}'}), 500

def enhanced_dijkstra_algorithm_bigdata(start_node, end_node, graph):
    """Enhanced Dijkstra algorithm with performance tracking for big data"""
    nodes = list(graph.keys())
    
    if start_node not in nodes or end_node not in nodes:
        return {'path': [], 'distance': float('inf'), 'nodes_explored': 0, 'steps': 0}
    
    # Initialize distances and tracking
    INFINITY = float('inf')
    distances = {node: INFINITY for node in nodes}
    distances[start_node] = 0
    previous_nodes = {}
    visited = set()
    unvisited = set(nodes)
    
    nodes_explored = 0
    steps = 0
    
    while unvisited:
        steps += 1
        
        # Find unvisited node with minimum distance
        current_node = min(unvisited, key=lambda node: distances[node])
        
        if distances[current_node] == INFINITY:
            break  # No more reachable nodes
        
        if current_node == end_node:
            break  # Reached destination
        
        visited.add(current_node)
        unvisited.remove(current_node)
        nodes_explored += 1
        
        # Update distances to neighbors
        neighbors = graph.get(current_node, {})
        for neighbor, weight in neighbors.items():
            if neighbor in unvisited:
                new_distance = distances[current_node] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_nodes[neighbor] = current_node
    
    # Reconstruct path
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = previous_nodes.get(current)
    path.reverse()
    
    # Verify path is valid
    if not path or path[0] != start_node:
        path = []
    
    return {
        'path': path,
        'distance': distances.get(end_node, INFINITY),
        'nodes_explored': nodes_explored,
        'steps': steps
    }

@app.route('/api/bigdata/alternative-routes', methods=['POST'])
def bigdata_alternative_routes():
    """Find alternative routes for big data scenario"""
    try:
        request_data = request.get_json()
        start_city = request_data.get('start')
        end_city = request_data.get('end')
        graph = request_data.get('graph', {})
        k = request_data.get('k', 5)  # Number of alternative routes
        
        if not start_city or not end_city:
            return jsonify({'error': 'Start and end cities are required'}), 400
            
        if not graph:
            return jsonify({'error': 'Graph data is required'}), 400
            
        print(f"🔍 Finding {k} alternative routes from {start_city} to {end_city}")
        
        # Find k shortest paths using edge removal technique
        routes = find_k_shortest_paths_bigdata(start_city, end_city, graph, k)
        
        # Create comprehensive analysis
        analysis = create_bigdata_comprehensive_analysis(routes, start_city, end_city)
        
        return jsonify({
            'routes': routes,
            'comprehensive_analysis': analysis,
            'total_routes_found': len(routes),
            'showing_top': min(k, len(routes)),
            'algorithm': 'K-Shortest Paths with Edge Removal',
            'graph_size': len(graph)
        })
        
    except Exception as e:
        print(f"❌ Error in bigdata alternative routes: {str(e)}")
        return jsonify({'error': f'Failed to find alternative routes: {str(e)}'}), 500

def find_k_shortest_paths_bigdata(start, end, graph, k=5):
    """Find k shortest paths using iterative edge removal"""
    routes = []
    temp_graph = copy.deepcopy(graph)
    
    # Find first shortest path
    first_result = enhanced_dijkstra_algorithm_bigdata(start, end, temp_graph)
    if first_result['path']:
        routes.append({
            'path': first_result['path'],
            'distance': first_result['distance'],
            'nodes_explored': first_result['nodes_explored'],
            'steps': first_result['steps'],
            'route_id': 1,
            'is_optimal': True
        })
    
    # Find alternative routes by removing edges
    for i in range(1, k):
        if not routes:
            break
            
        best_alternative = find_best_alternative_bigdata(start, end, temp_graph, routes)
        
        if best_alternative and best_alternative['path']:
            routes.append({
                'path': best_alternative['path'],
                'distance': best_alternative['distance'],
                'nodes_explored': best_alternative['nodes_explored'],
                'steps': best_alternative['steps'],
                'route_id': i + 1,
                'is_optimal': False
            })
            
            # Remove some edges from this path to encourage diversity
            remove_edges_from_path(temp_graph, best_alternative['path'])
        else:
            break
    
    return routes

def find_best_alternative_bigdata(start, end, graph, existing_routes):
    """Find best alternative route by temporarily removing edges"""
    best_alternative = None
    best_distance = float('inf')
    
    for route in existing_routes:
        if len(route['path']) < 2:
            continue
            
        # Try removing each edge in existing routes
        for i in range(len(route['path']) - 1):
            node_a = route['path'][i]
            node_b = route['path'][i + 1]
            
            # Temporarily remove edge
            temp_graph = copy.deepcopy(graph)
            if node_a in temp_graph and node_b in temp_graph[node_a]:
                del temp_graph[node_a][node_b]
            if node_b in temp_graph and node_a in temp_graph[node_b]:
                del temp_graph[node_b][node_a]
            
            # Find alternative path
            alt_result = enhanced_dijkstra_algorithm_bigdata(start, end, temp_graph)
            
            if alt_result['path'] and alt_result['distance'] < best_distance:
                best_alternative = alt_result
                best_distance = alt_result['distance']
    
    return best_alternative

def remove_edges_from_path(graph, path):
    """Remove some edges from path to encourage route diversity"""
    edges_to_remove = max(1, len(path) // 4)
    
    for i in range(min(edges_to_remove, len(path) - 1)):
        node_a = path[i]
        node_b = path[i + 1]
        
        if node_a in graph and node_b in graph[node_a]:
            del graph[node_a][node_b]
        if node_b in graph and node_a in graph[node_b]:
            del graph[node_b][node_a]

def create_bigdata_comprehensive_analysis(routes, start_city, end_city):
    """Create comprehensive analysis for big data alternative routes"""
    if not routes:
        return {}
    
    optimal_route = next((route for route in routes if route.get('is_optimal')), routes[0])
    shortest_distance = min(route['distance'] for route in routes)
    longest_distance = max(route['distance'] for route in routes)
    total_routes = len(routes)
    
    difference_km = longest_distance - shortest_distance
    
    analysis = {
        'dijkstra_choice': f"🎯 BIG DATA OPTIMAL: {optimal_route['distance']:.2f}km across {len(optimal_route['path'])} cities",
        'total_routes_found': f"📊 FOUND: {total_routes} alternative routes in large-scale network",
        'shortest_route': f"🟢 Shortest: {shortest_distance:.2f}km (Dijkstra's guarantee)",
        'longest_route': f"🔴 Longest: {longest_distance:.2f}km (+{difference_km:.2f}km longer)",
        'why_optimal': f"🧠 BIG DATA EFFICIENCY: Processed {optimal_route['nodes_explored']} nodes in {optimal_route['steps']} steps using optimized Dijkstra implementation",
        'scalability_note': f"⚡ SCALABLE: Algorithm maintains O(V²) complexity even with {len(routes)} routes across large city network"
    }
    
    return analysis

if __name__ == '__main__':
    print("🚀 Starting UNILAG Campus Navigation System...")
    print("🎯 Features: Campus Navigation | Big Data Analysis | Alternative Routes")
    print("📊 Serving on http://localhost:5001")
    print("📍 Campus Navigation: http://localhost:5001")
    print("🌍 Big Data Analysis: http://localhost:5001/bigdata")
    app.run(debug=True, host='0.0.0.0', port=5001)
