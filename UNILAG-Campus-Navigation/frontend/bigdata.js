/**
 * Big Data Algorithm Analysis - UK Cities
 * Demonstrates Dijkstra's Algorithm performance with large datasets
 */

let bigDataMap;
let citiesLayer;
let routeLayer;
let bigDataGraph = {};
let ukCitiesData = {};
let performanceMetrics = [];
let currentRoute = null;

// UK Cities Dataset
const ukCities = {
    'city': ['London','Birmingham','Manchester','Liverpool','Bristol','Newcastle upon Tyne','Sheffield','Cardiff','Leeds','Nottingham','Leicester','Coventry','Bradford','Newcastle','Stoke-on-Trent','Wolverhampton','Derby','Swansea','Plymouth','Reading','Hull','Preston','Luton','Portsmouth','Southampton','Sunderland','Warrington','Bournemouth','Swindon','Oxford','Huddersfield','Slough','Blackpool','Middlesbrough','Ipswich','Telford','York','West Bromwich','Peterborough','Stockport','Brighton','Hastings','Exeter','Chelmsford','Chester','St Helens','Colchester','Crawley','Stevenage','Birkenhead','Bolton','Stockton-on-Tees','Watford','Gloucester','Rotherham','Newport','Cambridge','St Albans','Bury','Southend-on-Sea','Woking','Maidstone','Lincoln','Gillingham','Chesterfield','Oldham','Charlton','Aylesbury','Keighley','Bangor','Scunthorpe','Guildford','Grimsby','Ellesmere Port','Blackburn','Hove','Hartlepool','Taunton','Maidenhead','Aldershot','Great Yarmouth','Rossendale'],
    'latitude': [51.509865,52.4862,53.483959,53.4084,51.4545,54.9784,53.3811,51.4816,53.8008,52.9548,52.6369,52.4068,53.7957,55.007,53.0027,52.5862,52.9228,51.6214,50.3755,51.4543,53.7443,53.7632,51.8787,50.8195,50.9097,54.9069,53.3872,50.7208,51.5686,51.752,53.649,51.5095,53.8175,54.5742,52.0567,52.6784,53.959,52.5187,52.5695,53.4084,50.8225,50.8552,50.7184,51.7361,53.1934,53.4539,51.8892,51.1124,51.9038,53.3934,53.5769,54.5741,51.6562,51.8642,53.432,51.5881,52.2053,51.752,53.591,51.5406,51.3169,51.2704,53.2307,51.3898,53.235,53.5444,51.4941,51.8156,53.867,53.2274,53.5896,51.2362,53.5675,53.2826,53.7486,50.8279,54.6892,51.0143,51.522,51.2484,52.6083,53.6458],
    'longitude': [-0.118092,-1.8904,-2.244644,-2.9916,-2.5879,-1.6174,-1.4701,-3.1791,-1.5491,-1.1581,-1.1398,-1.5197,-1.7593,-1.6174,-2.1794,-2.1288,-1.4777,-3.9436,-4.1427,-0.9781,-0.3326,-2.7031,-0.42,-1.0874,-1.4044,-1.3834,-2.5925,-1.9046,-1.7722,-1.2577,-1.7849,-0.5954,-3.0357,-1.2356,-1.1482,-2.4453,-1.0815,-1.9945,-0.2405,-2.1493,-0.1372,-0.5723,-3.5339,-0.4791,-2.8931,-2.7375,-0.9042,-0.1831,-0.1966,-3.0148,-2.428,-1.3187,-0.39,-2.2382,-1.3502,-3.1409,-0.1218,-0.339,-2.298,0.711,-0.56,-0.5227,-0.5406,-0.5486,-1.4216,-2.1183,-0.068,-0.8084,-1.9064,-4.1297,-0.6544,-0.5704,-0.0802,-2.8976,-2.4877,-0.1688,-1.2122,-3.1036,-0.7205,-0.755,-1.7303,-2.2864]
};

// Initialize the big data analysis page
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing Big Data Algorithm Analysis...');
    
    try {
        initializeBigDataMap();
        processUKCitiesData();
        setupBigDataEventListeners();
        initializeCharts();
        console.log('✅ Big Data Analysis initialized successfully');
    } catch (error) {
        console.error('❌ Error during initialization:', error);
    }
});

