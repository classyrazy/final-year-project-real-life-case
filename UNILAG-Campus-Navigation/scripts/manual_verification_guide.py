#!/usr/bin/env python3
"""
Manual Coordinate Verification Guide for UNILAG
This script provides you with exact search terms to manually verify coordinates
"""

def generate_verification_guide():
    """Generate a guide for manually verifying UNILAG coordinates"""
    
    unilag_locations = [
        "Main Gate", "University Library", "Faculty of Science", "Senate Building", 
        "Faculty of Arts", "Faculty of Engineering", "Faculty of Social Sciences", 
        "Faculty of Law", "Faculty of Medicine", "College of Medicine", "Sports Complex",
        "Medical Center", "Student Affairs Division", "Bursary Department", "Registry",
        "Vice Chancellor's Office", "Distance Learning Institute", "School of Postgraduate Studies",
        "Faculty of Education", "Faculty of Environmental Sciences", "Multipurpose Hall",
        "New Hall (Female Hostel)", "Eni Njoku Hall (Male Hostel)", "Queen Amina Hall (Female Hostel)", 
        "Biobaku Hall (Male Hostel)", "Makama Bida Hall (Female Hostel)", "Fagunwa Hall (Male Hostel)",
        "El-Kanemi Hall (Male Hostel)", "Moremi Hall (Female Hostel)", "Jaja Hall (Male Hostel)",
        "Kofo Ademola Hall (Female Hostel)", "Staff Quarters", "University Bookshop",
        "Banking Complex", "Central Mosque", "Chapel of Resurrection", "UNILAG Consult",
        "Works and Physical Planning", "Security Unit", "Fire Service Station", "Lagoon Front",
        "Faculty of Pharmacy", "Faculty of Dentistry", "CMUL (College of Medicine)",
        "Teaching Hospital", "Bus Stop (Main)", "Car Park A", "Car Park B", "Car Park C",
        "Staff Club", "Guest House"
    ]
    
    print("📍 UNILAG COORDINATE VERIFICATION GUIDE")
    print("=" * 60)
    print("Use these search terms in Google Maps, OpenStreetMap, or GPS tools:\n")
    
    for i, location in enumerate(unilag_locations, 1):
        print(f"{i:2d}. {location}")
        
        # Generate specific search terms for each location
        search_terms = []
        
        if "Hall" in location:
            # Student hostels
            hall_name = location.split(" (")[0]
            search_terms = [
                f"{hall_name}, University of Lagos",
                f"{hall_name} Hall, UNILAG, Akoka",
                f"UNILAG {hall_name}, Lagos"
            ]
        elif "Faculty" in location:
            # Academic faculties
            faculty = location.replace("Faculty of ", "")
            search_terms = [
                f"Faculty of {faculty}, University of Lagos",
                f"{faculty} Faculty, UNILAG, Akoka",
                f"University of Lagos {faculty} Department"
            ]
        else:
            # Other buildings
            search_terms = [
                f"{location}, University of Lagos, Akoka",
                f"UNILAG {location}, Lagos",
                f"{location}, University of Lagos, Nigeria"
            ]
        
        for term in search_terms:
            print(f"     🔍 {term}")
        print()
    
    print("\n" + "=" * 60)
    print("📋 VERIFICATION CHECKLIST:")
    print("=" * 60)
    print("✅ Ensure coordinates are within UNILAG bounds:")
    print("   • Latitude: 6.5100 to 6.5300")
    print("   • Longitude: 3.3700 to 3.4100")
    print("\n✅ Cross-reference with multiple sources:")
    print("   • Google Maps")
    print("   • OpenStreetMap")
    print("   • Bing Maps")
    print("   • UNILAG official campus map")
    print("\n✅ Verify location makes sense relative to campus layout")
    print("\n🌐 ONLINE COORDINATE TOOLS:")
    print("   • https://nominatim.openstreetmap.org")
    print("   • https://maps.google.com (right-click for coordinates)")
    print("   • https://www.latlong.net")
    print("   • https://gps-coordinates.org")

if __name__ == "__main__":
    generate_verification_guide()
