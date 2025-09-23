#!/usr/bin/env python3
"""
Development server for YouTube Audio Extractor Web App
Runs both Flask backend and Webpack dev server
"""

import os
import subprocess
import sys
import time
import threading
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

    # Check yt-dlp version and update if needed
    try:
        import yt_dlp
        current_version = yt_dlp.version.__version__
        print(f"✅ yt-dlp {current_version} OK")

        # Check if yt-dlp is recent enough for YouTube compatibility
        if current_version < "2025.0.0":
            print("⚠️  yt-dlp version may be outdated for YouTube compatibility")
            print("💡 Consider updating with: pip install --upgrade yt-dlp")
    except ImportError as e:
        print(f"❌ Missing yt-dlp: {e}")
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
    """Install frontend dependencies if needed"""
    web_dir = Path('web')
    if not web_dir.exists():
        print("❌ web/ directory not found")
        return False

    # Check if node_modules exists
    if not (web_dir / 'node_modules').exists():
        print("📦 Installing frontend dependencies...")
        os.chdir(web_dir)

        try:
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
    else:
        print("✅ Frontend dependencies already installed")

    return True

def start_webpack_dev_server():
    """Start Webpack dev server in background"""
    print("🌐 Starting Webpack dev server...")

    web_dir = Path('web')
    os.chdir(web_dir)

    try:
        # Start Webpack dev server
        process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Wait a bit for server to start
        time.sleep(3)

        if process.poll() is None:
            print("✅ Webpack dev server started on http://localhost:3000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Webpack dev server failed to start: {stderr}")
            return None

    except Exception as e:
        print(f"❌ Error starting Webpack dev server: {e}")
        return None
    finally:
        os.chdir('..')

def start_flask_server():
    """Start Flask server"""
    print("🚀 Starting Flask server...")

    try:
        # Import and start the Flask app
        from web_app import app

        print("📱 Web UI will be available at: http://localhost:3000")
        print("🔧 API will be available at: http://localhost:5000/api/")
        print("⏹️  Press Ctrl+C to stop both servers")
        print()

        # Suppress Flask's development server warning
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

    except Exception as e:
        print(f"❌ Failed to start Flask server: {e}")
        return False

    return True

def main():
    """Main development function"""
    print("🎵 YouTube Audio Extractor - Development Mode")
    print("=" * 50)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Install frontend dependencies if needed
    if not install_frontend_dependencies():
        sys.exit(1)

    # Start Webpack dev server
    webpack_process = start_webpack_dev_server()
    if not webpack_process:
        sys.exit(1)

    try:
        # Start Flask server in main thread
        start_flask_server()
    except KeyboardInterrupt:
        print("\n👋 Stopping development servers...")
    finally:
        # Clean up Webpack process
        if webpack_process:
            print("🛑 Stopping Webpack dev server...")
            webpack_process.terminate()
            webpack_process.wait()
            print("✅ Webpack dev server stopped")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Development servers stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