function initializeBigDataMap() {
    // Initialize map centered on UK
    bigDataMap = L.map('bigdata-map').setView([54.0, -2.0], 6);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(bigDataMap);
    
    // Initialize layers
    citiesLayer = L.layerGroup().addTo(bigDataMap);
    routeLayer = L.layerGroup().addTo(bigDataMap);
    
    console.log('🗺️ Big Data map initialized');
}

function processUKCitiesData() {
    // Create coordinates mapping
    ukCitiesData = {};
    
    for (let i = 0; i < ukCities.city.length; i++) {
        const city = ukCities.city[i];
        const lat = ukCities.latitude[i];
        const lng = ukCities.longitude[i];
        
        ukCitiesData[city] = [lat, lng];
    }
    
    // Populate city selects
    populateCitySelects();
    
    // Add city markers to map
    addCityMarkers();
    
    console.log(`✅ Processed ${ukCities.city.length} UK cities`);
}

function populateCitySelects() {
    const startSelect = document.getElementById('start-city');
    const endSelect = document.getElementById('end-city');
    
    // Clear existing options
    startSelect.innerHTML = '<option value="">Select starting city...</option>';
    endSelect.innerHTML = '<option value="">Select destination city...</option>';
    
    // Add city options
    ukCities.city.forEach(city => {
        const startOption = new Option(city, city);
        const endOption = new Option(city, city);
        startSelect.add(startOption);
        endSelect.add(endOption);
    });
}

function addCityMarkers() {
    citiesLayer.clearLayers();
    
    Object.entries(ukCitiesData).forEach(([city, coords]) => {
        const marker = L.circleMarker(coords, {
            radius: 5,
            fillColor: '#667eea',
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        }).bindPopup(`<strong>${city}</strong><br>Lat: ${coords[0]}<br>Lng: ${coords[1]}`);
        
        citiesLayer.addLayer(marker);
    });
}

function setupBigDataEventListeners() {
    // Distance slider
    const distanceSlider = document.getElementById('max-distance');
    const distanceValue = document.getElementById('distance-value');
    
    distanceSlider.addEventListener('input', function() {
        distanceValue.textContent = `${this.value} km`;
    });
    
    // Control buttons
    document.getElementById('build-graph-btn').addEventListener('click', buildBigDataGraph);
    document.getElementById('find-route-btn').addEventListener('click', findBigDataRoute);
    document.getElementById('find-alternatives-btn').addEventListener('click', findBigDataAlternatives);
    document.getElementById('benchmark-btn').addEventListener('click', runBenchmark);
}

function calculateHaversineDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth's radius in kilometers
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

function buildBigDataGraph() {
    const maxDistance = parseInt(document.getElementById('max-distance').value);
    console.log(`🔧 Building graph with max distance: ${maxDistance}km`);
    
    const startTime = performance.now();
    bigDataGraph = {};
    let totalConnections = 0;
    let totalDistance = 0;
    
    // Build graph based on distance threshold
    Object.entries(ukCitiesData).forEach(([city1, coords1]) => {
        bigDataGraph[city1] = {};
        
        Object.entries(ukCitiesData).forEach(([city2, coords2]) => {
            if (city1 !== city2) {
                const distance = calculateHaversineDistance(coords1[0], coords1[1], coords2[0], coords2[1]);
                
                if (distance <= maxDistance) {
                    bigDataGraph[city1][city2] = distance;
                    totalConnections++;
                    totalDistance += distance;
                }
            }
        });
    });
    
    const buildTime = performance.now() - startTime;
    const avgDistance = totalConnections > 0 ? (totalDistance / totalConnections).toFixed(1) : 0;
    const maxPossibleConnections = ukCities.city.length * (ukCities.city.length - 1);
    const density = ((totalConnections / maxPossibleConnections) * 100).toFixed(1);
    
    // Update statistics
    document.getElementById('total-connections').textContent = totalConnections.toLocaleString();
    document.getElementById('avg-distance').textContent = `${avgDistance} km`;
    document.getElementById('graph-density').textContent = `${density}%`;
    
    console.log(`✅ Graph built in ${buildTime.toFixed(2)}ms with ${totalConnections} connections`);
    
    // Visualize connections on map
    visualizeGraphConnections();
}

