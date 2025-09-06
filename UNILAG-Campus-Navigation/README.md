# UNILAG Campus Navigation System

## Project Overview

The **UNILAG Campus Navigation System** is a dynamic navigation tool for the University of Lagos campus. It models the campus as a graph, where buildings, gates, and intersections are nodes, and walkways or roads are edges with weights representing **distance or travel time**.  

The system uses **graph theory** and **Dijkstra's algorithm** to compute:
- The **shortest path** between any two campus locations.
- **Alternative paths** (3 different routes for each destination).
- **Dynamic path updates** (e.g., road closures or traffic changes).

The result is visualized interactively on a **Leaflet.js map** with **OpenStreetMap tiles**, making it relatable, practical, and dynamic.

---

## Tech Stack

| Component              | Technology / Library                          | Purpose                                                                 |
|------------------------|----------------------------------------------|-------------------------------------------------------------------------|
| Backend / Algorithm     | Python 3.x                                   | Implement graph theory and Dijkstra's algorithm to calculate paths      |
| Graph / Data Structure  | NetworkX (Python library)                     | Represent campus as a weighted, directed graph                          |
| Map Visualization       | Leaflet.js                                   | Display campus map and paths interactively (OpenStreetMap tiles)        |
| Frontend Interface      | HTML, CSS, JavaScript                        | Allow users to select source and destination, show results dynamically |
| Web Server              | Flask                                        | Serve Python backend results to frontend                                 |
| Map Data                | OpenStreetMap (OSM)                          | Free, open-source map tiles and path data                                |

---

## Project Structure

```
UNILAG-Campus-Navigation/
│
├── backend/
│   ├── graph.py                  # Graph creation and Dijkstra algorithm
│   ├── paths.py                  # Functions for multi-path and dynamic updates
│   └── data/
│       └── campus_nodes_edges.json  # Campus nodes and edges dataset
│
├── frontend/
│   ├── index.html                # Main HTML page with map
│   ├── style.css                 # Page styling
│   └── app.js                    # Leaflet.js map logic and API integration
│
├── app.py                        # Flask server to connect backend & frontend
├── README.md                     # Project documentation
└── requirements.txt              # Python dependencies (NetworkX, Flask, etc.)
```

---

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/UNILAG-Campus-Navigation
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://localhost:5001
   ```

---

## Features

### 🔍 Core Navigation Features
- **Shortest Path Finding**: Uses Dijkstra's algorithm to find optimal routes
- **Alternative Routes**: Provides up to 3 different path options
- **Interactive Map**: Click-to-select locations on campus map
- **Real-time Visualization**: See routes highlighted on the map

### 🚧 Dynamic Updates
- **Traffic Simulation**: Simulate heavy traffic conditions
- **Construction Zones**: Simulate road closures and construction
- **Real-time Recalculation**: Routes update automatically when conditions change

### 🚨 Emergency Features
- **Emergency Routes**: Quick access to Medical Center, Admin Building, Security
- **Fastest Emergency Path**: Prioritizes speed for emergency situations

### 📱 User Interface
- **Responsive Design**: Works on desktop and mobile
- **Interactive Map**: Leaflet.js with OpenStreetMap tiles
- **Modern UI**: Clean, intuitive interface with real-time feedback

---

## Campus Data

The system includes 15 key campus locations:

### 📍 Major Buildings
- Main Gate, Library, Senate Building
- Faculty of Science, Faculty of Arts, Faculty of Engineering
- Admin Building, Medical Center, Student Affairs

### 🚶 Points of Interest
- Sports Complex, Cafeteria, Bookshop
- Amphitheatre, Bus Stop, Parking Lot A

### 🗺️ Graph Structure
- **Nodes**: 15 campus locations with GPS coordinates
- **Edges**: 26 bidirectional paths with time-based weights
- **Weights**: Walking time in minutes between locations

---

## API Endpoints

### GET /api/nodes
Get all campus locations and coordinates

### GET /api/shortest-path
Find shortest path between two locations
- Parameters: `start`, `end`

### GET /api/multiple-paths
Find multiple alternative paths
- Parameters: `start`, `end`, `k` (number of paths)

### POST /api/traffic-update
Apply dynamic traffic/construction updates

### GET /api/emergency-routes
Find emergency routes from current location
- Parameters: `start`

### POST /api/reset-graph
Reset all dynamic conditions to normal

---

## Implementation Details

### Graph Algorithm
```python
# Dijkstra's algorithm implementation
def shortest_path(graph, start, end):
    path = nx.dijkstra_path(graph, source=start, target=end, weight='weight')
    distance = nx.dijkstra_path_length(graph, source=start, target=end, weight='weight')
    return path, distance
