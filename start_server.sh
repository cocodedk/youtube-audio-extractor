#!/bin/bash

# YouTube Audio Extractor - Cross-platform startup script
# This script sets up the environment and starts the web server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# Function to install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."

    if [[ ! -f "requirements.txt" ]]; then
        print_error "requirements.txt not found!"
        return 1
    fi

    # Check if virtual environment exists
    if [[ ! -d "venv" ]]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi

    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate

    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip

    # Install requirements
    print_status "Installing Python packages..."
    pip install -r requirements.txt

    # Ensure yt-dlp is up to date for YouTube compatibility
    print_status "Ensuring yt-dlp is up to date for YouTube compatibility..."
    pip install --upgrade yt-dlp

    print_success "Python dependencies installed successfully!"
}

# Function to install Node.js dependencies
install_node_deps() {
    print_status "Installing Node.js dependencies..."

    if [[ ! -d "web" ]]; then
        print_error "web/ directory not found!"
        return 1
    fi

    cd web

    # Check if node_modules exists
    if [[ ! -d "node_modules" ]]; then
        print_status "Installing npm packages..."
        npm install
    else
        print_status "Updating npm packages..."
        npm install
    fi

    cd ..
    print_success "Node.js dependencies installed successfully!"
}

# Function to build frontend
build_frontend() {
    print_status "Building frontend..."

    cd web

    # Build for production
    print_status "Running production build..."
    npm run build

    cd ..
    print_success "Frontend built successfully!"
}

# Function to start the server
start_server() {
    print_status "Starting web server..."

    # Activate virtual environment
    source venv/bin/activate

    # Start the Flask server
    print_success "Starting YouTube Audio Extractor Web App..."
    print_status "Web UI will be available at: http://localhost:5000"
    print_status "API will be available at: http://localhost:5000/api/"
    print_status "💡 Note: This is production mode. For development with hot reload, use dev_server.py"
    print_status "Press Ctrl+C to stop the server"
    echo

    python3 start_web_app.py
}

# Function to check system requirements
check_requirements() {
    print_status "Checking system requirements..."

    # Check Python
    if ! command_exists python3; then
        print_error "Python 3 is not installed!"
        print_status "Please install Python 3.7+ from https://python.org"
        return 1
    fi

    # Check Python version
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    print_success "Python $PYTHON_VERSION found"

    # Check Node.js
    if ! command_exists node; then
        print_error "Node.js is not installed!"
        print_status "Please install Node.js from https://nodejs.org"
        return 1
    fi

    NODE_VERSION=$(node --version)
    print_success "Node.js $NODE_VERSION found"

    # Check npm
    if ! command_exists npm; then
        print_error "npm is not installed!"
        print_status "Please install npm (usually comes with Node.js)"
        return 1
    fi

    NPM_VERSION=$(npm --version)
    print_success "npm $NPM_VERSION found"

    print_success "All system requirements met!"
}

# Function to show help
show_help() {
    echo "YouTube Audio Extractor - Startup Script"
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -s, --setup    Only setup dependencies (don't start server)"
    echo "  -c, --clean    Clean build artifacts and reinstall"
    echo "  -v, --verbose  Verbose output"
    echo
    echo "Examples:"
    echo "  $0              # Setup and start server"
    echo "  $0 --setup      # Only setup dependencies"
    echo "  $0 --clean      # Clean and reinstall everything"
}

# Main function
main() {
    local SETUP_ONLY=false
    local CLEAN_BUILD=false
    local VERBOSE=false

    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -s|--setup)
                SETUP_ONLY=true
                shift
                ;;
            -c|--clean)
                CLEAN_BUILD=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done

    # Set verbose mode
    if [[ "$VERBOSE" == true ]]; then
        set -x
    fi

    echo "🎵 YouTube Audio Extractor - Startup Script"
    echo "============================================="
    echo "OS: $(detect_os)"
    echo "Python: $(python3 --version 2>/dev/null || echo 'Not found')"
    echo "Node.js: $(node --version 2>/dev/null || echo 'Not found')"
    echo "============================================="
    echo

    # Check system requirements
    if ! check_requirements; then
        exit 1
    fi

    # Clean build if requested
    if [[ "$CLEAN_BUILD" == true ]]; then
        print_status "Cleaning build artifacts..."
        rm -rf venv
        rm -rf web/node_modules
        rm -rf web/dist
        print_success "Clean build completed!"
    fi

    # Install Python dependencies
    if ! install_python_deps; then
        exit 1
    fi

    # Install Node.js dependencies
    if ! install_node_deps; then
        exit 1
    fi

    # Build frontend
    if ! build_frontend; then
        exit 1
    fi

    print_success "Setup completed successfully!"

    # Start server unless setup-only mode
    if [[ "$SETUP_ONLY" == false ]]; then
        start_server
    else
        print_status "Setup completed. Run '$0' to start the server."
    fi
}

# Trap Ctrl+C
trap 'echo -e "\n${YELLOW}[WARNING]${NC} Interrupted by user"; exit 1' INT

# Run main function
main "$@"