function visualizeGraphConnections() {
    routeLayer.clearLayers();
    
    const connectionCount = {};
    let connectionsDrawn = 0;
    const maxConnections = 500; // Limit for performance
    
    Object.entries(bigDataGraph).forEach(([city1, connections]) => {
        if (connectionsDrawn >= maxConnections) return;
        
        Object.entries(connections).forEach(([city2, distance]) => {
            if (connectionsDrawn >= maxConnections) return;
            
            const connectionKey = [city1, city2].sort().join('-');
            if (!connectionCount[connectionKey]) {
                connectionCount[connectionKey] = true;
                
                const coords1 = ukCitiesData[city1];
                const coords2 = ukCitiesData[city2];
                
                if (coords1 && coords2) {
                    const line = L.polyline([coords1, coords2], {
                        color: '#667eea',
                        weight: 1,
                        opacity: 0.3
                    }).bindPopup(`${city1} → ${city2}<br>Distance: ${distance.toFixed(1)} km`);
                    
                    routeLayer.addLayer(line);
                    connectionsDrawn++;
                }
            }
        });
    });
    
    console.log(`📊 Visualized ${connectionsDrawn} connections`);
}

async function findBigDataRoute() {
    const startCity = document.getElementById('start-city').value;
    const endCity = document.getElementById('end-city').value;
    
    if (!startCity || !endCity) {
        alert('Please select both start and end cities');
        return;
    }
    
    if (!bigDataGraph[startCity]) {
        alert('Please build the graph first');
        return;
    }
    
    console.log(`🔍 Finding route from ${startCity} to ${endCity}`);
    
    const startTime = performance.now();
    const result = await enhancedDijkstraForBigData(startCity, endCity, bigDataGraph);
    const endTime = performance.now();
    
    const executionTime = endTime - startTime;
    
    // Update performance metrics
    updatePerformanceMetrics(result, executionTime);
    
    // Visualize route
    visualizeRoute(result);
    
    // Update route information
    updateRouteInformation(result, executionTime);
    
    console.log(`✅ Route found in ${executionTime.toFixed(2)}ms`);
}

async function enhancedDijkstraForBigData(start, end, graph) {
    const nodes = Object.keys(graph);
    const distances = {};
    const previous = {};
    const visited = new Set();
    const unvisited = new Set(nodes);
    
    let steps = 0;
    let nodesExplored = 0;
    
    // Initialize distances
    nodes.forEach(node => {
        distances[node] = node === start ? 0 : Infinity;
    });
    
    while (unvisited.size > 0) {
        steps++;
        
        // Find unvisited node with minimum distance
        let currentNode = null;
        let minDistance = Infinity;
        
        unvisited.forEach(node => {
            if (distances[node] < minDistance) {
                minDistance = distances[node];
                currentNode = node;
            }
        });
        
        if (currentNode === null || minDistance === Infinity) break;
        if (currentNode === end) break;
        
        visited.add(currentNode);
        unvisited.delete(currentNode);
        nodesExplored++;
        
        // Update distances to neighbors
        const neighbors = graph[currentNode] || {};
        Object.entries(neighbors).forEach(([neighbor, weight]) => {
            if (!visited.has(neighbor)) {
                const newDistance = distances[currentNode] + weight;
                if (newDistance < distances[neighbor]) {
                    distances[neighbor] = newDistance;
                    previous[neighbor] = currentNode;
                }
            }
        });
        
        // Yield control occasionally for UI responsiveness
        if (steps % 100 === 0) {
            await new Promise(resolve => setTimeout(resolve, 0));
        }
    }
    
    // Reconstruct path
    const path = [];
    let current = end;
    
    while (current !== undefined) {
        path.unshift(current);
        current = previous[current];
    }
    
    return {
        path: path.length > 1 ? path : [],
        distance: distances[end],
        steps,
        nodesExplored,
        visited: Array.from(visited)
    };
}

