@echo off
REM YouTube Audio Extractor - Windows startup script
REM This script sets up the environment and starts the web server

setlocal enabledelayedexpansion

REM Set title
title YouTube Audio Extractor - Startup Script

REM Colors for output (Windows 10+)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM Function to print colored output
:print_status
echo %BLUE%[INFO]%NC% %~1
goto :eof

:print_success
echo %GREEN%[SUCCESS]%NC% %~1
goto :eof

:print_warning
echo %YELLOW%[WARNING]%NC% %~1
goto :eof

:print_error
echo %RED%[ERROR]%NC% %~1
goto :eof

REM Function to check if command exists
:command_exists
where %1 >nul 2>&1
if %errorlevel% equ 0 (
    set "EXISTS=true"
) else (
    set "EXISTS=false"
)
goto :eof

REM Function to install Python dependencies
:install_python_deps
call :print_status "Installing Python dependencies..."
if not exist "requirements.txt" (
    call :print_error "requirements.txt not found!"
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    call :print_status "Creating virtual environment..."
    python -m venv venv
    if !errorlevel! neq 0 (
        call :print_error "Failed to create virtual environment!"
        exit /b 1
    )
)

REM Activate virtual environment
call :print_status "Activating virtual environment..."
call venv\Scripts\activate.bat

REM Upgrade pip
call :print_status "Upgrading pip..."
python -m pip install --upgrade pip

REM Install requirements
call :print_status "Installing Python packages..."
pip install -r requirements.txt
if !errorlevel! neq 0 (
    call :print_error "Failed to install Python packages!"
    exit /b 1
)

call :print_success "Python dependencies installed successfully!"
exit /b 0

REM Function to install Node.js dependencies
:install_node_deps
call :print_status "Installing Node.js dependencies..."
if not exist "web" (
    call :print_error "web/ directory not found!"
    exit /b 1
)

cd web

REM Check if node_modules exists
if not exist "node_modules" (
    call :print_status "Installing npm packages..."
    npm install
) else (
    call :print_status "Updating npm packages..."
    npm install
)

if !errorlevel! neq 0 (
    call :print_error "Failed to install Node.js dependencies!"
    cd ..
    exit /b 1
)

cd ..
call :print_success "Node.js dependencies installed successfully!"
exit /b 0

REM Function to build frontend
:build_frontend
call :print_status "Building frontend..."
cd web

REM Build for production
call :print_status "Running production build..."
npm run build
if !errorlevel! neq 0 (
    call :print_error "Failed to build frontend!"
    cd ..
    exit /b 1
)

cd ..
call :print_success "Frontend built successfully!"
exit /b 0

REM Function to start the server
:start_server
call :print_status "Starting web server..."

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the Flask server
call :print_success "Starting YouTube Audio Extractor Web App..."
call :print_status "Web UI will be available at: http://localhost:5000"
call :print_status "API will be available at: http://localhost:5000/api/"
call :print_status "💡 Note: This is production mode. For development with hot reload, use dev_server.py"
call :print_status "Press Ctrl+C to stop the server"
echo.

python start_web_app.py
exit /b 0

REM Function to check system requirements
:check_requirements
call :print_status "Checking system requirements..."

REM Check Python
call :command_exists python
if "%EXISTS%"=="false" (
    call :print_error "Python is not installed!"
    call :print_status "Please install Python 3.7+ from https://python.org"
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
call :print_success "Python %PYTHON_VERSION% found"

REM Check Node.js
call :command_exists node
if "%EXISTS%"=="false" (
    call :print_error "Node.js is not installed!"
    call :print_status "Please install Node.js from https://nodejs.org"
    exit /b 1
)

for /f "tokens=1" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
call :print_success "Node.js %NODE_VERSION% found"

REM Check npm
call :command_exists npm
if "%EXISTS%"=="false" (
    call :print_error "npm is not installed!"
    call :print_status "Please install npm (usually comes with Node.js)"
    exit /b 1
)

for /f "tokens=1" %%i in ('npm --version 2^>^&1') do set NPM_VERSION=%%i
call :print_success "npm %NPM_VERSION% found"

call :print_success "All system requirements met!"
exit /b 0

REM Function to show help
:show_help
echo YouTube Audio Extractor - Startup Script
echo Usage: %~nx0 [OPTIONS]
echo.
echo Options:
echo   -h, --help     Show this help message
echo   -s, --setup    Only setup dependencies (don't start server)
echo   -c, --clean    Clean build artifacts and reinstall
echo.
echo Examples:
echo   %~nx0              # Setup and start server
echo   %~nx0 --setup      # Only setup dependencies
echo   %~nx0 --clean      # Clean and reinstall everything
goto :eof

REM Main function
:main
set "SETUP_ONLY=false"
set "CLEAN_BUILD=false"

REM Parse command line arguments
:parse_args
if "%~1"=="" goto :end_parse
if "%~1"=="-h" goto :show_help
if "%~1"=="--help" goto :show_help
if "%~1"=="-s" goto :set_setup
if "%~1"=="--setup" goto :set_setup
if "%~1"=="-c" goto :set_clean
if "%~1"=="--clean" goto :set_clean
shift
goto :parse_args

:set_setup
set "SETUP_ONLY=true"
shift
goto :parse_args

:set_clean
set "CLEAN_BUILD=true"
shift
goto :parse_args

:end_parse

echo 🎵 YouTube Audio Extractor - Startup Script
echo =============================================
echo OS: Windows
for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo Python: %%i
for /f "tokens=1" %%i in ('node --version 2^>^&1') do echo Node.js: %%i
echo =============================================
echo.

REM Check system requirements
call :check_requirements
if !errorlevel! neq 0 exit /b 1

REM Clean build if requested
if "%CLEAN_BUILD%"=="true" (
    call :print_status "Cleaning build artifacts..."
    if exist "venv" rmdir /s /q "venv"
    if exist "web\node_modules" rmdir /s /q "web\node_modules"
    if exist "web\dist" rmdir /s /q "web\dist"
    call :print_success "Clean build completed!"
)

REM Install Python dependencies
call :install_python_deps
if !errorlevel! neq 0 exit /b 1

REM Install Node.js dependencies
call :install_node_deps
if !errorlevel! neq 0 exit /b 1

REM Build frontend
call :build_frontend
if !errorlevel! neq 0 exit /b 1

call :print_success "Setup completed successfully!"

REM Start server unless setup-only mode
if "%SETUP_ONLY%"=="false" (
    call :start_server
) else (
    call :print_status "Setup completed. Run '%~nx0' to start the server."
)

exit /b 0

REM Show help if no arguments or help requested
if "%~1"=="" goto :show_help
if "%~1"=="-h" goto :show_help
if "%~1"=="--help" goto :show_help

REM Run main function
call :main %*
if !errorlevel! neq 0 (
    echo.
    call :print_error "Script failed with error code !errorlevel!"
    pause
    exit /b !errorlevel!
)
