#!/usr/bin/env python3
"""
Startup script for YouTube Audio Extractor Web App
Builds the frontend and starts the Flask server
"""

import os
import subprocess
import sys
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")

    # Check Python dependencies
    try:
        import flask
        import flask_cors
        print("✅ Python dependencies OK")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

    # Check Node.js and npm
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} OK")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js from https://nodejs.org/")
        return False

    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm {result.stdout.strip()} OK")
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found. Please install npm")
        return False

    return True

def install_frontend_dependencies():
    """Install frontend dependencies"""
    print("📦 Installing frontend dependencies...")

    web_dir = Path('web')
    if not web_dir.exists():
        print("❌ web/ directory not found")
        return False

    os.chdir(web_dir)

    try:
        # Install dependencies
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Frontend dependencies installed")
        else:
            print(f"❌ Failed to install frontend dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing frontend dependencies: {e}")
        return False

    os.chdir('..')
    return True

def build_frontend():
    """Build the frontend for production"""
    print("🔨 Building frontend...")

    web_dir = Path('web')
    os.chdir(web_dir)

    try:
        # Build for production
        result = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Frontend built successfully")
        else:
            print(f"❌ Failed to build frontend: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error building frontend: {e}")
        return False

    os.chdir('..')
    return True

def start_flask_server():
    """Start the Flask server"""
    print("🚀 Starting Flask server...")

    try:
        # Import and start the Flask app
        from web_app import app

        print("📱 Web UI will be available at: http://localhost:5000")
        print("🔧 API will be available at: http://localhost:5000/api/")
        print("⏹️  Press Ctrl+C to stop the server")
        print()

        app.run(debug=False, host='0.0.0.0', port=5000)

    except Exception as e:
        print(f"❌ Failed to start Flask server: {e}")
        return False

    return True

def main():
    """Main startup function"""
    print("🎵 YouTube Audio Extractor Web App")
    print("=" * 50)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Install frontend dependencies if needed
    if not install_frontend_dependencies():
        sys.exit(1)

    # Build frontend
    if not build_frontend():
        sys.exit(1)

    # Start Flask server
    if not start_flask_server():
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
