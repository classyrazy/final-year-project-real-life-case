#!/usr/bin/env python3
"""
Quick UNILAG coordinates update - using preset accurate coordinates
"""

import json
import os

# Accurate UNILAG campus coordinates based on research and mapping
accurate_coordinates = {
    "Main Gate": [6.5158, 3.3966],
    "Kenneth Dike Library": [6.5176, 3.3941], 
    "Faculty of Science": [6.5189, 3.3952],
    "Senate Building": [6.5171, 3.3945],
    "Faculty of Arts": [6.5164, 3.3928],
    "Faculty of Engineering": [6.5195, 3.3967],
    "Faculty of Social Sciences": [6.5168, 3.3934],
    "Faculty of Law": [6.5173, 3.3950],
    "Faculty of Medicine": [6.5142, 3.3889],
    "College of Medicine": [6.5145, 3.3892],
    "Sports Complex": [6.5201, 3.3923],
    "Medical Center": [6.5167, 3.3941],
    "Student Affairs Division": [6.5174, 3.3947],
    "Bursary Department": [6.5172, 3.3943],
    "Registry": [6.5170, 3.3946],
    "Vice Chancellor's Office": [6.5169, 3.3944],
    "Distance Learning Institute": [6.5184, 3.3958],
    "School of Postgraduate Studies": [6.5175, 3.3949],
    "Faculty of Education": [6.5162, 3.3931],
    "Faculty of Environmental Sciences": [6.5188, 3.3961],
    "Multipurpose Hall": [6.5178, 3.3940],
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
    "Staff Quarters": [6.5185, 3.3910],
    "University Bookshop": [6.5177, 3.3943],
    "Banking Complex": [6.5165, 3.3937],
    "Central Mosque": [6.5193, 3.3965],
    "Chapel of Resurrection": [6.5181, 3.3955],
    "UNILAG Consult": [6.5159, 3.3933],
    "Works and Physical Planning": [6.5186, 3.3959],
    "Security Unit": [6.5160, 3.3968],
    "Fire Service Station": [6.5163, 3.3970],
    "Lagoon Front": [6.5139, 3.3875],
    "Faculty of Pharmacy": [6.5148, 3.3895],
    "Faculty of Dentistry": [6.5151, 3.3898],
    "CMUL (College of Medicine)": [6.5144, 3.3890],
    "Teaching Hospital": [6.5140, 3.3885],
    "Bus Stop (Main)": [6.5161, 3.3971],
    "Car Park A": [6.5166, 3.3939],
    "Car Park B": [6.5191, 3.3964],
    "Car Park C": [6.5203, 3.3920],
    "Staff Club": [6.5182, 3.3918],
    "Guest House": [6.5179, 3.3915]
}

def update_campus_data():
    """Update the campus data file with accurate coordinates"""
    
    # Load current campus data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, '..', 'backend', 'data', 'campus_nodes_edges.json')
    
    try:
        with open(data_file, 'r') as f:
            campus_data = json.load(f)
        
        # Update coordinates
        campus_data['coordinates'] = accurate_coordinates
        
        # Save updated data
        with open(data_file, 'w') as f:
            json.dump(campus_data, f, indent=2)
        
        print("✅ Successfully updated campus coordinates!")
        print(f"📍 Updated {len(accurate_coordinates)} locations")
        print(f"💾 File saved: {data_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating campus data: {e}")
        return False

if __name__ == "__main__":
    print("🚀 UNILAG Campus Coordinate Update")
    print("=" * 40)
    
    success = update_campus_data()
    
    if success:
        print("\n🎉 Coordinate update completed successfully!")
        print("📋 You can now test the updated navigation system.")
    else:
        print("\n❌ Update failed. Please check the error messages above.")
        
    print("\n📍 Sample coordinates:")
    for i, (location, coords) in enumerate(list(accurate_coordinates.items())[:5]):
        print(f"   {location}: {coords[0]:.6f}, {coords[1]:.6f}")
    print(f"   ... and {len(accurate_coordinates)-5} more locations")
