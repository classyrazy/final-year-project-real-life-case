#!/usr/bin/env python3
"""
Simple frontend server for UNILAG Campus Navigation
Serves static files on port 8080
"""

import http.server
import socketserver
import os
from pathlib import Path

# Set the directory to serve (frontend folder)
frontend_dir = '/Users/mac/Desktop/school/final-year/UNILAG-Campus-Navigation/frontend'
os.chdir(frontend_dir)

# Create server
PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

print(f"🌐 Starting Frontend Server...")
print(f"📁 Serving files from: {frontend_dir}")
print(f"🔗 Frontend URL: http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"✅ Frontend server running on port {PORT}")
    print("Press Ctrl+C to stop")
    httpd.serve_forever()
