/**
 * UNILAG Campus Navigation System
 * Enhanced with Algorithm Visualization and Alternative Routing
 */

let map;
let routeLayer;
let markersLayer;
let currentSteps = [];
let currentStepIndex = 0;
let autoPlayInterval;
let currentRoute = null;
let alternativeRoutes = [];

// DOM Elements
const startLocationSelect = document.getElementById('startLocation');
const endLocationSelect = document.getElementById('endLocation');
const findRouteBtn = document.getElementById('findRoute');
const clearRouteBtn = document.getElementById('clearRoute');
const alternativeRoutesBtn = document.getElementById('alternativeRoutes');
const toggleVisualizationBtn = document.getElementById('toggleVisualization');
const routeInfo = document.getElementById('routeInfo');
const algorithmPanel = document.getElementById('algorithm-panel');

// Algorithm visualization elements
const stepDescription = document.getElementById('step-description');
const currentNodeSpan = document.getElementById('current-node');
const visitedNodesSpan = document.getElementById('visited-nodes');
const queueStateSpan = document.getElementById('queue-state');
const stepCounter = document.getElementById('step-counter');
const prevStepBtn = document.getElementById('prev-step-btn');
const nextStepBtn = document.getElementById('next-step-btn');
const autoPlayBtn = document.getElementById('auto-play-btn');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing UNILAG Campus Navigation System...');
    
    // Re-get DOM elements to ensure they're available
    const startLocationSelect = document.getElementById('startLocation');
    const endLocationSelect = document.getElementById('endLocation');
    
    console.log('🔍 DOM elements check:');
    console.log('  startLocationSelect:', startLocationSelect);
    console.log('  endLocationSelect:', endLocationSelect);
    console.log('  map container:', document.getElementById('map'));
    
    if (!startLocationSelect || !endLocationSelect) {
        console.error('❌ Required DOM elements not found!');
        return;
    }
    
    try {
        initializeMap();
        loadCampusLocations();
        setupEventListeners();
        console.log('✅ Application initialized successfully');
    } catch (error) {
        console.error('❌ Error during initialization:', error);
        showError('Failed to initialize the application. Please refresh the page.');
    }
});

function initializeMap() {
    try {
        // Initialize Leaflet map centered on UNILAG
        map = L.map('map').setView([6.5158, 3.3968], 16);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(map);
        
        // Initialize layers
        markersLayer = L.layerGroup().addTo(map);
        routeLayer = L.layerGroup().addTo(map);
        
        console.log('🗺️ Map initialized successfully');
    } catch (error) {
        console.error('❌ Error initializing map:', error);
        throw new Error('Failed to initialize map');
    }
}

async function loadCampusLocations() {
    try {
        console.log('📍 Loading campus locations...');
        console.log('🔗 Fetching from: http://localhost:5001/api/nodes');
        
        const response = await fetch('http://localhost:5001/api/nodes');
        
        console.log('📊 Response status:', response.status);
        console.log('📊 Response headers:', response.headers);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('📊 Full API Response:', data);
        console.log('📊 Nodes array:', data.nodes);
        console.log('📊 Nodes count:', data.count);
        console.log('📊 First 5 nodes:', data.nodes?.slice(0, 5));
        console.log('📊 Coordinates keys:', Object.keys(data.coordinates || {}));
        
        if (!data.nodes || !Array.isArray(data.nodes) || data.nodes.length === 0) {
            throw new Error('No location data received from API');
        }
        
        // Test direct select manipulation
        console.log('🧪 Testing direct select manipulation...');
        const testSelect = document.getElementById('startLocation');
        console.log('🧪 Start select element:', testSelect);
        console.log('🧪 Start select current options:', testSelect?.options?.length);
        
        console.log('🚀 About to call populateLocationSelects with', data.nodes.length, 'locations');
        populateLocationSelects(data.nodes);
        console.log('✅ populateLocationSelects completed');
        addLocationMarkers(data.nodes, data.coordinates);
        
        // Re-check after population
        console.log('🧪 After population - Start select options:', testSelect?.options?.length);
        
        console.log(`✅ Loaded ${data.count} campus locations`);
    } catch (error) {
        console.error('❌ Error loading campus locations:', error);
        console.error('❌ Error details:', {
            message: error.message,
            stack: error.stack
        });
        showError('Failed to load campus locations. Please ensure the server is running.');
    }
}

