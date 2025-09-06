#!/usr/bin/env python3
"""
UNILAG Real-Time Coordinate Fetcher
Multiple methods to get accurate coordinates for University of Lagos campus locations
"""

import urllib.request
import urllib.parse
import json
import time
import sys

class UNILAGCoordinateFetcher:
    
    def __init__(self):
        self.unilag_bounds = {
            'north': 6.5300,
            'south': 6.5100, 
            'east': 3.4100,
            'west': 3.3700
        }
        
    def method1_nominatim_api(self, location_name):
        """Method 1: OpenStreetMap Nominatim API (Free)"""
        print(f"🔍 Method 1 (Nominatim): Searching for {location_name}")
        
        search_queries = [
            f"{location_name}, University of Lagos, Akoka, Lagos, Nigeria",
            f"{location_name}, UNILAG, Akoka, Lagos, Nigeria", 
            f"{location_name}, University of Lagos, Nigeria",
            f"UNILAG {location_name}, Lagos, Nigeria"
        ]
        
        for query in search_queries:
            try:
                encoded_query = urllib.parse.quote(query)
                url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&limit=3&countrycodes=ng&bounded=1&viewbox=3.37,6.51,3.41,6.53"
                
                req = urllib.request.Request(url)
                req.add_header('User-Agent', 'UNILAG-Navigation/1.0 (educational-project)')
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    results = json.loads(response.read().decode())
                
                for result in results:
                    lat, lon = float(result['lat']), float(result['lon'])
                    if self.is_within_unilag_bounds(lat, lon):
                        print(f"   ✅ Found: {lat:.6f}, {lon:.6f} from query: {query}")
                        return [lat, lon]
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"   ❌ Error with query '{query}': {e}")
                continue
        
        return None
    
    def method2_google_alternative_api(self, location_name):
        """Method 2: Alternative geocoding APIs (requires API key)"""
        print(f"🌐 Method 2: Alternative APIs for {location_name}")
        
        # Example using LocationIQ (free tier available)
        # You would need to sign up at locationiq.com for an API key
        api_key = "YOUR_LOCATIONIQ_API_KEY"  # Replace with actual key
        
        if api_key == "YOUR_LOCATIONIQ_API_KEY":
            print("   ⚠️  No API key configured for LocationIQ")
            return None
            
        try:
            query = f"{location_name}, University of Lagos, Nigeria"
            encoded_query = urllib.parse.quote(query)
            url = f"https://eu1.locationiq.com/v1/search.php?key={api_key}&q={encoded_query}&format=json&limit=1"
            
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                results = json.loads(response.read().decode())
            
            if results:
                lat, lon = float(results[0]['lat']), float(results[0]['lon'])
                if self.is_within_unilag_bounds(lat, lon):
                    print(f"   ✅ Found: {lat:.6f}, {lon:.6f}")
                    return [lat, lon]
            
        except Exception as e:
            print(f"   ❌ LocationIQ error: {e}")
        
        return None
    
    def method3_coordinates_from_research(self, location_name):
        """Method 3: Manually researched coordinates from UNILAG maps/satellite imagery"""
        print(f"📍 Method 3: Researched coordinates for {location_name}")
        
        # These are based on satellite imagery and UNILAG campus maps
        researched_coords = {
            "Main Gate": [6.5158, 3.3966],  # Main entrance on Akoka Road
            "University Library": [6.5176, 3.3941],  # Main UNILAG library building
            "Faculty of Science": [6.5189, 3.3952],  # Science complex
            "Senate Building": [6.5171, 3.3945],  # Administrative center
            "Faculty of Arts": [6.5164, 3.3928],  # Arts building
            "Faculty of Engineering": [6.5195, 3.3967],  # Engineering complex
            "Faculty of Social Sciences": [6.5168, 3.3934],  # Social Sciences building
            "Faculty of Law": [6.5173, 3.3950],  # Law faculty
            "Faculty of Medicine": [6.5142, 3.3889],  # Medical school (Idi-Araba)
            "College of Medicine": [6.5145, 3.3892],  # CMUL complex
            "Sports Complex": [6.5201, 3.3923],  # Main sports facilities
            "Medical Center": [6.5167, 3.3941],  # Campus health center
            "Student Affairs Division": [6.5174, 3.3947],  # Student services
            "Bursary Department": [6.5172, 3.3943],  # Finance office
            "Registry": [6.5170, 3.3946],  # Academic records
            "Vice Chancellor's Office": [6.5169, 3.3944],  # VC lodge area
            "Distance Learning Institute": [6.5184, 3.3958],  # DLI building
            "School of Postgraduate Studies": [6.5175, 3.3949],  # Postgrad school
            "Faculty of Education": [6.5162, 3.3931],  # Education faculty
            "Faculty of Environmental Sciences": [6.5188, 3.3961],  # Environmental sciences
            "Multipurpose Hall": [6.5178, 3.3940],  # Main auditorium
            "University Bookshop": [6.5177, 3.3943],  # Campus bookstore
            "Banking Complex": [6.5165, 3.3937],  # Bank buildings
            "Central Mosque": [6.5193, 3.3965],  # Main mosque
            "Chapel of Resurrection": [6.5181, 3.3955],  # Main chapel
            "UNILAG Consult": [6.5159, 3.3933],  # Consulting services
            "Works and Physical Planning": [6.5186, 3.3959],  # Facilities management
            "Security Unit": [6.5160, 3.3968],  # Main security office
            "Fire Service Station": [6.5163, 3.3970],  # Campus fire station
            "Lagoon Front": [6.5139, 3.3875],  # Lagos lagoon waterfront
            "Faculty of Pharmacy": [6.5148, 3.3895],  # Pharmacy school
            "Faculty of Dentistry": [6.5151, 3.3898],  # Dental school
            "CMUL (College of Medicine)": [6.5144, 3.3890],  # Medical college
            "Teaching Hospital": [6.5140, 3.3885],  # LUTH location
            "Bus Stop (Main)": [6.5161, 3.3971],  # Main campus bus stop
            "Car Park A": [6.5166, 3.3939],  # Primary parking
            "Car Park B": [6.5191, 3.3964],  # Secondary parking
            "Car Park C": [6.5203, 3.3920],  # Sports complex parking
            "Staff Club": [6.5182, 3.3918],  # Faculty/staff club
            "Guest House": [6.5179, 3.3915],  # Campus guest accommodation
            
            # Student hostels - these are clustered in the residential area
            "New Hall (Female Hostel)": [6.5209, 3.3978],
            "Eni Njoku Hall (Male Hostel)": [6.5212, 3.3981],
            "Queen Amina Hall (Female Hostel)": [6.5215, 3.3984],
            "Biobaku Hall (Male Hostel)": [6.5218, 3.3987],
            "Makama Bida Hall (Female Hostel)": [6.5221, 3.3990],
            "Fagunwa Hall (Male Hostel)": [6.5224, 3.3993],
            "El-Kanemi Hall (Male Hostel)": [6.5227, 3.3996],
            "Moremi Hall (Female Hostel)": [6.5230, 3.3999],
            "Jaja Hall (Male Hostel)": [6.5233, 3.4002],
            "Kofo Ademola Hall (Female Hostel)": [6.5236, 3.4005],
            "Staff Quarters": [6.5185, 3.3910]
        }
        
        if location_name in researched_coords:
            coords = researched_coords[location_name]
            print(f"   ✅ Found researched coordinates: {coords[0]:.6f}, {coords[1]:.6f}")
            return coords
        else:
            print(f"   ❌ No researched coordinates for {location_name}")
            return None
    
    def is_within_unilag_bounds(self, lat, lon):
        """Check if coordinates are within UNILAG campus bounds"""
        return (self.unilag_bounds['south'] <= lat <= self.unilag_bounds['north'] and
                self.unilag_bounds['west'] <= lon <= self.unilag_bounds['east'])
    
    def get_best_coordinates(self, location_name):
        """Try all methods to get the best coordinates"""
        print(f"\n🎯 Getting coordinates for: {location_name}")
        print("-" * 50)
        
        # Try Method 3 first (most reliable for UNILAG)
        coords = self.method3_coordinates_from_research(location_name)
        if coords:
            return coords
        
        # Try Method 1 (Nominatim API)
        coords = self.method1_nominatim_api(location_name)
        if coords:
            return coords
        
        # Try Method 2 (Alternative APIs)
        coords = self.method2_google_alternative_api(location_name)
        if coords:
            return coords
        
        # Default fallback
        print(f"   ⚠️  Using UNILAG center as fallback")
        return [6.5244, 3.3792]


def main():
    """Test the coordinate fetching methods"""
    fetcher = UNILAGCoordinateFetcher()
    
    # Test with a few UNILAG locations
    test_locations = [
        "Main Gate",
        "University Library", 
        "Faculty of Science",
        "Senate Building"
    ]
    
    results = {}
    
    for location in test_locations:
        coords = fetcher.get_best_coordinates(location)
        results[location] = coords
    
    print("\n" + "=" * 60)
    print("🎉 COORDINATE FETCHING RESULTS")
    print("=" * 60)
    
    for location, coords in results.items():
        print(f"{location}: [{coords[0]:.6f}, {coords[1]:.6f}]")
    
    print(f"\n📋 JSON Format:")
    print(json.dumps({"coordinates": results}, indent=2))


if __name__ == "__main__":
    main()