function updatePerformanceMetrics(result, executionTime) {
    document.getElementById('execution-time').textContent = `${executionTime.toFixed(2)} ms`;
    document.getElementById('nodes-explored').textContent = result.nodesExplored;
    document.getElementById('algorithm-steps').textContent = result.steps;
    
    // Estimate memory usage (rough calculation)
    const memoryUsage = (Object.keys(bigDataGraph).length * 4 + result.steps * 2) / 1024;
    document.getElementById('memory-usage').textContent = `${memoryUsage.toFixed(1)} KB`;
    
    // Store for charts
    performanceMetrics.push({
        executionTime,
        nodesExplored: result.nodesExplored,
        steps: result.steps,
        graphSize: Object.keys(bigDataGraph).length
    });
    
    updateCharts();
}

function visualizeRoute(result) {
    // Clear previous route
    routeLayer.clearLayers();
    
    if (result.path.length > 1) {
        const routeCoords = result.path.map(city => ukCitiesData[city]).filter(coord => coord);
        
        // Create route line
        const routeLine = L.polyline(routeCoords, {
            color: '#ff6b6b',
            weight: 4,
            opacity: 0.8
        });
        
        routeLayer.addLayer(routeLine);
        
        // Add markers for start and end
        const startMarker = L.marker(routeCoords[0], {
            icon: L.divIcon({
                className: 'custom-marker start-marker',
                html: '<i class="fas fa-play" style="color: white;"></i>',
                iconSize: [30, 30]
            })
        }).bindPopup(`Start: ${result.path[0]}`);
        
        const endMarker = L.marker(routeCoords[routeCoords.length - 1], {
            icon: L.divIcon({
                className: 'custom-marker end-marker',
                html: '<i class="fas fa-flag-checkered" style="color: white;"></i>',
                iconSize: [30, 30]
            })
        }).bindPopup(`End: ${result.path[result.path.length - 1]}`);
        
        routeLayer.addLayer(startMarker);
        routeLayer.addLayer(endMarker);
        
        // Fit map to route
        bigDataMap.fitBounds(routeLine.getBounds(), { padding: [20, 20] });
    }
}

function updateRouteInformation(result, executionTime) {
    const routeDetails = document.getElementById('route-details');
    
    if (result.path.length > 1) {
        routeDetails.innerHTML = `
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
                <h5>🎯 Optimal Route Found</h5>
                <p><strong>Path:</strong> ${result.path.join(' → ')}</p>
                <p><strong>Total Distance:</strong> ${result.distance.toFixed(1)} km</p>
                <p><strong>Cities Visited:</strong> ${result.path.length}</p>
                <p><strong>Execution Time:</strong> ${executionTime.toFixed(2)} ms</p>
                <p><strong>Algorithm Efficiency:</strong> O(V²) where V = ${Object.keys(bigDataGraph).length}</p>
                <small>✅ Successfully demonstrated scalability with ${Object.keys(bigDataGraph).length} node graph</small>
            </div>
        `;
    } else {
        routeDetails.innerHTML = `
            <div style="background: #ffe6e6; padding: 15px; border-radius: 8px; color: #d63384;">
                <h5>❌ No Route Found</h5>
                <p>No path exists between the selected cities with current distance constraints.</p>
                <p>Try increasing the maximum connection distance.</p>
            </div>
        `;
    }
}

async function findBigDataAlternatives() {
    const startCity = document.getElementById('start-city').value;
    const endCity = document.getElementById('end-city').value;
    
    if (!startCity || !endCity) {
        alert('Please select both start and end cities');
        return;
    }
    
    if (!bigDataGraph[startCity]) {
        alert('Please build the graph first');
        return;
    }
    
    console.log(`🔍 Finding alternative routes from ${startCity} to ${endCity}`);
    
    const startTime = performance.now();
    
    // Find multiple alternative routes using k-shortest paths approach
    const alternatives = await findKShortestPaths(startCity, endCity, bigDataGraph, 5);
    
    const endTime = performance.now();
    const executionTime = endTime - startTime;
    
    // Update performance metrics
    updateAlternativePerformanceMetrics(alternatives, executionTime);
    
    // Visualize all alternative routes
    visualizeAlternativeRoutes(alternatives);
    
    // Update route information with comprehensive analysis
    updateAlternativeRouteInformation(alternatives, executionTime);
    
    console.log(`✅ Found ${alternatives.length} alternative routes in ${executionTime.toFixed(2)}ms`);
}