function populateLocationSelects(locations) {
    console.log('🚀 Starting populateLocationSelects function');
    console.log('🔍 Received locations:', locations);
    console.log('🔍 Locations type:', typeof locations, 'length:', locations?.length);
    
    // Get fresh DOM element references
    const startLocationSelect = document.getElementById('startLocation');
    const endLocationSelect = document.getElementById('endLocation');
    
    console.log('🔍 DOM elements found:');
    console.log('  startLocationSelect:', !!startLocationSelect, startLocationSelect);
    console.log('  endLocationSelect:', !!endLocationSelect, endLocationSelect);
    
    if (!startLocationSelect || !endLocationSelect) {
        console.error('❌ Location select elements not found');
        console.error('❌ Available elements with "Location" in ID:');
        const allElements = document.querySelectorAll('[id*="Location"]');
        allElements.forEach(el => console.error('  -', el.id, el));
        return;
    }
    
    console.log('📝 Populating select dropdowns with', locations.length, 'locations');
    
    // Clear existing options
    startLocationSelect.innerHTML = '<option value="">Select starting location</option>';
    endLocationSelect.innerHTML = '<option value="">Select destination</option>';
    
    console.log('📝 Cleared existing options, now adding new ones...');
    
    // Add location options
    locations.forEach((location, index) => {
        console.log(`📝 Adding location ${index + 1}/${locations.length}: "${location}"`);
        
        try {
            const startOption = new Option(location, location);
            const endOption = new Option(location, location);
            startLocationSelect.add(startOption);
            endLocationSelect.add(endOption);
            
            if (index < 3) { // Log first 3 for debugging
                console.log(`  ✅ Successfully added option ${index + 1}: ${location}`);
            }
        } catch (error) {
            console.error(`❌ Error adding option ${location}:`, error);
        }
    });
    
    console.log(`✅ Completed populating select dropdowns with ${locations.length} locations`);
    console.log('🔍 Final counts:');
    console.log('  Start select options count:', startLocationSelect.options.length);
    console.log('  End select options count:', endLocationSelect.options.length);
    
    // Double-check by listing all options
    console.log('🔍 Start select options:');
    for (let i = 0; i < startLocationSelect.options.length; i++) {
        console.log(`  ${i}: ${startLocationSelect.options[i].text} (value: ${startLocationSelect.options[i].value})`);
    }
}

function addLocationMarkers(locations, coordinates) {
    if (!markersLayer) {
        console.warn('⚠️ Markers layer not initialized yet, skipping marker placement');
        return;
    }
    
    if (!coordinates) {
        console.warn('⚠️ No coordinates provided for markers');
        return;
    }
    
    markersLayer.clearLayers();
    let markersAdded = 0;
    
    locations.forEach(location => {
        if (coordinates[location]) {
            const [lat, lng] = coordinates[location];
            try {
                const marker = L.marker([lat, lng])
                    .bindPopup(`<strong>${location}</strong>`)
                    .addTo(markersLayer);
                markersAdded++;
            } catch (error) {
                console.error(`❌ Error adding marker for ${location}:`, error);
            }
        } else {
            console.warn(`⚠️ No coordinates found for location: ${location}`);
        }
    });
    
    console.log(`✅ Added ${markersAdded} markers to the map`);
}

function setupEventListeners() {
    // Route finding buttons
    findRouteBtn?.addEventListener('click', findRoute);
    clearRouteBtn?.addEventListener('click', clearRoute);
    alternativeRoutesBtn?.addEventListener('click', findAlternativeRoutes);
    toggleVisualizationBtn?.addEventListener('click', toggleAlgorithmVisualization);
    
    // Algorithm visualization controls
    prevStepBtn?.addEventListener('click', () => showAlgorithmStep(currentStepIndex - 1));
    nextStepBtn?.addEventListener('click', () => showAlgorithmStep(currentStepIndex + 1));
    autoPlayBtn?.addEventListener('click', toggleAutoPlay);
    
    console.log('🎛️ Event listeners set up');
}

