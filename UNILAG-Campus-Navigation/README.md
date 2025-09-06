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

## 🚀 Step-by-Step Setup Guide for Colleagues

### Prerequisites Check

Before starting, ensure you have the following installed on your laptop:

| Requirement | Minimum Version | Check Command |
|------------|----------------|---------------|
| **Python** | 3.8+ | `python --version` or `python3 --version` |
| **pip** | Latest | `pip --version` or `pip3 --version` |
| **Git** | Any recent version | `git --version` |
| **Web Browser** | Chrome, Firefox, Safari, Edge | Any modern browser |

> **Note**: If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/)

---

### Step 1: Clone the Project

Open your terminal/command prompt and run:

```bash
# Option 1: Clone from GitHub (if available)
git clone https://github.com/your-username/UNILAG-Campus-Navigation.git
cd UNILAG-Campus-Navigation

# Option 2: If you received the project folder, navigate to it
cd path/to/UNILAG-Campus-Navigation
```

**Verify you're in the right directory:**
```bash
ls -la
# You should see: app.py, frontend/, backend/, requirements.txt, etc.
```

---

### Step 2: Set Up Python Environment (Recommended)

Create a virtual environment to avoid conflicts with other Python projects:

```bash
# Create virtual environment
python -m venv campus_nav_env

# Activate virtual environment
# On Windows:
campus_nav_env\Scripts\activate

# On macOS/Linux:
source campus_nav_env/bin/activate

# You should see (campus_nav_env) at the beginning of your terminal prompt
```

---

### Step 3: Install Dependencies

Install all required Python packages:

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
# You should see: Flask, networkx, flask-cors, and other packages
```

**If you encounter any errors**, try:
```bash
# Alternative installation methods
pip3 install -r requirements.txt
# OR
python -m pip install -r requirements.txt
```

---

### Step 4: Start the Application

You have two options to run the application:

#### Option A: Using the Start Script (Recommended)
```bash
# Make the script executable (macOS/Linux)
chmod +x start.sh

# Run the start script
./start.sh

# Follow the prompts - select 'n' when asked about tests
```

#### Option B: Manual Startup
Open **two separate terminal windows**:

**Terminal 1 - Backend Server:**
```bash
cd UNILAG-Campus-Navigation
python app.py
# You should see: "Server starting on http://localhost:5001"
```

**Terminal 2 - Frontend Server:**
```bash
cd UNILAG-Campus-Navigation
python frontend_server.py
# You should see: "Serving at port 8080"
```

---

### Step 5: Open the Application

1. **Open your web browser**
2. **Navigate to**: `http://localhost:8080`
3. **You should see**: The UNILAG Campus Navigation interface with a map

---

### Step 6: Test the Application

Follow these steps to verify everything is working:

#### Test 1: Basic Navigation
1. **Select Start Location**: Choose "Main Gate" from the dropdown
2. **Select Destination**: Choose "Senate Building" from the dropdown
3. **Click "Find Route"**
4. **Expected Result**: You should see:
   - A blue route line on the map
   - Route information panel showing distance and time
   - Step-by-step algorithm visualization

#### Test 2: Alternative Routes
1. **Keep the same start/end locations**
2. **Click "Alternative Routes"**
3. **Expected Result**: Multiple colored route lines showing different paths

#### Test 3: Algorithm Visualization
1. **After finding a route**, look for the "Algorithm Visualization" panel
2. **Click the step navigation buttons** (Previous/Next)
3. **Expected Result**: See how Dijkstra's algorithm works step-by-step

---

### 🛠️ Troubleshooting Common Issues

#### Issue 1: "Port already in use"
```bash
# Kill processes using the ports
# On macOS/Linux:
lsof -ti:5001 | xargs kill -9
lsof -ti:8080 | xargs kill -9

# On Windows:
netstat -ano | findstr :5001
taskkill /PID <PID_NUMBER> /F
```

#### Issue 2: "Module not found" errors
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

#### Issue 3: Python version conflicts
```bash
# Use specific Python version
python3 app.py
python3 frontend_server.py
```

#### Issue 4: Virtual environment issues
```bash
# Deactivate and recreate
deactivate
rm -rf campus_nav_env
python -m venv campus_nav_env
source campus_nav_env/bin/activate  # macOS/Linux
# OR
campus_nav_env\Scripts\activate     # Windows
pip install -r requirements.txt
```

#### Issue 5: Browser doesn't show the map
1. **Check console for errors** (F12 → Console tab)
2. **Verify both servers are running**:
   - Backend: `http://localhost:5001/api/nodes` should return JSON data
   - Frontend: `http://localhost:8080` should show the interface
3. **Try a different browser**

---

### 📱 Testing on Different Devices

#### Desktop Testing
- **Recommended browsers**: Chrome, Firefox, Safari, Edge
- **Screen resolution**: Works best on screens 1024px+ wide

#### Mobile Testing
- **Open**: `http://YOUR_IP_ADDRESS:8080` on mobile browser
- **Find your IP**: 
  ```bash
  # macOS/Linux:
  ifconfig | grep inet
  # Windows:
  ipconfig
  ```

---

### 🔧 Development Mode

If you want to modify the code and see changes instantly:

#### Backend Development
```bash
# Run with auto-reload
export FLASK_DEBUG=1  # macOS/Linux
set FLASK_DEBUG=1     # Windows
python app.py
```

#### Frontend Development
- Edit files in the `frontend/` directory
- Refresh browser to see changes
- No restart needed for HTML/CSS/JS changes

---

### 📊 Project Structure Overview

```
UNILAG-Campus-Navigation/
├── 🐍 app.py                     # Main Flask server (Backend)
├── 🌐 frontend_server.py         # Static file server (Frontend)
├── 🚀 start.sh                   # Convenient startup script
├── 📋 requirements.txt           # Python dependencies
├── 📁 frontend/
│   ├── 🗺️ index.html            # Main interface
│   ├── 🎨 style.css             # Styling
│   └── ⚡ app.js                # Map logic & API calls
├── 📁 backend/
│   ├── 📊 graph.py               # Graph algorithms
│   ├── 🛣️ paths.py              # Pathfinding logic
│   └── 📁 data/
│       └── 🗃️ campus_nodes_edges.json  # Campus data
└── 📁 scripts/                   # Additional utilities
```

---

### ✅ Success Checklist

Before considering the setup complete, verify:

- [ ] **Backend server** is running on port 5001
- [ ] **Frontend server** is running on port 8080
- [ ] **Web interface** loads at `http://localhost:8080`
- [ ] **Location dropdowns** are populated with campus locations
- [ ] **"Find Route" button** generates a path on the map
- [ ] **Route information panel** shows distance and time
- [ ] **Alternative Routes** displays multiple path options
- [ ] **Algorithm visualization** shows step-by-step execution
- [ ] **No error messages** in browser console (F12)

---

### 🆘 Need Help?

If you encounter any issues:

1. **Check the terminal output** for error messages
2. **Open browser developer tools** (F12) and check the Console tab
3. **Verify all prerequisites** are installed correctly
4. **Try the troubleshooting steps** above
5. **Contact the project maintainer** with:
   - Your operating system (Windows/macOS/Linux)
   - Python version (`python --version`)
   - Error messages (copy exact text)
   - Steps you followed before the error occurred

---

### 💡 Quick Tips for Colleagues

- **Always activate the virtual environment** before working on the project
- **Keep both terminal windows open** while using the application
- **Use Ctrl+C** to stop the servers when done
- **The application works best with a stable internet connection** (for map tiles)
- **If something breaks, try restarting both servers**

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
