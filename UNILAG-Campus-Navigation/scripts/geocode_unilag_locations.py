#!/usr/bin/env python3
"""
UNILAG Campus Geocoding Script
Fetches accurate coordinates for all campus locations using Nominatim API
"""

import requests
import json
import time
import sys
import os
from typing import Dict, List, Optional, Tuple

class UNILAGGeocoder:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {
            "User-Agent": "UNILAG-Navigation-App/1.0 (190806014@live.unilag.edu.ng)"
        }
        self.cache = {}
        
    def get_coordinates(self, place_name: str, retries: int = 3) -> Optional[Tuple[float, float]]:
        """
        Get coordinates for a place using Nominatim API
        
        Args:
            place_name: Name of the place to geocode
            retries: Number of retry attempts
            
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        # Check cache first
        if place_name in self.cache:
            return self.cache[place_name]
            
        for attempt in range(retries):
            try:
                params = {
                    "q": place_name,
                    "format": "json",
                    "limit": 3,  # Get multiple results for better selection
                    "addressdetails": 1,
                    "bounded": 1,
                    "viewbox": "3.35,6.50,3.45,6.55",  # UNILAG bounding box
                    "countrycodes": "ng"  # Nigeria only
                }
                
                print(f"🔍 Searching for: {place_name} (attempt {attempt + 1})")
                
                response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                results = response.json()
                
                if results:
                    # Filter results to prefer UNILAG-specific ones
                    best_result = self._select_best_result(results, place_name)
                    
                    if best_result:
                        lat = float(best_result["lat"])
                        lon = float(best_result["lon"])
                        coords = (lat, lon)
                        
                        # Cache the result
                        self.cache[place_name] = coords
                        
                        print(f"✅ Found: {lat:.6f}, {lon:.6f}")
                        print(f"   Display name: {best_result.get('display_name', 'N/A')}")
                        
                        # Respect Nominatim usage policy
                        time.sleep(1.2)
                        return coords
                    
                print(f"⚠️  No suitable result found for: {place_name}")
                time.sleep(2)  # Wait before retry
                
            except requests.RequestException as e:
                print(f"❌ Request error for {place_name}: {e}")
                time.sleep(3)
            except Exception as e:
                print(f"❌ Unexpected error for {place_name}: {e}")
                time.sleep(3)
        
        return None
    
    def _select_best_result(self, results: List[Dict], search_term: str) -> Optional[Dict]:
        """
        Select the best result from multiple geocoding results
        
        Args:
            results: List of geocoding results
            search_term: Original search term
            
        Returns:
            Best matching result or None
        """
        # Priority keywords for UNILAG campus
        unilag_keywords = [
            "university of lagos", "unilag", "lagos", "akoka",
            "yaba", "nigeria", "campus"
        ]
        
        scored_results = []
        
        for result in results:
            score = 0
            display_name = result.get("display_name", "").lower()
            
            # Score based on UNILAG-related keywords
            for keyword in unilag_keywords:
                if keyword in display_name:
                    score += 10
            
            # Prefer results with higher importance
            importance = float(result.get("importance", 0))
            score += importance * 5
            
            # Check if coordinates are within reasonable UNILAG bounds
            lat, lon = float(result["lat"]), float(result["lon"])
            if 6.50 <= lat <= 6.55 and 3.35 <= lon <= 3.45:
                score += 20  # High bonus for being in UNILAG area
            
            scored_results.append((score, result))
        
        # Sort by score (highest first)
        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        return scored_results[0][1] if scored_results else None

def main():
    """Main function to geocode all UNILAG locations"""
    
    # All UNILAG campus locations with various search variations
    unilag_locations = {
        "Main Gate": [
            "Main Gate, University of Lagos, Akoka, Lagos, Nigeria",
            "UNILAG Main Gate, Akoka, Lagos",
            "University of Lagos Main Entrance, Nigeria"
        ],
        "Kenneth Dike Library": [
            "Kenneth Dike Library, University of Lagos, Nigeria",
            "UNILAG Library, Akoka, Lagos",
            "University of Lagos Library, Nigeria"
        ],
        "Faculty of Science": [
            "Faculty of Science, University of Lagos, Nigeria",
            "Science Faculty, UNILAG, Akoka, Lagos",
            "University of Lagos Faculty of Science"
        ],
        "Senate Building": [
            "Senate Building, University of Lagos, Nigeria",
            "UNILAG Senate Building, Akoka, Lagos",
            "University of Lagos Senate House"
        ],
        "Faculty of Arts": [
            "Faculty of Arts, University of Lagos, Nigeria",
            "Arts Faculty, UNILAG, Akoka, Lagos"
        ],
        "Faculty of Engineering": [
            "Faculty of Engineering, University of Lagos, Nigeria",
            "Engineering Faculty, UNILAG, Akoka, Lagos"
        ],
        "Faculty of Social Sciences": [
            "Faculty of Social Sciences, University of Lagos, Nigeria",
            "Social Sciences Faculty, UNILAG, Akoka, Lagos"
        ],
        "Faculty of Law": [
            "Faculty of Law, University of Lagos, Nigeria",
            "Law Faculty, UNILAG, Akoka, Lagos"
        ],
        "Faculty of Medicine": [
            "Faculty of Medicine, University of Lagos, Nigeria",
            "Medical Faculty, UNILAG, Akoka, Lagos"
        ],
        "College of Medicine": [
            "College of Medicine, University of Lagos, Nigeria",
            "CMUL, University of Lagos, Lagos"
        ],
        "Sports Complex": [
            "Sports Complex, University of Lagos, Nigeria",
            "UNILAG Sports Center, Akoka, Lagos"
        ],
        "Medical Center": [
            "Medical Center, University of Lagos, Nigeria",
            "UNILAG Health Center, Akoka, Lagos"
        ],
        "Student Affairs Division": [
            "Student Affairs, University of Lagos, Nigeria",
            "UNILAG Student Affairs Division, Akoka"
        ],
        "Registry": [
            "Registry, University of Lagos, Nigeria",
            "UNILAG Registry, Akoka, Lagos"
        ],
        "Vice Chancellor's Office": [
            "Vice Chancellor Office, University of Lagos, Nigeria",
            "VC Office, UNILAG, Akoka, Lagos"
        ],
        "Distance Learning Institute": [
            "Distance Learning Institute, University of Lagos, Nigeria",
            "DLI, UNILAG, Akoka, Lagos"
        ],
        "Faculty of Education": [
            "Faculty of Education, University of Lagos, Nigeria",
            "Education Faculty, UNILAG, Akoka, Lagos"
        ],
        "Faculty of Environmental Sciences": [
            "Faculty of Environmental Sciences, University of Lagos, Nigeria",
            "Environmental Sciences Faculty, UNILAG"
        ],
        "Multipurpose Hall": [
            "Multipurpose Hall, University of Lagos, Nigeria",
            "UNILAG Multipurpose Hall, Akoka, Lagos"
        ],
        "New Hall (Female Hostel)": [
            "New Hall, University of Lagos, Nigeria",
            "New Hall Female Hostel, UNILAG"
        ],
        "Eni Njoku Hall (Male Hostel)": [
            "Eni Njoku Hall, University of Lagos, Nigeria",
            "Eni Njoku Hall, UNILAG"
        ],
        "Queen Amina Hall (Female Hostel)": [
            "Queen Amina Hall, University of Lagos, Nigeria",
            "Queen Amina Hall, UNILAG"
        ],
        "Biobaku Hall (Male Hostel)": [
            "Biobaku Hall, University of Lagos, Nigeria",
            "Biobaku Hall, UNILAG"
        ],
        "Makama Bida Hall (Female Hostel)": [
            "Makama Bida Hall, University of Lagos, Nigeria",
            "Makama Bida Hall, UNILAG"
        ],
        "Fagunwa Hall (Male Hostel)": [
            "Fagunwa Hall, University of Lagos, Nigeria",
            "Fagunwa Hall, UNILAG"
        ],
        "El-Kanemi Hall (Male Hostel)": [
            "El-Kanemi Hall, University of Lagos, Nigeria",
            "El-Kanemi Hall, UNILAG"
        ],
        "Moremi Hall (Female Hostel)": [
            "Moremi Hall, University of Lagos, Nigeria",
            "Moremi Hall, UNILAG"
        ],
        "Jaja Hall (Male Hostel)": [
            "Jaja Hall, University of Lagos, Nigeria",
            "Jaja Hall, UNILAG"
        ],
        "Kofo Ademola Hall (Female Hostel)": [
            "Kofo Ademola Hall, University of Lagos, Nigeria",
            "Kofo Ademola Hall, UNILAG"
        ],
        "University Bookshop": [
            "University Bookshop, University of Lagos, Nigeria",
            "UNILAG Bookshop, Akoka, Lagos"
        ],
        "Central Mosque": [
            "Central Mosque, University of Lagos, Nigeria",
            "UNILAG Mosque, Akoka, Lagos"
        ],
        "Chapel of Resurrection": [
            "Chapel of Resurrection, University of Lagos, Nigeria",
            "UNILAG Chapel, Akoka, Lagos"
        ],
        "Teaching Hospital": [
            "Lagos University Teaching Hospital, Nigeria",
            "LUTH, Lagos, Nigeria"
        ],
        "Lagoon Front": [
            "Lagos Lagoon, University of Lagos, Nigeria",
            "UNILAG Lagoon Front, Akoka"
        ]
    }
    
    # Create geocoder instance
    geocoder = UNILAGGeocoder()
    
    # Store results
    coordinates = {}
    failed_locations = []
    
    print("🚀 Starting UNILAG Campus Geocoding Process")
    print("=" * 50)
    
    for location, search_terms in unilag_locations.items():
        print(f"\n📍 Processing: {location}")
        
        coords = None
        
        # Try each search variation
        for search_term in search_terms:
            coords = geocoder.get_coordinates(search_term)
            if coords:
                break
        
        if coords:
            coordinates[location] = [coords[0], coords[1]]  # [lat, lon] format
            print(f"✅ SUCCESS: {location} -> {coords[0]:.6f}, {coords[1]:.6f}")
        else:
            failed_locations.append(location)
            print(f"❌ FAILED: {location}")
            # Use approximate coordinates based on UNILAG campus center
            coordinates[location] = [6.5244, 3.3792]  # Default UNILAG center
    
    # Generate output
    print("\n" + "=" * 50)
    print("📊 GEOCODING RESULTS")
    print("=" * 50)
    print(f"✅ Successfully geocoded: {len(coordinates) - len(failed_locations)} locations")
    print(f"❌ Failed geocoding: {len(failed_locations)} locations")
    
    if failed_locations:
        print(f"\n⚠️  Failed locations (using default coordinates):")
        for location in failed_locations:
            print(f"   - {location}")
    
    # Save results to file
    output_file = os.path.join(os.path.dirname(__file__), '..', 'backend', 'data', 'geocoded_coordinates.json')
    
    output_data = {
        "coordinates": coordinates,
        "metadata": {
            "total_locations": len(coordinates),
            "successfully_geocoded": len(coordinates) - len(failed_locations),
            "failed_locations": failed_locations,
            "geocoding_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": "OpenStreetMap Nominatim API"
        }
    }
    
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        # Also print JSON for manual copy-paste
        print(f"\n📋 Coordinates JSON (for manual update):")
        print("-" * 50)
        print(json.dumps({"coordinates": coordinates}, indent=2))
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        print(f"\n📋 Raw coordinates output:")
        print(json.dumps(coordinates, indent=2))

if __name__ == "__main__":
    main()