async function findRoute() {
    const startLocation = startLocationSelect.value;
    const endLocation = endLocationSelect.value;
    
    console.log('🚀 Finding route from:', startLocation, 'to:', endLocation);
    
    if (!startLocation || !endLocation) {
        showError('Please select both starting location and destination');
        return;
    }
    
    if (startLocation === endLocation) {
        showError('Starting location and destination cannot be the same');
        return;
    }
    
    try {
        showLoading('Finding optimal route...');
        
        console.log('📡 Making API request to shortest-path endpoint...');
        const response = await fetch('http://localhost:5001/api/shortest-path', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                start: startLocation,
                end: endLocation
            })
        });
        
        console.log('📡 API Response status:', response.status);
        console.log('📡 API Response headers:', response.headers);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP ${response.status}`);
        }
        
        const routeData = await response.json();
        console.log('📊 Route data received:', routeData);
        console.log('📊 Path:', routeData.path);
        console.log('📊 Comprehensive analysis:', routeData.comprehensive_analysis);
        
        if (!routeData.path || routeData.path.length === 0) {
            throw new Error('No route found between selected locations');
        }
        
        currentRoute = routeData;
        currentSteps = routeData.algorithm_steps || [];
        currentStepIndex = 0;
        
        displayRoute(routeData);
        displayRouteInfo(routeData);
        showAlgorithmVisualization();
        
        hideLoading();
        console.log('✅ Route found and displayed successfully');
        
    } catch (error) {
        console.error('❌ Error finding route:', error);
        hideLoading();
        showError(`Failed to find route: ${error.message}`);
    }
}

async function findAlternativeRoutes() {
    const startLocation = startLocationSelect.value;
    const endLocation = endLocationSelect.value;
    
    if (!startLocation || !endLocation) {
        showError('Please select both starting location and destination');
        return;
    }
    
    try {
        showLoading('Finding all possible alternative routes...');
        
        const response = await fetch('http://localhost:5001/api/alternative-routes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                start: startLocation,
                end: endLocation,
                k: 5  // Show top 5 alternative routes
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP ${response.status}`);
        }
        
        const data = await response.json();
        alternativeRoutes = data.routes || [];
        
        displayAlternativeRoutes(alternativeRoutes, data.comprehensive_analysis, data.total_possible_paths);
        hideLoading();
        
        console.log(`✅ Found ${data.showing_top} of ${data.total_possible_paths} total possible routes`);
        
    } catch (error) {
        console.error('❌ Error finding alternative routes:', error);
        hideLoading();
        showError(`Failed to find alternative routes: ${error.message}`);
    }
}

async function displayRoute(routeData) {
    routeLayer.clearLayers();
    
    if (routeData.path_coordinates && routeData.path_coordinates.length > 0) {
        // Generate realistic campus-aware route
        const realisticRoute = generateCampusAwareRoute(routeData.path_coordinates);
        
        // Display the enhanced route
        const routePolyline = L.polyline(realisticRoute, {
            color: '#007bff',
            weight: 5,
            opacity: 0.8,
            smoothFactor: 1.0 // Smooth the polyline
        }).addTo(routeLayer);
        
        console.log('✅ Displaying campus-aware route with', realisticRoute.length, 'points');
        
        // Add start and end markers
        const startMarker = L.marker(routeData.path_coordinates[0], {
            icon: L.divIcon({
                className: 'custom-marker start-marker',
                html: '<i class="fas fa-play"></i>',
                iconSize: [30, 30]
            })
        }).bindPopup('Start: ' + routeData.path[0]).addTo(routeLayer);
        
        const endMarker = L.marker(routeData.path_coordinates[routeData.path_coordinates.length - 1], {
            icon: L.divIcon({
                className: 'custom-marker end-marker',
                html: '<i class="fas fa-flag-checkered"></i>',
                iconSize: [30, 30]
            })
        }).bindPopup('End: ' + routeData.path[routeData.path.length - 1]).addTo(routeLayer);
        
        // Fit map to route bounds
        map.fitBounds(routePolyline.getBounds(), { padding: [20, 20] });
    }
}

// Function to generate realistic pathways without external APIs
function generateRealisticRoute(coordinates) {
    if (!coordinates || coordinates.length < 2) {
        return coordinates;
    }
    
    const enhancedRoute = [];
    
    for (let i = 0; i < coordinates.length - 1; i++) {
        const start = coordinates[i];
        const end = coordinates[i + 1];
        
        // Add the start point
        enhancedRoute.push(start);
        
        // Calculate distance between points
        const distance = calculateDistance(start[0], start[1], end[0], end[1]);
        
        // If distance is significant, add intermediate points to create a more natural path
        if (distance > 0.2) { // More than 200 meters
            const intermediatePoints = generateIntermediatePoints(start, end, distance);
            enhancedRoute.push(...intermediatePoints);
        }
    }
    
    // Add the final point
    enhancedRoute.push(coordinates[coordinates.length - 1]);
    
    return enhancedRoute;
}

