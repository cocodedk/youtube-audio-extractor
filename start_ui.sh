#!/bin/bash

# YouTube Audio Extractor - Smart Startup Script
# This script gives you a choice between development and production modes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}🎵 YouTube Audio Extractor - Smart Startup${NC}"
    echo "============================================="
}

print_choice() {
    echo -e "${YELLOW}Choose your startup mode:${NC}"
    echo "1) Development Mode (with hot reload)"
    echo "   - Frontend: http://localhost:3000 (Webpack dev server)"
    echo "   - Backend:  http://localhost:5000 (Flask with debug)"
    echo "   - Features: Hot reload, debug mode, real-time updates"
    echo ""
    echo "2) Production Mode (optimized)"
    echo "   - Frontend: http://localhost:5000 (served by Flask)"
    echo "   - Backend:  http://localhost:5000 (Flask production)"
    echo "   - Features: Optimized build, production ready"
    echo ""
    echo "3) Exit"
    echo ""
}

check_dependencies() {
    echo -e "${BLUE}🔍 Checking dependencies...${NC}"

    # Check if virtual environment exists
    if [[ ! -d "venv" ]]; then
        echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
        python3 -m venv venv
    fi

    # Activate virtual environment
    source venv/bin/activate

    # Check yt-dlp version
    if command -v pip &> /dev/null; then
        YTDLP_VERSION=$(pip show yt-dlp 2>/dev/null | grep Version | cut -d' ' -f2 || echo "not_installed")
        if [[ "$YTDLP_VERSION" == "not_installed" ]]; then
            echo -e "${YELLOW}📦 Installing dependencies...${NC}"
            pip install -r requirements.txt
        elif [[ "$YTDLP_VERSION" < "2025.0.0" ]]; then
            echo -e "${YELLOW}⚠️  yt-dlp version $YTDLP_VERSION may be outdated${NC}"
            echo -e "${BLUE}💡 Updating yt-dlp for better YouTube compatibility...${NC}"
            pip install --upgrade yt-dlp
        else
            echo -e "${GREEN}✅ yt-dlp $YTDLP_VERSION is up to date${NC}"
        fi
    fi

    echo -e "${GREEN}✅ Dependencies check complete${NC}"
}

start_development() {
    echo -e "${GREEN}🚀 Starting Development Mode...${NC}"
    echo -e "${BLUE}💡 This will start both Webpack dev server and Flask backend${NC}"

    # Check if ports are available
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port 3000 is already in use${NC}"
        echo "Attempting to stop existing processes on port 3000..."

        # Kill processes on port 3000
        PIDS=$(lsof -Pi :3000 -sTCP:LISTEN -t 2>/dev/null || true)
        if [[ -n "$PIDS" ]]; then
            echo "Stopping processes: $PIDS"
            kill $PIDS 2>/dev/null || true
            sleep 2

            # Check if still running
            if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
                echo -e "${RED}❌ Failed to stop processes on port 3000${NC}"
                echo "Please manually stop them and try again"
                return 1
            else
                echo -e "${GREEN}✅ Port 3000 is now available${NC}"
            fi
        fi
    fi

    if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port 5000 is already in use${NC}"
        echo "Attempting to stop existing processes on port 5000..."

        # Kill processes on port 5000
        PIDS=$(lsof -Pi :5000 -sTCP:LISTEN -t 2>/dev/null || true)
        if [[ -n "$PIDS" ]]; then
            echo "Stopping processes: $PIDS"
            kill $PIDS 2>/dev/null || true
            sleep 2

            # Check if still running
            if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
                echo -e "${RED}❌ Failed to stop processes on port 5000${NC}"
                echo "Please manually stop them and try again"
                return 1
            else
                echo -e "${GREEN}✅ Port 5000 is now available${NC}"
            fi
        fi
    fi

    # Activate virtual environment and start development servers
    source venv/bin/activate
    python3 dev_server.py
}

start_production() {
    echo -e "${GREEN}🚀 Starting Production Mode...${NC}"
    echo -e "${BLUE}💡 This will build the frontend and start Flask in production mode${NC}"

    # Check if port 5000 is available
    if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}❌ Port 5000 is already in use${NC}"
        echo "Please stop any existing servers first"
        return 1
    fi

    # Build frontend
    echo -e "${BLUE}🔨 Building frontend...${NC}"
    cd web
    npm run build
    cd ..

    # Activate virtual environment and start production server
    echo -e "${BLUE}🚀 Starting production server...${NC}"
    source venv/bin/activate
    python3 start_web_app.py
}

main() {
    print_header

    # Check dependencies first
    check_dependencies

    while true; do
        print_choice
        read -p "Enter your choice (1-3): " choice

        case $choice in
            1)
                start_development
                break
                ;;
            2)
                start_production
                break
                ;;
            3)
                echo -e "${GREEN}👋 Goodbye!${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Invalid choice. Please enter 1, 2, or 3.${NC}"
                ;;
        esac
    done
}

# Run main function
main