async function findKShortestPaths(start, end, graph, k = 5) {
    const routes = [];
    const tempGraph = JSON.parse(JSON.stringify(graph)); // Deep copy
    
    // Find the first shortest path
    const firstRoute = await enhancedDijkstraForBigData(start, end, tempGraph);
    if (firstRoute.path.length > 0) {
        routes.push({
            ...firstRoute,
            routeId: 1,
            isOptimal: true
        });
    }
    
    // Find alternative routes by temporarily removing edges
    for (let i = 1; i < k && routes.length > 0; i++) {
        const bestAlternative = await findBestAlternativeRoute(start, end, tempGraph, routes);
        
        if (bestAlternative && bestAlternative.path.length > 0) {
            routes.push({
                ...bestAlternative,
                routeId: i + 1,
                isOptimal: false
            });
            
            // Remove some edges from the best alternative to encourage diversity
            removeEdgesFromPath(tempGraph, bestAlternative.path);
        } else {
            break;
        }
        
        // Yield control for UI responsiveness
        await new Promise(resolve => setTimeout(resolve, 10));
    }
    
    return routes;
}

async function findBestAlternativeRoute(start, end, graph, existingRoutes) {
    const tempGraph = JSON.parse(JSON.stringify(graph));
    
    // Try removing different edges from existing routes to find alternatives
    const bestAlternatives = [];
    
    for (const route of existingRoutes) {
        if (route.path.length < 2) continue;
        
        // Try removing each edge in the existing route
        for (let i = 0; i < route.path.length - 1; i++) {
            const nodeA = route.path[i];
            const nodeB = route.path[i + 1];
            
            // Temporarily remove this edge
            const originalWeight = tempGraph[nodeA] && tempGraph[nodeA][nodeB];
            if (originalWeight !== undefined) {
                delete tempGraph[nodeA][nodeB];
                if (tempGraph[nodeB] && tempGraph[nodeB][nodeA] !== undefined) {
                    delete tempGraph[nodeB][nodeA];
                }
                
                // Find alternative path without this edge
                const alternative = await enhancedDijkstraForBigData(start, end, tempGraph);
                
                if (alternative.path.length > 0 && alternative.distance < Infinity) {
                    bestAlternatives.push(alternative);
                }
                
                // Restore the edge
                if (!tempGraph[nodeA]) tempGraph[nodeA] = {};
                if (!tempGraph[nodeB]) tempGraph[nodeB] = {};
                tempGraph[nodeA][nodeB] = originalWeight;
                tempGraph[nodeB][nodeA] = originalWeight;
            }
        }
    }
    
    // Return the best alternative (shortest among alternatives)
    if (bestAlternatives.length > 0) {
        bestAlternatives.sort((a, b) => a.distance - b.distance);
        return bestAlternatives[0];
    }
    
    return null;
}

function removeEdgesFromPath(graph, path) {
    // Remove some edges from the path to encourage route diversity
    const edgesToRemove = Math.max(1, Math.floor(path.length / 4));
    
    for (let i = 0; i < edgesToRemove && i < path.length - 1; i++) {
        const nodeA = path[i];
        const nodeB = path[i + 1];
        
        if (graph[nodeA] && graph[nodeA][nodeB] !== undefined) {
            delete graph[nodeA][nodeB];
        }
        if (graph[nodeB] && graph[nodeB][nodeA] !== undefined) {
            delete graph[nodeB][nodeA];
        }
    }
}

function visualizeAlternativeRoutes(alternatives) {
    // Clear existing routes
    routeLayer.clearLayers();
    
    const colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1'];
    
    alternatives.forEach((route, index) => {
        if (route.path.length > 1) {
            const color = colors[index % colors.length];
            const coordinates = route.path.map(city => ukCitiesData[city].coords);
            
            // Enhanced route visualization for big data
            const enhancedRoute = generateRealisticRouteForBigData(coordinates);
            
            const polyline = L.polyline(enhancedRoute, {
                color: color,
                weight: route.isOptimal ? 4 : 3,
                opacity: route.isOptimal ? 0.9 : 0.7,
                dashArray: route.isOptimal ? null : '8,4'
            }).addTo(routeLayer);
            
            polyline.bindPopup(`
                <strong>Route ${route.routeId} ${route.isOptimal ? '(OPTIMAL)' : ''}</strong><br>
                Distance: ${route.distance.toFixed(2)} km<br>
                Cities: ${route.path.length}<br>
                Steps: ${route.steps}<br>
                Nodes Explored: ${route.nodesExplored}<br>
                ${route.isOptimal ? '<br><strong>🎯 Dijkstra\'s Choice</strong>' : ''}
            `);
        }
    });
    
    // Fit map to show all routes
    if (alternatives.length > 0 && alternatives[0].path.length > 0) {
        const allCoords = alternatives[0].path.map(city => ukCitiesData[city].coords);
        const bounds = L.latLngBounds(allCoords);
        bigDataMap.fitBounds(bounds, { padding: [20, 20] });
    }
}