function generateIntermediatePoints(start, end, distance) {
    const points = [];
    const numPoints = Math.min(Math.floor(distance * 3), 8); // Max 8 intermediate points
    
    for (let i = 1; i <= numPoints; i++) {
        const ratio = i / (numPoints + 1);
        
        // Linear interpolation with slight curves
        const lat = start[0] + (end[0] - start[0]) * ratio;
        const lng = start[1] + (end[1] - start[1]) * ratio;
        
        // Add slight offset to create more natural curves
        const offsetLat = lat + (Math.sin(ratio * Math.PI) * 0.0001 * Math.random());
        const offsetLng = lng + (Math.cos(ratio * Math.PI) * 0.0001 * Math.random());
        
        points.push([offsetLat, offsetLng]);
    }
    
    return points;
}

function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth's radius in kilometers
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

// Enhanced function to create campus-aware pathways
function generateCampusAwareRoute(coordinates) {
    if (!coordinates || coordinates.length < 2) {
        return coordinates;
    }
    
    const campusRoutes = [];
    
    // Known campus pathways and roads (approximate coordinates for UNILAG)
    const campusPathways = [
        // Main road through campus
        { from: [6.5158, 3.3968], to: [6.5167, 3.3975], type: 'main_road' },
        { from: [6.5167, 3.3975], to: [6.5165, 3.3982], type: 'main_road' },
        { from: [6.5165, 3.3982], to: [6.5170, 3.3990], type: 'main_road' },
        
        // Secondary paths
        { from: [6.5160, 3.3970], to: [6.5168, 3.3985], type: 'pathway' },
        { from: [6.5162, 3.3972], to: [6.5169, 3.3988], type: 'pathway' },
    ];
    
    for (let i = 0; i < coordinates.length - 1; i++) {
        const start = coordinates[i];
        const end = coordinates[i + 1];
        
        campusRoutes.push(start);
        
        // Check if we can route through known pathways
        const pathwayRoute = findPathwayRoute(start, end, campusPathways);
        if (pathwayRoute && pathwayRoute.length > 0) {
            campusRoutes.push(...pathwayRoute);
        } else {
            // Generate realistic intermediate points
            const distance = calculateDistance(start[0], start[1], end[0], end[1]);
            if (distance > 0.1) {
                const intermediatePoints = generateCampusIntermediatePoints(start, end);
                campusRoutes.push(...intermediatePoints);
            }
        }
    }
    
    campusRoutes.push(coordinates[coordinates.length - 1]);
    
    return campusRoutes;
}

function findPathwayRoute(start, end, pathways) {
    // Simple pathway routing - find if there's a pathway that gets us closer to destination
    const route = [];
    
    for (const pathway of pathways) {
        const pathwayStart = pathway.from;
        const pathwayEnd = pathway.to;
        
        // Check if this pathway is useful for our route
        const distanceToPathwayStart = calculateDistance(start[0], start[1], pathwayStart[0], pathwayStart[1]);
        const distanceFromPathwayEnd = calculateDistance(pathwayEnd[0], pathwayEnd[1], end[0], end[1]);
        const directDistance = calculateDistance(start[0], start[1], end[0], end[1]);
        
        // If going through this pathway is not too much of a detour, use it
        if (distanceToPathwayStart < 0.2 && distanceFromPathwayEnd < directDistance) {
            // Add intermediate points to get to pathway start
            if (distanceToPathwayStart > 0.05) {
                route.push(...generateCampusIntermediatePoints(start, pathwayStart));
            }
            route.push(pathwayStart);
            
            // Add pathway itself with some intermediate points
            route.push(...generateCampusIntermediatePoints(pathwayStart, pathwayEnd));
            route.push(pathwayEnd);
            
            return route;
        }
    }
    
    return [];
}

