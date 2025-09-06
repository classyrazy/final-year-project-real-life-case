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
let isEmergencyMode = false;

// DOM Elements
const startLocationSelect = document.getElementById('startLocation');
const endLocationSelect = document.getElementById('endLocation');
const findRouteBtn = document.getElementById('findRoute');
const clearRouteBtn = document.getElementById('clearRoute');
const emergencyBtn = document.getElementById('emergencyRoute');
const alternativeRoutesBtn = document.getElementById('alternativeRoutes');
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
    emergencyBtn?.addEventListener('click', handleEmergency);
    alternativeRoutesBtn?.addEventListener('click', findAlternativeRoutes);
    
    // Algorithm visualization controls
    prevStepBtn?.addEventListener('click', () => showAlgorithmStep(currentStepIndex - 1));
    nextStepBtn?.addEventListener('click', () => showAlgorithmStep(currentStepIndex + 1));
    autoPlayBtn?.addEventListener('click', toggleAutoPlay);
    
    console.log('🎛️ Event listeners set up');
}

async function findRoute() {
    const startLocation = startLocationSelect.value;
    const endLocation = endLocationSelect.value;
    
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
        
        const response = await fetch('http://localhost:5001/api/shortest-path', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                start: startLocation,
                end: endLocation
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP ${response.status}`);
        }
        
        const routeData = await response.json();
        
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
        console.log('✅ Route found and displayed');
        
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
        showLoading('Finding alternative routes...');
        
        const response = await fetch('http://localhost:5001/api/alternative-routes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                start: startLocation,
                end: endLocation,
                k: 3
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP ${response.status}`);
        }
        
        const data = await response.json();
        alternativeRoutes = data.routes || [];
        
        displayAlternativeRoutes(alternativeRoutes);
        hideLoading();
        
        console.log(`✅ Found ${data.count} alternative routes`);
        
    } catch (error) {
        console.error('❌ Error finding alternative routes:', error);
        hideLoading();
        showError(`Failed to find alternative routes: ${error.message}`);
    }
}

async function handleEmergency() {
    const startLocation = startLocationSelect.value;
    
    if (!startLocation) {
        showError('Please select your current location for emergency routing');
        return;
    }
    
    // Toggle emergency mode
    isEmergencyMode = !isEmergencyMode;
    document.body.classList.toggle('emergency-mode', isEmergencyMode);
    
    if (isEmergencyMode) {
        try {
            showLoading('Finding emergency route...');
            
            const response = await fetch('http://localhost:5001/api/emergency-route', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    start: startLocation,
                    emergency_type: 'medical'
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }
            
            const emergencyRoute = await response.json();
            currentRoute = emergencyRoute;
            
            displayRoute(emergencyRoute);
            displayEmergencyInfo(emergencyRoute);
            
            hideLoading();
            emergencyBtn.innerHTML = '<i class="fas fa-times"></i> Exit Emergency Mode';
            
        } catch (error) {
            console.error('❌ Error finding emergency route:', error);
            hideLoading();
            showError(`Failed to find emergency route: ${error.message}`);
            isEmergencyMode = false;
            document.body.classList.remove('emergency-mode');
        }
    } else {
        clearRoute();
        emergencyBtn.innerHTML = '<i class="fas fa-ambulance"></i> Emergency Route';
    }
}

function displayRoute(routeData) {
    routeLayer.clearLayers();
    
    if (routeData.path_coordinates && routeData.path_coordinates.length > 0) {
        // Draw route polyline
        const routePolyline = L.polyline(routeData.path_coordinates, {
            color: isEmergencyMode ? '#dc3545' : '#007bff',
            weight: 4,
            opacity: 0.8
        }).addTo(routeLayer);
        
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

function displayAlternativeRoutes(routes) {
    routeLayer.clearLayers();
    
    const colors = ['#007bff', '#28a745', '#ffc107', '#dc3545'];
    
    routes.forEach((route, index) => {
        if (route.path_coordinates && route.path_coordinates.length > 0) {
            const color = colors[index % colors.length];
            const polyline = L.polyline(route.path_coordinates, {
                color: color,
                weight: 3,
                opacity: 0.7,
                dashArray: index === 0 ? null : '10,5'
            }).addTo(routeLayer);
            
            polyline.bindPopup(`
                <strong>Route ${index + 1}</strong><br>
                Distance: ${route.distance_km ? route.distance_km + ' km' : route.distance || 'N/A'}<br>
                Walking Time: ${route.walking_time_minutes || 'N/A'} minutes<br>
                Nodes: ${route.path ? route.path.length : 0}
            `);
        }
    });
    
    // Update route info
    if (routes.length > 0) {
        routeInfo.innerHTML = `
            <div class="alert alert-info">
                <h5><i class="fas fa-route"></i> Alternative Routes Found</h5>
                <p>Found ${routes.length} alternative routes using enhanced pathfinding. Click on any route to see details.</p>
                ${routes.map((route, index) => `
                    <div class="route-option" style="border-left: 4px solid ${colors[index % colors.length]}; margin-bottom: 10px; padding: 10px;">
                        <strong>Route ${index + 1}:</strong> ${route.path ? route.path.join(' → ') : 'N/A'}
                        <br><small><strong>Distance:</strong> ${route.distance_km ? route.distance_km + ' km' : route.distance || 'N/A'} | 
                        <strong>Time:</strong> ${route.walking_time_minutes || 'N/A'} min | 
                        <strong>Nodes:</strong> ${route.path ? route.path.length : 0}</small>
                    </div>
                `).join('')}
                <small class="text-muted"><i class="fas fa-info-circle"></i> All distances calculated using real-world Haversine distances.</small>
            </div>
        `;
    }
}

function displayRouteInfo(routeData) {
    const optimizationInfo = routeData.optimization_info || {};
    
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

function displayEmergencyInfo(routeData) {
    routeInfo.innerHTML = `
        <div class="alert alert-danger">
            <h5><i class="fas fa-ambulance"></i> Emergency Route</h5>
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Emergency Type:</strong> ${routeData.emergency_type || 'Medical'}</p>
                    <p><strong>Destination:</strong> ${routeData.destination_type || 'Emergency Facility'}</p>
                    <p><strong>Priority:</strong> ${routeData.priority || 'HIGH'}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Distance:</strong> ${routeData.total_distance}m</p>
                    <p><strong>Estimated Time:</strong> ${routeData.estimated_time} minutes</p>
                    <p><strong>Path:</strong> ${routeData.path.join(' → ')}</p>
                </div>
            </div>
            <div class="mt-2">
                <small><i class="fas fa-exclamation-triangle"></i> <strong>Emergency Mode Active:</strong> Fastest route to nearest emergency facility</small>
            </div>
        </div>
    `;
}

function showAlgorithmVisualization() {
    if (currentSteps.length === 0) return;
    
    algorithmPanel.style.display = 'block';
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
    
    // Exit emergency mode
    isEmergencyMode = false;
    document.body.classList.remove('emergency-mode');
    emergencyBtn.innerHTML = '<i class="fas fa-ambulance"></i> Emergency Route';
    
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