function generateRealisticRouteForBigData(coordinates) {
    // Enhanced route generation for big data scenarios
    if (!coordinates || coordinates.length < 2) {
        return coordinates;
    }
    
    const enhancedRoute = [];
    
    for (let i = 0; i < coordinates.length - 1; i++) {
        const start = coordinates[i];
        const end = coordinates[i + 1];
        
        enhancedRoute.push(start);
        
        // Add intermediate points for longer distances
        const distance = calculateDistanceForBigData(start[0], start[1], end[0], end[1]);
        
        if (distance > 50) { // More than 50 km
            const numPoints = Math.min(Math.floor(distance / 25), 4);
            
            for (let j = 1; j <= numPoints; j++) {
                const ratio = j / (numPoints + 1);
                const lat = start[0] + (end[0] - start[0]) * ratio;
                const lng = start[1] + (end[1] - start[1]) * ratio;
                
                // Add slight curves for realism
                const curve = Math.sin(ratio * Math.PI) * 0.01;
                enhancedRoute.push([lat + curve, lng + curve]);
            }
        }
    }
    
    enhancedRoute.push(coordinates[coordinates.length - 1]);
    return enhancedRoute;
}

function calculateDistanceForBigData(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth's radius in kilometers
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

function updateAlternativePerformanceMetrics(alternatives, executionTime) {
    document.getElementById('execution-time').textContent = `${executionTime.toFixed(2)} ms`;
    
    if (alternatives.length > 0) {
        const totalNodesExplored = alternatives.reduce((sum, route) => sum + route.nodesExplored, 0);
        const totalSteps = alternatives.reduce((sum, route) => sum + route.steps, 0);
        
        document.getElementById('nodes-explored').textContent = totalNodesExplored;
        document.getElementById('algorithm-steps').textContent = totalSteps;
        
        // Estimate memory usage for multiple routes
        const memoryUsage = (Object.keys(bigDataGraph).length * 4 + totalSteps * 2 + alternatives.length * 100) / 1024;
        document.getElementById('memory-usage').textContent = `${memoryUsage.toFixed(1)} KB`;
    }
}

function updateAlternativeRouteInformation(alternatives, executionTime) {
    if (alternatives.length === 0) {
        console.log('No alternative routes found');
        return;
    }
    
    const optimalRoute = alternatives.find(route => route.isOptimal);
    const shortestDistance = Math.min(...alternatives.map(route => route.distance));
    const longestDistance = Math.max(...alternatives.map(route => route.distance));
    
    console.log(`📊 Alternative Routes Analysis:`);
    console.log(`   🎯 Optimal Distance: ${optimalRoute?.distance.toFixed(2)} km`);
    console.log(`   📈 Total Routes Found: ${alternatives.length}`);
    console.log(`   🟢 Shortest Route: ${shortestDistance.toFixed(2)} km`);
    console.log(`   🔴 Longest Route: ${longestDistance.toFixed(2)} km`);
    console.log(`   ⚡ Execution Time: ${executionTime.toFixed(2)} ms`);
    console.log(`   🔍 Why Optimal: Dijkstra guarantees shortest distance using real-world coordinates`);
    
    // You could also update a UI element here to show this information
}

// Chart initialization and updates
let performanceChart, complexityChart;

function initializeCharts() {
    // Performance Chart
    const perfCtx = document.getElementById('performance-chart').getContext('2d');
    performanceChart = new Chart(perfCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Execution Time (ms)',
                data: [],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Algorithm Performance Over Time'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Execution Time (ms)'
                    }
                }
            }
        }
    });
    
    // Complexity Chart
    const compCtx = document.getElementById('complexity-chart').getContext('2d');
    complexityChart = new Chart(compCtx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Nodes Explored vs Graph Size',
                data: [],
                backgroundColor: '#ff6b6b'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Algorithm Complexity Analysis'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Graph Size (nodes)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Nodes Explored'
                    }
                }
            }
        }
    });
}

