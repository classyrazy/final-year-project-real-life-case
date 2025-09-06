from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import sys

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.graph import CampusGraph
from backend.paths import PathFinder

# Initialize Flask app
app = Flask(__name__, 
           static_folder='frontend',
           template_folder='frontend')
CORS(app)  # Enable CORS for frontend-backend communication

# Initialize the campus navigation system
campus = CampusGraph()
pathfinder = PathFinder(campus)

# Routes for serving frontend files
@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/frontend/<path:filename>')
def serve_static(filename):
    """Serve static frontend files"""
    return send_from_directory('frontend', filename)

# API Routes for navigation functionality

@app.route('/api/nodes', methods=['GET'])
def get_all_nodes():
    """Get all available campus locations"""
    try:
        nodes = campus.get_all_nodes()
        coordinates = campus.get_all_coordinates()
        
        return jsonify({
            "success": True,
            "nodes": sorted(nodes),
            "coordinates": coordinates,
            "total_count": len(nodes)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/shortest-path', methods=['GET'])
def get_shortest_path():
    """Get the shortest path between two locations"""
    try:
        start = request.args.get('start')
        end = request.args.get('end')
        
        if not start or not end:
            return jsonify({
                "success": False,
                "error": "Both 'start' and 'end' parameters are required"
            }), 400
        
        path, distance = campus.shortest_path(start, end)
        
        if not path:
            return jsonify({
                "success": False,
                "error": f"No path found between '{start}' and '{end}'"
            }), 404
        
        # Get coordinates for the path
        coordinates = [campus.get_node_coordinates(node) for node in path]
        
        return jsonify({
            "success": True,
            "start": start,
            "end": end,
            "path": path,
            "distance": distance,
            "estimated_time": round(distance * 1.2, 1),
            "coordinates": coordinates
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/multiple-paths', methods=['GET'])
def get_multiple_paths():
    """Get multiple alternative paths between two locations"""
    try:
        start = request.args.get('start')
        end = request.args.get('end')
        k = int(request.args.get('k', 3))  # Default to 3 paths
        
        if not start or not end:
            return jsonify({
                "success": False,
                "error": "Both 'start' and 'end' parameters are required"
            }), 400
        
        routes = pathfinder.find_optimal_routes(start, end, num_routes=k)
        
        return jsonify({
            "success": True,
            "data": routes
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/route-preferences', methods=['POST'])
def get_route_with_preferences():
    """Get routes based on user preferences"""
    try:
        data = request.get_json()
        start = data.get('start')
        end = data.get('end')
        preferences = data.get('preferences', {})
        
        if not start or not end:
            return jsonify({
                "success": False,
                "error": "Both 'start' and 'end' are required"
            }), 400
        
        routes = pathfinder.get_route_alternatives_with_preferences(start, end, preferences)
        
        return jsonify({
            "success": True,
            "data": routes
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/traffic-update', methods=['POST'])
def apply_traffic_updates():
    """Apply dynamic traffic/construction updates"""
    try:
        data = request.get_json()
        traffic_updates = data.get('updates', [])
        
        if not traffic_updates:
            return jsonify({
                "success": False,
                "error": "No traffic updates provided"
            }), 400
        
        result = pathfinder.simulate_traffic_conditions(traffic_updates)
        
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/emergency-routes', methods=['GET'])
def get_emergency_routes():
    """Get emergency routes from current location"""
    try:
        start = request.args.get('start')
        emergency_locations = ["Medical Center", "Admin Building", "Security Post", "Main Gate"]
        
        if not start:
            return jsonify({
                "success": False,
                "error": "'start' parameter is required"
            }), 400
        
        # Filter emergency locations to only include those that exist in the graph
        available_emergency = [loc for loc in emergency_locations if loc in campus.get_all_nodes()]
        
        routes = pathfinder.get_emergency_routes(start, available_emergency)
        
        return jsonify({
            "success": True,
            "data": routes
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/reset-graph', methods=['POST'])
def reset_graph():
    """Reset the graph to original state (remove all dynamic updates)"""
    try:
        global campus, pathfinder
        campus = CampusGraph()  # Reload original graph
        pathfinder = PathFinder(campus)
        
        return jsonify({
            "success": True,
            "message": "Graph reset to original state"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/graph-info', methods=['GET'])
def get_graph_info():
    """Get basic information about the campus graph"""
    try:
        nodes = campus.get_all_nodes()
        edges_count = len(campus.graph.edges())
        
        return jsonify({
            "success": True,
            "data": {
                "total_nodes": len(nodes),
                "total_edges": edges_count,
                "nodes": sorted(nodes),
                "description": "UNILAG Campus Navigation Graph",
                "last_updated": "2025-09-05"
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

# Development configuration
if __name__ == '__main__':
    print("🏫 UNILAG Campus Navigation System Starting...")
    print("📍 Graph loaded with {} nodes".format(len(campus.get_all_nodes())))
    print("🌐 Server starting on http://localhost:8080")
    print("📱 Open http://localhost:8080 in your browser")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=8080)
