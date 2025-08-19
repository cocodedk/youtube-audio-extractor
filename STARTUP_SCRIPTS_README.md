# 🚀 YouTube Audio Extractor - Startup Scripts

This directory contains cross-platform startup scripts that automatically set up the environment, install dependencies, and start the web server for the YouTube Audio Extractor.

## 📁 Available Scripts

### 🐧 Linux/macOS: `start_server.sh`
- **Usage**: `./start_server.sh [OPTIONS]`
- **Requirements**: Bash shell, Python 3.7+, Node.js, npm
- **Features**: Full automation with colored output, error handling, and command-line options

### 🪟 Windows Batch: `start_server.bat`
- **Usage**: `start_server.bat [OPTIONS]`
- **Requirements**: Windows Command Prompt, Python 3.7+, Node.js, npm
- **Features**: Windows-compatible batch script with colored output

### 🪟 Windows PowerShell: `start_server.ps1`
- **Usage**: `.\start_server.ps1 [OPTIONS]`
- **Requirements**: Windows PowerShell 5.0+, Python 3.7+, Node.js, npm
- **Features**: Modern PowerShell script with better error handling and features

## 🎯 What These Scripts Do

The startup scripts automatically perform the following tasks:

1. **🔍 System Check**: Verify Python 3.7+, Node.js, and npm are installed
2. **🐍 Python Setup**: Create virtual environment and install Python dependencies
3. **📦 Node.js Setup**: Install frontend dependencies from `package.json`
4. **🔨 Frontend Build**: Build the TypeScript/React frontend for production
5. **🚀 Server Start**: Launch the Flask web server on `http://localhost:5000`

## 🌐 Port Configuration

### Production Mode (start_server.* scripts)
- **Web UI + API**: Both served on port 5000
- **URL**: http://localhost:5000
- **API Endpoints**: http://localhost:5000/api/*

### Development Mode (dev_server.py)
- **Web UI**: Port 3000 (Webpack dev server with hot reload)
- **API**: Port 5000 (Flask backend)
- **Web UI URL**: http://localhost:3000
- **API Endpoints**: http://localhost:5000/api/*
- **Features**: Hot reload, live updates, development tools

## 🚀 Quick Start

### Linux/macOS
```bash
# Make script executable (first time only)
chmod +x start_server.sh

# Run the script
./start_server.sh
```

### Windows Command Prompt
```cmd
# Run the batch script
start_server.bat
```

### Windows PowerShell
```powershell
# Run the PowerShell script
.\start_server.ps1
```

## ⚙️ Command Line Options

All scripts support the following options:

| Option | Long Form | Description |
|--------|-----------|-------------|
| `-h` | `--help` | Show help message and exit |
| `-s` | `--setup` | Only setup dependencies (don't start server) |
| `-c` | `--clean` | Clean build artifacts and reinstall everything |
| `-v` | `--verbose` | Enable verbose output (Linux/macOS only) |

### Examples

```bash
# Setup only (don't start server)
./start_server.sh --setup

# Clean build and reinstall
./start_server.sh --clean

# Show help
./start_server.sh --help
```

## 🔧 Prerequisites

Before running the scripts, ensure you have:

### Required Software
- **Python 3.7+**: Download from [python.org](https://python.org)
- **Node.js 16+**: Download from [nodejs.org](https://nodejs.org)
- **npm**: Usually comes with Node.js

### System Requirements
- **Linux**: Any modern distribution with bash
- **macOS**: 10.14+ (Mojave) or later
- **Windows**: Windows 10+ or Windows Server 2016+

## 📋 What Gets Installed

### Python Dependencies
- Flask web framework
- yt-dlp for YouTube video processing
- Other packages from `requirements.txt`

### Node.js Dependencies
- TypeScript compiler
- Webpack bundler
- Tailwind CSS
- Other build tools from `web/package.json`

## 🏗️ Project Structure After Setup

```
yt-audio-extractor/
├── venv/                    # Python virtual environment
├── web/
│   ├── node_modules/        # Node.js dependencies
│   ├── dist/               # Built frontend files
│   └── package-lock.json   # Locked dependency versions
├── start_server.sh          # Linux/macOS script
├── start_server.bat         # Windows batch script
├── start_server.ps1         # Windows PowerShell script
└── ...                     # Other project files
```

## 🚨 Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Install Python 3.7+ from python.org
# On Ubuntu/Debian:
sudo apt update && sudo apt install python3 python3-venv python3-pip

# On macOS with Homebrew:
brew install python3

# On Windows: Download installer from python.org
```

#### Node.js Not Found
```bash
# Install Node.js from nodejs.org
# On Ubuntu/Debian:
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# On macOS with Homebrew:
brew install node

# On Windows: Download installer from nodejs.org
```

#### Permission Denied (Linux/macOS)
```bash
# Make script executable
chmod +x start_server.sh

# Or run with bash explicitly
bash start_server.sh
```

#### PowerShell Execution Policy (Windows)
```powershell
# Allow script execution (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run with bypass
PowerShell -ExecutionPolicy Bypass -File start_server.ps1
```

### Clean Build
If you encounter issues, try a clean build:

```bash
# Linux/macOS
./start_server.sh --clean

# Windows
start_server.bat --clean
# or
.\start_server.ps1 -Clean
```

## 🔄 Development Workflow

### First Time Setup
1. Clone the repository
2. Run the startup script: `./start_server.sh` (or equivalent)
3. Wait for all dependencies to install
4. Access the web UI at `http://localhost:5000`

### Subsequent Runs
- The script will detect existing installations and skip redundant steps
- Only new/updated dependencies will be installed
- The frontend will be rebuilt automatically

### Development Mode
For development with hot reload and live updates, use:
- **`dev_server.py`** - Development server (Web UI on port 3000, API on port 5000)
- **`web/` directory** - Frontend development with webpack
- **Hot Reload**: Frontend automatically updates when you change code
- **Separate Ports**: Web UI (3000) and API (5000) run independently

## 📝 Script Features

### Error Handling
- Comprehensive error checking at each step
- Clear error messages with suggested solutions
- Graceful failure with proper exit codes

### Progress Feedback
- Colored output for different message types
- Step-by-step progress indication
- Success/failure status for each operation

### Cross-Platform Compatibility
- Automatic OS detection (Linux/macOS script)
- Platform-specific path handling
- Consistent behavior across operating systems

## 🤝 Contributing

When modifying the startup scripts:

1. **Test on all platforms** before committing
2. **Maintain backward compatibility** with existing setups
3. **Update this README** if adding new features
4. **Follow the existing code style** and structure

## 📄 License

These scripts are part of the YouTube Audio Extractor project and are licensed under the same terms as the main project.

---

**Need help?** Check the main [README.md](../README.md) or open an issue on GitHub.
