#!/usr/bin/env python3
"""
Simple UNILAG Campus Coordinate Updater
Uses urllib (built-in) to fetch coordinates and updates the campus data file
"""

import urllib.request
import urllib.parse
import json
import time
import os

def get_coordinates(place_name):
    """Get coordinates using Nominatim API with urllib"""
    base_url = "https://nominatim.openstreetmap.org/search"
    
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1,
        "addressdetails": "1",
        "bounded": "1",
        "viewbox": "3.35,6.50,3.45,6.55",  # UNILAG area
        "countrycodes": "ng"
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'UNILAG-Navigation-App/1.0')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
        if data:
            return [float(data[0]["lat"]), float(data[0]["lon"])]
        return None
        
    except Exception as e:
        print(f"Error geocoding {place_name}: {e}")
        return None

# UNILAG locations with search terms
locations = {
    "Main Gate": "Main Gate, University of Lagos, Akoka, Lagos, Nigeria",
    "Kenneth Dike Library": "Kenneth Dike Library, University of Lagos, Nigeria",
    "Faculty of Science": "Faculty of Science, University of Lagos, Nigeria", 
    "Senate Building": "Senate Building, University of Lagos, Nigeria",
    "Faculty of Arts": "Faculty of Arts, University of Lagos, Nigeria",
    "Faculty of Engineering": "Faculty of Engineering, University of Lagos, Nigeria",
    "Faculty of Social Sciences": "Faculty of Social Sciences, University of Lagos, Nigeria",
    "Faculty of Law": "Faculty of Law, University of Lagos, Nigeria",
    "Faculty of Medicine": "Faculty of Medicine, University of Lagos, Nigeria",
    "College of Medicine": "College of Medicine, University of Lagos, Nigeria",
    "Sports Complex": "Sports Complex, University of Lagos, Nigeria",
    "Medical Center": "Medical Center, University of Lagos, Nigeria",
    "Student Affairs Division": "Student Affairs Division, University of Lagos, Nigeria",
    "Bursary Department": "Bursary Department, University of Lagos, Nigeria",
    "Registry": "Registry, University of Lagos, Nigeria",
    "Vice Chancellor's Office": "Vice Chancellor Office, University of Lagos, Nigeria",
    "Distance Learning Institute": "Distance Learning Institute, University of Lagos, Nigeria",
    "School of Postgraduate Studies": "School of Postgraduate Studies, University of Lagos, Nigeria",
    "Faculty of Education": "Faculty of Education, University of Lagos, Nigeria",
    "Faculty of Environmental Sciences": "Faculty of Environmental Sciences, University of Lagos, Nigeria",
    "Multipurpose Hall": "Multipurpose Hall, University of Lagos, Nigeria",
    "New Hall (Female Hostel)": "New Hall, University of Lagos, Nigeria",
    "Eni Njoku Hall (Male Hostel)": "Eni Njoku Hall, University of Lagos, Nigeria",
    "Queen Amina Hall (Female Hostel)": "Queen Amina Hall, University of Lagos, Nigeria",
    "Biobaku Hall (Male Hostel)": "Biobaku Hall, University of Lagos, Nigeria",
    "Makama Bida Hall (Female Hostel)": "Makama Bida Hall, University of Lagos, Nigeria",
    "Fagunwa Hall (Male Hostel)": "Fagunwa Hall, University of Lagos, Nigeria",
    "El-Kanemi Hall (Male Hostel)": "El-Kanemi Hall, University of Lagos, Nigeria",
    "Moremi Hall (Female Hostel)": "Moremi Hall, University of Lagos, Nigeria",
    "Jaja Hall (Male Hostel)": "Jaja Hall, University of Lagos, Nigeria",
    "Kofo Ademola Hall (Female Hostel)": "Kofo Ademola Hall, University of Lagos, Nigeria",
    "Staff Quarters": "Staff Quarters, University of Lagos, Nigeria",
    "University Bookshop": "University Bookshop, University of Lagos, Nigeria",
    "Banking Complex": "Banking Complex, University of Lagos, Nigeria",
    "Central Mosque": "Central Mosque, University of Lagos, Nigeria",
    "Chapel of Resurrection": "Chapel of Resurrection, University of Lagos, Nigeria",
    "UNILAG Consult": "UNILAG Consult, University of Lagos, Nigeria",
    "Works and Physical Planning": "Works and Physical Planning, University of Lagos, Nigeria",
    "Security Unit": "Security Unit, University of Lagos, Nigeria",
    "Fire Service Station": "Fire Service Station, University of Lagos, Nigeria",
    "Lagoon Front": "Lagos Lagoon, University of Lagos, Nigeria",
    "Faculty of Pharmacy": "Faculty of Pharmacy, University of Lagos, Nigeria",
    "Faculty of Dentistry": "Faculty of Dentistry, University of Lagos, Nigeria",
    "CMUL (College of Medicine)": "College of Medicine, University of Lagos, Nigeria",
    "Teaching Hospital": "Lagos University Teaching Hospital, Nigeria",
    "Bus Stop (Main)": "Main Bus Stop, University of Lagos, Nigeria",
    "Car Park A": "Car Park A, University of Lagos, Nigeria",
    "Car Park B": "Car Park B, University of Lagos, Nigeria", 
    "Car Park C": "Car Park C, University of Lagos, Nigeria",
    "Staff Club": "Staff Club, University of Lagos, Nigeria",
    "Guest House": "Guest House, University of Lagos, Nigeria"
}

def main():
    print("🚀 Fetching accurate coordinates for UNILAG campus locations...")
    print("=" * 60)
    
    coordinates = {}
    failed = []
    
    for location, search_term in locations.items():
        print(f"📍 Geocoding: {location}")
        coords = get_coordinates(search_term)
        
        if coords:
            coordinates[location] = coords
            print(f"   ✅ Found: {coords[0]:.6f}, {coords[1]:.6f}")
        else:
            failed.append(location)
            # Use reasonable default coordinates within UNILAG campus
            coordinates[location] = [6.5244, 3.3792]
            print(f"   ❌ Failed, using default coordinates")
        
        # Respect rate limits
        time.sleep(1.2)
    
    print(f"\n📊 Results: {len(coordinates) - len(failed)} successful, {len(failed)} failed")
    
    if failed:
        print(f"⚠️  Failed locations: {', '.join(failed)}")
    
    # Output the coordinates JSON
    print(f"\n📋 Updated coordinates JSON:")
    print("=" * 60)
    print(json.dumps({"coordinates": coordinates}, indent=2))
    
    # Save to file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, '..', 'backend', 'data', 'updated_coordinates.json')
    
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump({"coordinates": coordinates}, f, indent=2)
        print(f"\n💾 Saved coordinates to: {output_file}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

if __name__ == "__main__":
    main()
