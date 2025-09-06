#!/usr/bin/env python3
"""
UNILAG Campus Coordinates Verification Script
============================================

This script verifies the coordinates of UNILAG campus locations by:
1. Checking if coordinates are within Lagos, Nigeria boundaries
2. Validating coordinate ranges for the campus area
3. Cross-referencing with known UNILAG landmarks
4. Analyzing coordinate clustering and distances
5. Providing recommendations for coordinate corrections
"""

import json
import math
from typing import Dict, List, Tuple, Any

def load_campus_data(file_path: str) -> Dict[str, Any]:
    """Load campus nodes and coordinates data."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}")
        return {}

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates using Haversine formula."""
    R = 6371000  # Earth's radius in meters
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(delta_lon/2) * math.sin(delta_lon/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def verify_coordinates_boundaries(coordinates: Dict[str, List[float]]) -> Dict[str, Any]:
    """Verify that all coordinates are within reasonable UNILAG campus boundaries."""
    # UNILAG campus approximate boundaries (from research)
    # Main campus at Akoka, Yaba, Lagos
    UNILAG_BOUNDS = {
        'min_lat': 6.510,    # Southern boundary
        'max_lat': 6.525,    # Northern boundary  
        'min_lon': 3.380,    # Western boundary
        'max_lon': 3.400     # Eastern boundary
    }
    
    # Known reference points from research
    REFERENCE_POINTS = {
        'UNILAG_CENTER': [6.5158, 3.3966],  # Approximate center from Wikipedia
        'MAIN_GATE': [6.5158, 3.3966],      # Main entrance
        'LAGOON_FRONT': [6.5139, 3.3875]    # Lagoon area (confirmed from sources)
    }
    
    results = {
        'total_locations': len(coordinates),
        'within_bounds': 0,
        'outside_bounds': [],
        'suspicious_coordinates': [],
        'distance_analysis': {},
        'recommendations': []
    }
    
    # Calculate campus center from our coordinates
    if coordinates:
        lats = [coord[0] for coord in coordinates.values()]
        lons = [coord[1] for coord in coordinates.values()]
        campus_center = [sum(lats)/len(lats), sum(lons)/len(lons)]
        results['calculated_center'] = campus_center
    
    # Verify each coordinate
    for location, coord in coordinates.items():
        lat, lon = coord[0], coord[1]
        
        # Check if within UNILAG boundaries
        if (UNILAG_BOUNDS['min_lat'] <= lat <= UNILAG_BOUNDS['max_lat'] and
            UNILAG_BOUNDS['min_lon'] <= lon <= UNILAG_BOUNDS['max_lon']):
            results['within_bounds'] += 1
        else:
            results['outside_bounds'].append({
                'location': location,
                'coordinates': coord,
                'issue': 'Outside UNILAG campus boundaries'
            })
        
        # Check distance from known reference points
        distances = {}
        for ref_name, ref_coord in REFERENCE_POINTS.items():
            distance = calculate_distance(lat, lon, ref_coord[0], ref_coord[1])
            distances[ref_name] = distance
        
        results['distance_analysis'][location] = distances
        
        # Flag suspicious coordinates (too far from center)
        center_distance = calculate_distance(lat, lon, REFERENCE_POINTS['UNILAG_CENTER'][0], REFERENCE_POINTS['UNILAG_CENTER'][1])
        if center_distance > 2000:  # More than 2km from center
            results['suspicious_coordinates'].append({
                'location': location,
                'coordinates': coord,
                'distance_from_center': center_distance,
                'issue': 'Unusually far from campus center'
            })
    
    return results

def analyze_edges_distances(edges: List[List], coordinates: Dict[str, List[float]]) -> Dict[str, Any]:
    """Analyze edge distances to verify they make sense geographically."""
    results = {
        'total_edges': len(edges),
        'realistic_edges': 0,
        'unrealistic_edges': [],
        'distance_stats': {
            'min_distance': float('inf'),
            'max_distance': 0,
            'avg_distance': 0,
            'distances': []
        }
    }
    
    for edge in edges:
        if len(edge) >= 2:
            loc1, loc2 = edge[0], edge[1]
            if loc1 in coordinates and loc2 in coordinates:
                coord1 = coordinates[loc1]
                coord2 = coordinates[loc2]
                
                # Calculate actual distance
                actual_distance = calculate_distance(coord1[0], coord1[1], coord2[0], coord2[1])
                
                # Get declared distance (if provided)
                declared_distance = edge[2] if len(edge) > 2 else None
                
                results['distance_stats']['distances'].append(actual_distance)
                results['distance_stats']['min_distance'] = min(results['distance_stats']['min_distance'], actual_distance)
                results['distance_stats']['max_distance'] = max(results['distance_stats']['max_distance'], actual_distance)
                
                # Check if edge distance is realistic (between 50m and 1000m for campus)
                if 50 <= actual_distance <= 1000:
                    results['realistic_edges'] += 1
                else:
                    results['unrealistic_edges'].append({
                        'edge': edge,
                        'actual_distance': actual_distance,
                        'declared_distance': declared_distance,
                        'issue': 'Distance outside typical campus range (50m-1000m)'
                    })
    
    # Calculate average distance
    if results['distance_stats']['distances']:
        results['distance_stats']['avg_distance'] = sum(results['distance_stats']['distances']) / len(results['distance_stats']['distances'])
    
    return results

def generate_recommendations(coord_results: Dict, edge_results: Dict) -> List[str]:
    """Generate recommendations based on verification results."""
    recommendations = []
    
    # Coordinate recommendations
    if coord_results['outside_bounds']:
        recommendations.append(f"❌ {len(coord_results['outside_bounds'])} locations are outside UNILAG campus boundaries")
        for item in coord_results['outside_bounds']:
            recommendations.append(f"   • {item['location']}: {item['coordinates']} - {item['issue']}")
    
    if coord_results['suspicious_coordinates']:
        recommendations.append(f"⚠️  {len(coord_results['suspicious_coordinates'])} locations are suspiciously far from campus center")
        for item in coord_results['suspicious_coordinates']:
            recommendations.append(f"   • {item['location']}: {item['distance_from_center']:.0f}m from center")
    
    # Edge recommendations
    if edge_results['unrealistic_edges']:
        recommendations.append(f"❌ {len(edge_results['unrealistic_edges'])} edges have unrealistic distances")
        for item in edge_results['unrealistic_edges'][:5]:  # Show first 5
            recommendations.append(f"   • {item['edge'][0]} ↔ {item['edge'][1]}: {item['actual_distance']:.0f}m")
    
    # Positive feedback
    if coord_results['within_bounds'] == coord_results['total_locations']:
        recommendations.append("✅ All coordinates are within UNILAG campus boundaries")
    
    if edge_results['realistic_edges'] == edge_results['total_edges']:
        recommendations.append("✅ All edge distances are realistic for campus navigation")
    
    # General recommendations
    recommendations.append("\n📍 COORDINATE VERIFICATION SUMMARY:")
    recommendations.append(f"   • Campus center (calculated): {coord_results.get('calculated_center', 'N/A')}")
    recommendations.append(f"   • Locations within bounds: {coord_results['within_bounds']}/{coord_results['total_locations']}")
    recommendations.append(f"   • Realistic edges: {edge_results['realistic_edges']}/{edge_results['total_edges']}")
    recommendations.append(f"   • Average edge distance: {edge_results['distance_stats']['avg_distance']:.0f}m")
    
    return recommendations

def main():
    """Main verification function."""
    print("🔍 UNILAG Campus Coordinates Verification")
    print("=" * 50)
    
    # Load campus data
    campus_data = load_campus_data('../backend/data/campus_nodes_edges.json')
    if not campus_data:
        return
    
    coordinates = campus_data.get('coordinates', {})
    edges = campus_data.get('edges', [])
    nodes = campus_data.get('nodes', [])
    
    print(f"📊 Data Summary:")
    print(f"   • Nodes: {len(nodes)}")
    print(f"   • Edges: {len(edges)}")
    print(f"   • Coordinates: {len(coordinates)}")
    print()
    
    # Verify coordinates
    print("🗺️  Verifying coordinate boundaries...")
    coord_results = verify_coordinates_boundaries(coordinates)
    
    # Analyze edges
    print("📏 Analyzing edge distances...")
    edge_results = analyze_edges_distances(edges, coordinates)
    
    # Generate recommendations
    print("\n📋 VERIFICATION RESULTS:")
    print("-" * 30)
    recommendations = generate_recommendations(coord_results, edge_results)
    
    for rec in recommendations:
        print(rec)
    
    # Detailed coordinate analysis
    print("\n🔬 DETAILED COORDINATE ANALYSIS:")
    print("-" * 40)
    
    # Show some key locations and their distances from center
    key_locations = ['Main Gate', 'University Library', 'Senate Building', 'Faculty of Science', 'Lagoon Front']
    for location in key_locations:
        if location in coordinates and location in coord_results['distance_analysis']:
            coord = coordinates[location]
            distances = coord_results['distance_analysis'][location]
            print(f"📍 {location}: {coord}")
            print(f"   Distance from campus center: {distances['UNILAG_CENTER']:.0f}m")
    
    print("\n✅ Verification complete!")

if __name__ == "__main__":
    main()
