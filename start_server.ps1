# YouTube Audio Extractor - Windows PowerShell startup script
# This script sets up the environment and starts the web server

param(
    [switch]$Help,
    [switch]$Setup,
    [switch]$Clean,
    [switch]$Verbose
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"
$White = "White"

# Function to print colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

# Function to check if command exists
function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Function to install Python dependencies
function Install-PythonDependencies {
    Write-Status "Installing Python dependencies..."

    if (-not (Test-Path "requirements.txt")) {
        Write-Error "requirements.txt not found!"
        return $false
    }

    # Check if virtual environment exists
    if (-not (Test-Path "venv")) {
        Write-Status "Creating virtual environment..."
        python -m venv venv
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to create virtual environment!"
            return $false
        }
    }

    # Activate virtual environment
    Write-Status "Activating virtual environment..."
    & "venv\Scripts\Activate.ps1"

    # Upgrade pip
    Write-Status "Upgrading pip..."
    python -m pip install --upgrade pip

    # Install requirements
    Write-Status "Installing Python packages..."
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install Python packages!"
        return $false
    }

    Write-Success "Python dependencies installed successfully!"
    return $true
}

# Function to install Node.js dependencies
function Install-NodeDependencies {
    Write-Status "Installing Node.js dependencies..."

    if (-not (Test-Path "web")) {
        Write-Error "web/ directory not found!"
        return $false
    }

    Push-Location "web"

    try {
        # Check if node_modules exists
        if (-not (Test-Path "node_modules")) {
            Write-Status "Installing npm packages..."
            npm install
        } else {
            Write-Status "Updating npm packages..."
            npm install
        }

        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to install Node.js dependencies!"
            return $false
        }

        Write-Success "Node.js dependencies installed successfully!"
        return $true
    } finally {
        Pop-Location
    }
}

# Function to build frontend
function Build-Frontend {
    Write-Status "Building frontend..."

    Push-Location "web"

    try {
        # Build for production
        Write-Status "Running production build..."
        npm run build

        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to build frontend!"
            return $false
        }

        Write-Success "Frontend built successfully!"
        return $true
    } finally {
        Pop-Location
    }
}

# Function to start the server
function Start-WebServer {
    Write-Status "Starting web server..."

    # Activate virtual environment
    & "venv\Scripts\Activate.ps1"

    # Start the Flask server
    Write-Success "Starting YouTube Audio Extractor Web App..."
    Write-Status "Web UI will be available at: http://localhost:5000"
    Write-Status "API will be available at: http://localhost:5000/api/"
    Write-Status "💡 Note: This is production mode. For development with hot reload, use dev_server.py"
    Write-Status "Press Ctrl+C to stop the server"
    Write-Host ""

    python start_web_app.py
}

# Function to check system requirements
function Test-SystemRequirements {
    Write-Status "Checking system requirements..."

    # Check Python
    if (-not (Test-Command "python")) {
        Write-Error "Python is not installed!"
        Write-Status "Please install Python 3.7+ from https://python.org"
        return $false
    }

    # Check Python version
    try {
        $pythonVersion = python --version 2>&1
        Write-Success "Python $pythonVersion found"
    } catch {
        Write-Error "Failed to get Python version"
        return $false
    }

    # Check Node.js
    if (-not (Test-Command "node")) {
        Write-Error "Node.js is not installed!"
        Write-Status "Please install Node.js from https://nodejs.org"
        return $false
    }

    try {
        $nodeVersion = node --version
        Write-Success "Node.js $nodeVersion found"
    } catch {
        Write-Error "Failed to get Node.js version"
        return $false
    }

    # Check npm
    if (-not (Test-Command "npm")) {
        Write-Error "npm is not installed!"
        Write-Status "Please install npm (usually comes with Node.js)"
        return $false
    }

    try {
        $npmVersion = npm --version
        Write-Success "npm $npmVersion found"
    } catch {
        Write-Error "Failed to get npm version"
        return $false
    }

    Write-Success "All system requirements met!"
    return $true
}

# Function to show help
function Show-Help {
    Write-Host "YouTube Audio Extractor - Startup Script" -ForegroundColor $White
    Write-Host "Usage: $($MyInvocation.MyCommand.Name) [OPTIONS]" -ForegroundColor $White
    Write-Host ""
    Write-Host "Options:" -ForegroundColor $White
    Write-Host "  -Help, -h     Show this help message" -ForegroundColor $White
    Write-Host "  -Setup, -s    Only setup dependencies (don't start server)" -ForegroundColor $White
    Write-Host "  -Clean, -c    Clean build artifacts and reinstall" -ForegroundColor $White
    Write-Host "  -Verbose, -v  Verbose output" -ForegroundColor $White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor $White
    Write-Host "  $($MyInvocation.MyCommand.Name)              # Setup and start server" -ForegroundColor $White
    Write-Host "  $($MyInvocation.MyCommand.Name) -Setup       # Only setup dependencies" -ForegroundColor $White
    Write-Host "  $($MyInvocation.MyCommand.Name) -Clean       # Clean and reinstall everything" -ForegroundColor $White
}

# Function to clean build artifacts
function Clear-BuildArtifacts {
    Write-Status "Cleaning build artifacts..."

    if (Test-Path "venv") {
        Remove-Item -Recurse -Force "venv"
    }

    if (Test-Path "web\node_modules") {
        Remove-Item -Recurse -Force "web\node_modules"
    }

    if (Test-Path "web\dist") {
        Remove-Item -Recurse -Force "web\dist"
    }

    Write-Success "Clean build completed!"
}

# Main function
function Main {
    Write-Host "🎵 YouTube Audio Extractor - Startup Script" -ForegroundColor $White
    Write-Host "=============================================" -ForegroundColor $White
    Write-Host "OS: Windows (PowerShell)" -ForegroundColor $White

    try {
        $pythonVersion = python --version 2>&1
        Write-Host "Python: $pythonVersion" -ForegroundColor $White
    } catch {
        Write-Host "Python: Not found" -ForegroundColor $Red
    }

    try {
        $nodeVersion = node --version
        Write-Host "Node.js: $nodeVersion" -ForegroundColor $White
    } catch {
        Write-Host "Node.js: Not found" -ForegroundColor $Red
    }

    Write-Host "=============================================" -ForegroundColor $White
    Write-Host ""

    # Check system requirements
    if (-not (Test-SystemRequirements)) {
        exit 1
    }

    # Clean build if requested
    if ($Clean) {
        Clear-BuildArtifacts
    }

    # Install Python dependencies
    if (-not (Install-PythonDependencies)) {
        exit 1
    }

    # Install Node.js dependencies
    if (-not (Install-NodeDependencies)) {
        exit 1
    }

    # Build frontend
    if (-not (Build-Frontend)) {
        exit 1
    }

    Write-Success "Setup completed successfully!"

    # Start server unless setup-only mode
    if (-not $Setup) {
        Start-WebServer
    } else {
        Write-Status "Setup completed. Run '$($MyInvocation.MyCommand.Name)' to start the server."
    }
}

# Show help if requested
if ($Help) {
    Show-Help
    exit 0
}

# Set verbose mode
if ($Verbose) {
    $VerbosePreference = "Continue"
}

# Run main function
try {
    Main
} catch {
    Write-Error "Unexpected error: $($_.Exception.Message)"
    if ($Verbose) {
        Write-Error $_.ScriptStackTrace
    }
    exit 1
}