function generateCampusIntermediatePoints(start, end) {
    const points = [];
    const distance = calculateDistance(start[0], start[1], end[0], end[1]);
    const numPoints = Math.min(Math.floor(distance * 5), 6); // More points for smoother paths
    
    for (let i = 1; i <= numPoints; i++) {
        const ratio = i / (numPoints + 1);
        
        // Create curved paths that might follow roads/walkways
        let lat = start[0] + (end[0] - start[0]) * ratio;
        let lng = start[1] + (end[1] - start[1]) * ratio;
        
        // Add slight curves to simulate following roads/paths
        const curve = Math.sin(ratio * Math.PI) * 0.00015;
        lat += curve * (Math.random() - 0.5);
        lng += curve * (Math.random() - 0.5);
        
        points.push([lat, lng]);
    }
    
    return points;
}

async function displayAlternativeRoutes(routes, comprehensiveAnalysis, totalPossiblePaths) {
    routeLayer.clearLayers();
    
    const colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1'];
    
    // Process routes and display them with realistic pathways
    routes.forEach((route, index) => {
        if (route.path_coordinates && route.path_coordinates.length > 0) {
            const color = colors[index % colors.length];
            
            // Generate realistic route for each alternative
            const realisticRoute = generateCampusAwareRoute(route.path_coordinates);
            
            // Display the enhanced route
            const polyline = L.polyline(realisticRoute, {
                color: color,
                weight: index === 0 ? 5 : 3,
                opacity: index === 0 ? 0.9 : 0.7,
                dashArray: index === 0 ? null : '8,4',
                smoothFactor: 1.0
            }).addTo(routeLayer);
            
            polyline.bindPopup(`
                <strong>Route ${index + 1} ${route.is_optimal ? '(OPTIMAL)' : ''}</strong><br>
                Distance: ${route.distance_km ? route.distance_km + ' km' : route.distance || 'N/A'}<br>
                Walking Time: ${route.walking_time_minutes || 'N/A'} minutes<br>
                Nodes: ${route.path ? route.path.length : 0}<br>
                ${route.is_optimal ? '<br><strong>🎯 Dijkstra\'s Choice</strong>' : ''}<br>
                <small>Campus-optimized pathway</small>
            `);
            
            console.log(`✅ Route ${index + 1}: Campus-aware route with ${realisticRoute.length} points`);
            
            // Add markers only for the first (optimal) route
            if (index === 0) {
                const startMarker = L.marker(route.path_coordinates[0], {
                    icon: L.divIcon({
                        className: 'custom-marker start-marker',
                        html: '<i class="fas fa-play"></i>',
                        iconSize: [30, 30]
                    })
                }).bindPopup('Start: ' + route.path[0]).addTo(routeLayer);
                
                const endMarker = L.marker(route.path_coordinates[route.path_coordinates.length - 1], {
                    icon: L.divIcon({
                        className: 'custom-marker end-marker',
                        html: '<i class="fas fa-flag-checkered"></i>',
                        iconSize: [30, 30]
                    })
                }).bindPopup('End: ' + route.path[route.path.length - 1]).addTo(routeLayer);
            }
        }
    });
    
    // Fit map to show all routes (use the first route for bounds)
    if (routes.length > 0 && routes[0].path_coordinates) {
        const bounds = L.latLngBounds(routes[0].path_coordinates);
        routes.forEach(route => {
            if (route.path_coordinates) {
                route.path_coordinates.forEach(coord => bounds.extend(coord));
            }
        });
        map.fitBounds(bounds, { padding: [20, 20] });
    }
    
    // Update route info with comprehensive analysis
    if (routes.length > 0) {
        let analysisHtml = '';
        if (comprehensiveAnalysis && comprehensiveAnalysis.dijkstra_choice) {
            analysisHtml = `
                <div class="mb-3" style="font-size: 16px; line-height: 1.6; background: #f8f9fa; padding: 15px; border-radius: 8px;">
                    <div><strong>${comprehensiveAnalysis.dijkstra_choice}</strong></div>
                    <div><strong>${comprehensiveAnalysis.total_routes_found}</strong></div>
                    <div><strong>${comprehensiveAnalysis.shortest_route}</strong></div>
                    <div><strong>${comprehensiveAnalysis.longest_route}</strong></div>
                    <div><strong>${comprehensiveAnalysis.why_optimal}</strong></div>
                </div>
            `;
        }
        
        routeInfo.innerHTML = `
            <div class="alert alert-info">
                <h5><i class="fas fa-route"></i> All Possible Routes Analysis</h5>
                ${analysisHtml}
                <p>Showing ${routes.length} routes out of ${totalPossiblePaths || 'N/A'} total possible paths. Routes are optimized for campus navigation.</p>
                ${routes.map((route, index) => `
                    <div class="route-option" style="border-left: 4px solid ${colors[index % colors.length]}; margin-bottom: 10px; padding: 10px; ${route.is_optimal ? 'background-color: #e8f5e8;' : ''}">
                        <strong>Route ${index + 1}${route.is_optimal ? ' 🎯 (OPTIMAL)' : ''}:</strong> ${route.path ? route.path.join(' → ') : 'N/A'}
                        <br><small><strong>Distance:</strong> ${route.distance_km ? route.distance_km + ' km' : route.distance || 'N/A'} | 
                        <strong>Time:</strong> ${route.walking_time_minutes || 'N/A'} min | 
                        <strong>Nodes:</strong> ${route.path ? route.path.length : 0}${route.is_optimal ? ' | <strong>Shortest Distance</strong>' : ''}</small>
                    </div>
                `).join('')}
                <small class="text-muted"><i class="fas fa-info-circle"></i> Routes use campus-optimized pathways with realistic curves and connections.</small>
            </div>
        `;
    }
}

