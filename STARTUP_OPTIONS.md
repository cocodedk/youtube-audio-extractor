# 🚀 YouTube Audio Extractor - Startup Options

This document explains the different ways to start the YouTube Audio Extractor application.

## 🎯 **Quick Start (Recommended)**

Use the new smart startup script that gives you choices:

```bash
./start_ui.sh
```

This script will:
- ✅ Check and update dependencies automatically
- ✅ Give you a choice between development and production modes
- ✅ Handle port conflicts gracefully
- ✅ Ensure yt-dlp is up to date for YouTube compatibility

## 🔧 **Development Mode (Recommended for Development)**

**Features:**
- Hot reload for frontend changes
- Debug mode enabled
- Real-time progress tracking
- Separate frontend and backend servers

**How to start:**
```bash
# Option 1: Use the smart startup script
./start_ui.sh
# Choose option 1 (Development Mode)

# Option 2: Direct command
python3 dev_server.py
```

**URLs:**
- Frontend: http://localhost:3000 (Webpack dev server)
- Backend: http://localhost:5000 (Flask API)

## 🚀 **Production Mode**

**Features:**
- Optimized frontend build
- Single server deployment
- Production-ready configuration

**How to start:**
```bash
# Option 1: Use the smart startup script
./start_ui.sh
# Choose option 2 (Production Mode)

# Option 2: Direct command
./start_server.sh
```

**URLs:**
- Application: http://localhost:5000 (served by Flask)

## ⚠️ **Important Notes**

### **yt-dlp Version Management**

The application automatically manages yt-dlp versions:

- **Requirements.txt**: Uses `yt-dlp>=2025.8.0` (minimum version)
- **Auto-update**: Scripts automatically upgrade yt-dlp for YouTube compatibility
- **Version check**: Warns if yt-dlp is outdated

### **Port Conflicts**

The startup scripts check for port conflicts:
- Port 3000: Webpack dev server (development mode)
- Port 5000: Flask backend (both modes)

If ports are in use, the scripts will inform you to stop existing servers first.

## 🛠️ **Manual Startup (Advanced Users)**

### **Frontend Only (Webpack Dev Server)**
```bash
cd web
npm run dev
```

### **Backend Only (Flask)**
```bash
python3 web_app.py
```

### **Production Build**
```bash
cd web
npm run build
cd ..
python3 start_web_app.py
```

## 🔍 **Troubleshooting**

### **"Download Failed" Errors**

If you get download failures:

1. **Check yt-dlp version:**
   ```bash
   source venv/bin/activate
   pip show yt-dlp
   ```

2. **Update yt-dlp manually:**
   ```bash
   source venv/bin/activate
   pip install --upgrade yt-dlp
   ```

3. **Restart the application** after updating

### **Port Already in Use**

If you get port conflicts:

1. **Find processes using the port:**
   ```bash
   lsof -i :5000  # For Flask
   lsof -i :3000  # For Webpack
   ```

2. **Stop the conflicting process:**
   ```bash
   kill <PID>
   ```

3. **Restart the application**

### **Dependencies Issues**

If you have dependency problems:

1. **Recreate virtual environment:**
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Use the smart startup script:**
   ```bash
   ./start_ui.sh
   ```

## 📋 **Summary**

| Startup Method | Use Case | Frontend | Backend | Features |
|----------------|----------|----------|---------|----------|
| `./start_ui.sh` | **Recommended** | Choice | Choice | Smart, auto-updates |
| `python3 dev_server.py` | Development | localhost:3000 | localhost:5000 | Hot reload, debug |
| `./start_server.sh` | Production | localhost:5000 | localhost:5000 | Optimized, single server |

**For most users, just run `./start_ui.sh` and choose your preferred mode!** 🎉
