#!/bin/bash

# UNILAG Campus Navigation System - Startup Script
# This script sets up and runs the campus navigation system

echo "🏫 UNILAG Campus Navigation System"
echo "=================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Navigate to project directory
cd "$(dirname "$0")"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your pip installation."
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Run tests first (optional)
read -p "🧪 Would you like to run tests first? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔍 Running system tests..."
    python3 test_system.py
    echo
fi

# Start the server
echo "🚀 Starting UNILAG Campus Navigation System..."
echo "📱 Frontend will be available at: http://localhost:8080"
echo "🔧 Backend API will be available at: http://localhost:5001"
echo "🛑 Press Ctrl+C to stop the servers"
echo
echo "Opening browser in 3 seconds..."

# Try to open browser automatically (macOS)
if command -v open &> /dev/null; then
    (sleep 3 && open http://localhost:8080) &
fi

# Start both servers
echo "🌐 Starting Frontend Server (port 8080)..."
python3 frontend_server.py &
FRONTEND_PID=$!

echo "⚡ Starting Backend API Server (port 5001)..."
python3 app.py &
BACKEND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "🛑 Stopping servers..."
    kill $FRONTEND_PID 2>/dev/null
    kill $BACKEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit
}

# Set trap to cleanup on script exit
trap cleanup INT TERM

echo "✅ Both servers are running!"
echo "📱 Frontend: http://localhost:8080"
echo "🔧 Backend: http://localhost:5001"

# Wait for both processes
wait
