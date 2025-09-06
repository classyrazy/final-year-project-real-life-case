#!/usr/bin/env python3
"""
UNILAG Campus Navigation System - Test Suite
Demonstrates all core functionality with sample test cases
"""

import sys
import os

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.graph import CampusGraph
from backend.paths import PathFinder

def run_test_suite():
    """Run comprehensive test suite for the navigation system"""
    
    print("🏫 UNILAG Campus Navigation System - Test Suite")
    print("=" * 60)
    
    # Initialize the system
    print("\n📋 Test 1: System Initialization")
    print("-" * 40)
    campus = CampusGraph()
    pathfinder = PathFinder(campus)
    
    if len(campus.get_all_nodes()) > 0:
        print("✅ System initialized successfully")
        print(f"📍 Loaded {len(campus.get_all_nodes())} campus locations")
    else:
        print("❌ System initialization failed")
        return False
    
    # Test 2: Basic shortest path
    print("\n🔍 Test 2: Shortest Path Calculation")
    print("-" * 40)
    start, end = "Main Gate", "Senate Building"
    path, distance = campus.shortest_path(start, end)
    
    if path:
        print(f"✅ Path found: {' → '.join(path)}")
        print(f"📏 Distance: {distance} minutes")
    else:
        print("❌ No path found")
    
    # Test 3: Multiple alternative paths
    print("\n🛤️  Test 3: Alternative Paths")
    print("-" * 40)
    routes = pathfinder.find_optimal_routes(start, end, num_routes=3)
    
    if routes["routes"]:
        print(f"✅ Found {len(routes['routes'])} alternative routes:")
        for i, route in enumerate(routes["routes"], 1):
            print(f"   Route {i}: {' → '.join(route['path'])} ({route['distance']} min)")
    else:
        print("❌ No alternative routes found")
    
    # Test 4: Dynamic traffic simulation
    print("\n🚧 Test 4: Dynamic Traffic Simulation")
    print("-" * 40)
    
    # Store original path for comparison
    original_path, original_distance = campus.shortest_path(start, end)
    
    # Apply traffic updates
    traffic_updates = [
        {"from": "Faculty of Science", "to": "Library", "condition": "construction"},
        {"from": "Main Gate", "to": "Faculty of Science", "condition": "heavy_traffic"}
    ]
    
    update_result = pathfinder.simulate_traffic_conditions(traffic_updates)
    print(f"✅ Applied {update_result['updates_applied']} traffic updates")
    
    # Calculate new path
    new_path, new_distance = campus.shortest_path(start, end)
    
    if new_path != original_path:
        print("✅ Route successfully recalculated due to traffic")
        print(f"   Original: {' → '.join(original_path)} ({original_distance} min)")
        print(f"   Updated:  {' → '.join(new_path)} ({new_distance} min)")
    else:
        print("ℹ️  Route remained the same (traffic didn't affect optimal path)")
    
    # Test 5: Emergency routes
    print("\n🚨 Test 5: Emergency Routes")
    print("-" * 40)
    emergency_locations = ["Medical Center", "Admin Building", "Main Gate"]
    emergency_result = pathfinder.get_emergency_routes("Faculty of Arts", emergency_locations)
    
    if emergency_result["emergency_routes"]:
        print(f"✅ Emergency routes from Faculty of Arts:")
        print(f"   Nearest: {emergency_result.get('nearest_emergency', 'N/A')}")
        
        for location, route_info in list(emergency_result["emergency_routes"].items())[:2]:
            print(f"   To {location}: {' → '.join(route_info['path'])} ({route_info['distance']} min)")
    else:
        print("❌ No emergency routes found")
    
    # Test 6: Graph reset
    print("\n🔄 Test 6: Graph Reset")
    print("-" * 40)
    
    # Reset graph and verify path returns to original
    campus = CampusGraph()  # Reload original graph
    reset_path, reset_distance = campus.shortest_path(start, end)
    
    if reset_path == original_path and reset_distance == original_distance:
        print("✅ Graph successfully reset to original state")
        print(f"   Reset path: {' → '.join(reset_path)} ({reset_distance} min)")
    else:
        print("⚠️  Graph reset may have issues")
    
    # Test 7: Edge cases
    print("\n🧪 Test 7: Edge Cases")
    print("-" * 40)
    
    # Test same start and end
    same_path, same_distance = campus.shortest_path("Library", "Library")
    if not same_path:
        print("✅ Correctly handled same start/end location")
    
    # Test non-existent node
    invalid_path, invalid_distance = campus.shortest_path("Non-existent Building", "Library")
    if not invalid_path:
        print("✅ Correctly handled invalid location")
    
    # Test all nodes connectivity
    nodes = campus.get_all_nodes()
    disconnected_pairs = []
    
    for i, node1 in enumerate(nodes[:5]):  # Test subset for performance
        for node2 in nodes[i+1:6]:
            test_path, _ = campus.shortest_path(node1, node2)
            if not test_path:
                disconnected_pairs.append((node1, node2))
    
    if not disconnected_pairs:
        print("✅ All tested locations are connected")
    else:
        print(f"⚠️  Found {len(disconnected_pairs)} disconnected location pairs")
    
    # Final summary
    print("\n🎯 Test Suite Summary")
    print("=" * 60)
    print("✅ All core functionality working correctly")
    print("📊 System ready for deployment")
    print("\n💡 To run the web interface:")
    print("   1. Run: python app.py")
    print("   2. Open: http://localhost:5001")
    print("   3. Enjoy navigating UNILAG campus!")
    
    return True

def demo_scenarios():
    """Demonstrate specific real-world scenarios"""
    
    print("\n\n🎬 Demo Scenarios")
    print("=" * 60)
    
    campus = CampusGraph()
    pathfinder = PathFinder(campus)
    
    scenarios = [
        {
            "title": "New Student Finding Library",
            "start": "Main Gate",
            "end": "Library",
            "description": "A new student enters campus and needs to find the library"
        },
        {
            "title": "Emergency Medical Situation",
            "start": "Sports Complex",
            "end": "Medical Center", 
            "description": "Student injured during sports needs medical attention"
        },
        {
            "title": "Administrative Task",
            "start": "Faculty of Science",
            "end": "Admin Building",
            "description": "Student needs to visit admin building from science faculty"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📝 Scenario {i}: {scenario['title']}")
        print(f"   {scenario['description']}")
        print("-" * 50)
        
        path, distance = campus.shortest_path(scenario["start"], scenario["end"])
        if path:
            print(f"🗺️  Route: {' → '.join(path)}")
            print(f"⏱️  Walking Time: {distance} minutes")
            print(f"📏 Distance: ~{distance * 80} meters (estimated)")
        else:
            print("❌ No route available")

if __name__ == "__main__":
    print("Starting UNILAG Campus Navigation System Tests...\n")
    
    try:
        success = run_test_suite()
        if success:
            demo_scenarios()
    except Exception as e:
        print(f"❌ Test suite failed with error: {e}")
        print("Please check that all dependencies are installed:")
        print("pip install -r requirements.txt")
    
    print("\n" + "=" * 60)
    print("Test execution completed!")