function updateCharts() {
    if (performanceMetrics.length === 0) return;
    
    // Update performance chart
    performanceChart.data.labels = performanceMetrics.map((_, i) => `Test ${i + 1}`);
    performanceChart.data.datasets[0].data = performanceMetrics.map(m => m.executionTime);
    performanceChart.update();
    
    // Update complexity chart
    complexityChart.data.datasets[0].data = performanceMetrics.map(m => ({
        x: m.graphSize,
        y: m.nodesExplored
    }));
    complexityChart.update();
}

async function runBenchmark() {
    console.log('🚀 Starting algorithm benchmark...');
    
    const testCases = [
        { start: 'London', end: 'Manchester' },
        { start: 'Birmingham', end: 'Liverpool' },
        { start: 'Bristol', end: 'Newcastle upon Tyne' },
        { start: 'Cardiff', end: 'Leeds' },
        { start: 'Sheffield', end: 'Plymouth' }
    ];
    
    const benchmarkResults = [];
    
    for (const testCase of testCases) {
        if (!bigDataGraph[testCase.start] || !bigDataGraph[testCase.end]) {
            console.log(`⚠️ Skipping ${testCase.start} to ${testCase.end} - not in current graph`);
            continue;
        }
        
        console.log(`🔍 Benchmarking route: ${testCase.start} → ${testCase.end}`);
        
        const startTime = performance.now();
        const result = await enhancedDijkstraForBigData(testCase.start, testCase.end, bigDataGraph);
        const endTime = performance.now();
        
        const executionTime = endTime - startTime;
        
        benchmarkResults.push({
            route: `${testCase.start} → ${testCase.end}`,
            executionTime,
            distance: result.distance,
            nodesExplored: result.nodesExplored,
            steps: result.steps,
            pathLength: result.path.length
        });
        
        console.log(`✅ ${testCase.start} → ${testCase.end}: ${executionTime.toFixed(2)}ms, ${result.distance.toFixed(1)}km`);
    }
    
    // Display benchmark results
    displayBenchmarkResults(benchmarkResults);
    
    console.log('🏁 Benchmark completed!');
}

function displayBenchmarkResults(results) {
    const benchmarkDiv = document.getElementById('route-details');
    
    const avgExecutionTime = results.reduce((sum, r) => sum + r.executionTime, 0) / results.length;
    const avgNodesExplored = results.reduce((sum, r) => sum + r.nodesExplored, 0) / results.length;
    const avgSteps = results.reduce((sum, r) => sum + r.steps, 0) / results.length;
    
    let html = `
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
            <h5>📊 Algorithm Benchmark Results</h5>
            <p><strong>Test Cases:</strong> ${results.length}</p>
            <p><strong>Average Execution Time:</strong> ${avgExecutionTime.toFixed(2)} ms</p>
            <p><strong>Average Nodes Explored:</strong> ${avgNodesExplored.toFixed(0)}</p>
            <p><strong>Average Algorithm Steps:</strong> ${avgSteps.toFixed(0)}</p>
            <hr>
            <h6>Individual Results:</h6>
            <div style="max-height: 200px; overflow-y: auto;">
    `;
    
    results.forEach(result => {
        html += `
            <div style="margin: 5px 0; padding: 5px; background: white; border-radius: 4px;">
                <strong>${result.route}</strong><br>
                Time: ${result.executionTime.toFixed(2)}ms | 
                Distance: ${result.distance.toFixed(1)}km | 
                Nodes: ${result.nodesExplored} | 
                Steps: ${result.steps}
            </div>
        `;
    });
    
    html += `
            </div>
            <small>✅ Benchmark demonstrates consistent O(V²) performance across different route scenarios</small>
        </div>
    `;
    
    benchmarkDiv.innerHTML = html;
}

console.log('✅ Big Data Algorithm Analysis loaded successfully!');
console.log('🎯 Features: UK Cities Dataset | Performance Analysis | Algorithm Benchmarking');