function displayRouteInfo(routeData) {
    const optimizationInfo = routeData.optimization_info || {};
    const analysis = routeData.comprehensive_analysis || {};
    
    // Check if we have comprehensive analysis data
    if (analysis.dijkstra_choice) {
        routeInfo.innerHTML = `
            <div class="alert alert-success">
                <h5><i class="fas fa-route"></i> Route Analysis Complete</h5>
                <div class="mb-3" style="font-size: 16px; line-height: 1.6;">
                    <div><strong>${analysis.dijkstra_choice}</strong></div>
                    <div><strong>${analysis.total_routes_found}</strong></div>
                    <div><strong>${analysis.shortest_route}</strong></div>
                    <div><strong>${analysis.longest_route}</strong></div>
                    <div><strong>${analysis.why_optimal}</strong></div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Path:</strong> ${routeData.path.join(' → ')}</p>
                        <p><strong>Walking Time:</strong> ${routeData.walking_time_minutes} minutes</p>
                        <p><strong>Route Type:</strong> <span class="badge badge-info">Optimized Path</span></p>
                        <p><strong>All Possible Paths:</strong> ${routeData.all_possible_paths || 'N/A'}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Algorithm:</strong> ${optimizationInfo.algorithm || 'Enhanced Dijkstra with Haversine'}</p>
                        <p><strong>Nodes Explored:</strong> ${routeData.nodes_explored || 'N/A'}</p>
                        <p><strong>Academic Buildings:</strong> ${routeData.academic_buildings_passed || 0}</p>
                        <p><strong>Connected Nodes:</strong> ${routeData.connected_nodes_count || 'N/A'}</p>
                    </div>
                </div>
                <div class="mt-2">
                    <small class="text-muted"><i class="fas fa-info-circle"></i> Comprehensive analysis of all possible routes using enhanced pathfinding with depth-first search exploration.</small>
                </div>
            </div>
        `;
    } else {
        // Fallback to original display if comprehensive analysis not available
        routeInfo.innerHTML = `
            <div class="alert alert-success">
                <h5><i class="fas fa-route"></i> Enhanced Route Found</h5>
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Path:</strong> ${routeData.path.join(' → ')}</p>
                        <p><strong>Distance:</strong> ${routeData.total_distance_km || (routeData.total_distance / 1000).toFixed(3)} km (${routeData.total_distance}m)</p>
                        <p><strong>Walking Time:</strong> ${routeData.walking_time_minutes} minutes</p>
                        <p><strong>Route Type:</strong> <span class="badge badge-info">Real-world distances</span></p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Algorithm:</strong> ${optimizationInfo.algorithm || 'Enhanced Dijkstra with Haversine'}</p>
                        <p><strong>Distance Metric:</strong> ${optimizationInfo.distance_metric || 'Haversine distance'}</p>
                        <p><strong>Nodes Explored:</strong> ${routeData.nodes_explored || 'N/A'}</p>
                        <p><strong>Academic Buildings:</strong> ${routeData.academic_buildings_passed || 0}</p>
                    </div>
                </div>
                <div class="mt-2">
                    <small><strong>Why Optimal:</strong> ${optimizationInfo.why_optimal || 'Uses real-world distances for accurate routing'}</small>
                </div>
                <div class="mt-2">
                    <small class="text-muted"><i class="fas fa-info-circle"></i> Distances calculated using Haversine formula for accurate great-circle distances between coordinates.</small>
                </div>
            </div>
        `;
    }
}