```

### Dynamic Updates
```python
# Simulate traffic conditions
traffic_updates = [
    {"from": "Library", "to": "Sports Complex", "condition": "heavy_traffic"},
    {"from": "Main Gate", "to": "Faculty of Science", "condition": "construction"}
]
```

### Frontend Mapping
```javascript
// Initialize Leaflet map
const map = L.map('map').setView([6.5244, 3.3792], 16);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
```

---

## Testing Cases

### 1. Standard Shortest Path
- **Test**: Find shortest path from Main Gate → Senate Building
- **Expected**: Optimal route with minimum travel time
- **Result**: Displays path on map with distance/time info

### 2. Multiple Alternative Paths
- **Test**: Find 3 alternative routes between any two locations
- **Expected**: Different paths ranked by distance/time
- **Result**: Color-coded routes on map with comparison data

### 3. Dynamic Updates
- **Test**: Simulate road closure (Faculty of Science ↔ Library)
- **Action**: Increase edge weight from 5 to 50 minutes
- **Expected**: Route recalculates to avoid blocked path
- **Result**: New optimal path displayed automatically

### 4. Emergency Routes
- **Test**: Find fastest routes to emergency locations
- **Expected**: Prioritized paths to Medical Center, Security, etc.
- **Result**: Multiple emergency routes with nearest location highlighted

---

## Development

### File Structure
- `backend/graph.py`: Core graph algorithms and data structures
- `backend/paths.py`: Advanced pathfinding and route optimization
- `app.py`: Flask API server
- `frontend/`: Web interface files
- `backend/data/`: Campus location and connection data

### Adding New Locations
1. Update `campus_nodes_edges.json` with new nodes and edges
2. Add GPS coordinates for map visualization
3. Restart server to load new data

### Customizing Routes
- Modify edge weights in JSON file
- Add new campus connections
- Update coordinate mappings for accurate map display

---

## Why This Implementation is Unique

- **Real Campus Model**: Uses actual UNILAG campus locations and layout
- **Multi-Algorithm Approach**: Combines shortest path with alternative route finding
- **Dynamic Adaptability**: Real-time updates for traffic and construction
- **Interactive Visualization**: Modern web interface with live map updates
- **Emergency Features**: Specialized routing for urgent situations
- **Open Source Stack**: Uses free, accessible technologies (OSM, Leaflet.js)
- **Educational Value**: Demonstrates practical application of graph theory

---

## Future Enhancements

- **GPS Integration**: Real-time location tracking
- **Accessibility Routes**: Wheelchair-friendly path options
- **Time-based Routing**: Different paths for different times of day
- **Crowd-sourced Updates**: User-reported conditions
- **Mobile App**: Native iOS/Android application
- **Indoor Navigation**: Building-level routing

---

## License

This project is created for educational purposes as part of a Final Year Project. Feel free to use and modify for academic purposes.

---

## Contributors

- **Final Year Student**: UNILAG Computer Science Department
- **Project**: Campus Navigation System using Graph Theory
- **Year**: 2025

---

## Contact

For questions or suggestions regarding this project, please contact through the university's academic channels.

---

*Built with ❤️ for the University of Lagos community*