function showAlgorithmVisualization() {
    if (currentSteps.length === 0) return;
    
    algorithmPanel.style.display = 'block';
    toggleVisualizationBtn.innerHTML = '<i class="fas fa-eye-slash"></i> Hide Algorithm';
    updateStepCounter();
    showAlgorithmStep(0);
}

function showAlgorithmStep(stepIndex) {
    if (!currentSteps || stepIndex < 0 || stepIndex >= currentSteps.length) return;
    
    currentStepIndex = stepIndex;
    const step = currentSteps[stepIndex];
    
    // Update step description
    stepDescription.textContent = step.description || 'Processing...';
    
    // Update algorithm state
    currentNodeSpan.textContent = step.current_node || '-';
    visitedNodesSpan.textContent = step.visited ? step.visited.join(', ') : 'None';
    queueStateSpan.textContent = step.queue ? step.queue.join(', ') : 'Empty';
    
    // Update step counter
    updateStepCounter();
    
    // Update button states
    prevStepBtn.disabled = stepIndex === 0;
    nextStepBtn.disabled = stepIndex === currentSteps.length - 1;
    
    console.log(`Showing algorithm step ${stepIndex + 1}/${currentSteps.length}`);
}

function updateStepCounter() {
    if (stepCounter) {
        stepCounter.textContent = `Step ${currentStepIndex + 1} of ${currentSteps.length}`;
    }
}

function toggleAutoPlay() {
    if (autoPlayInterval) {
        clearInterval(autoPlayInterval);
        autoPlayInterval = null;
        autoPlayBtn.innerHTML = '<i class="fas fa-play"></i> Auto Play';
    } else {
        autoPlayInterval = setInterval(() => {
            if (currentStepIndex < currentSteps.length - 1) {
                showAlgorithmStep(currentStepIndex + 1);
            } else {
                clearInterval(autoPlayInterval);
                autoPlayInterval = null;
                autoPlayBtn.innerHTML = '<i class="fas fa-play"></i> Auto Play';
            }
        }, 1500);
        autoPlayBtn.innerHTML = '<i class="fas fa-pause"></i> Pause';
    }
}

function toggleAlgorithmVisualization() {
    const isVisible = algorithmPanel.style.display !== 'none';
    
    if (isVisible) {
        // Hide the panel
        algorithmPanel.style.display = 'none';
        toggleVisualizationBtn.innerHTML = '<i class="fas fa-eye"></i> Show Algorithm';
        console.log('🔍 Algorithm visualization panel hidden');
    } else {
        // Show the panel
        algorithmPanel.style.display = 'block';
        toggleVisualizationBtn.innerHTML = '<i class="fas fa-eye-slash"></i> Hide Algorithm';
        
        // If we have algorithm steps, show them
        if (currentSteps.length > 0) {
            showAlgorithmVisualization();
        }
        console.log('🔍 Algorithm visualization panel shown');
    }
}

function clearRoute() {
    routeLayer.clearLayers();
    routeInfo.innerHTML = '';
    algorithmPanel.style.display = 'none';
    currentRoute = null;
    currentSteps = [];
    alternativeRoutes = [];
    
    if (autoPlayInterval) {
        clearInterval(autoPlayInterval);
        autoPlayInterval = null;
        autoPlayBtn.innerHTML = '<i class="fas fa-play"></i> Auto Play';
    }
    
    // Reset the visualization toggle button
    toggleVisualizationBtn.innerHTML = '<i class="fas fa-eye"></i> Show Algorithm';
    
    console.log('🧹 Route cleared');
}

// Utility functions
function showLoading(message) {
    routeInfo.innerHTML = `
        <div class="alert alert-info">
            <i class="fas fa-spinner fa-spin"></i> ${message}
        </div>
    `;
}

function hideLoading() {
    // Loading will be replaced by route info or cleared
}

function showError(message) {
    routeInfo.innerHTML = `
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle"></i> ${message}
        </div>
    `;
}

console.log('✅ UNILAG Campus Navigation System loaded successfully!');
console.log('🎯 Features: Enhanced Algorithm Visualization | Step-by-Step Analysis | Real-time Insights');
