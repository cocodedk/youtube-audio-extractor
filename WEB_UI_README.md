# 🎵 YouTube Audio Extractor - Web UI

A beautiful, modern web interface for the YouTube Audio Extractor, built with **TypeScript**, **Tailwind CSS**, and **Webpack**. This provides a user-friendly alternative to the command-line interface.

## ✨ Features

- **🎨 Modern UI**: Clean, responsive design with Tailwind CSS
- **📱 Mobile First**: Works perfectly on all device sizes
- **⚡ Real-time Updates**: Live status messages and progress tracking
- **🔧 TypeScript**: Full type safety and modern JavaScript features
- **📦 Component-based**: Modular architecture for easy maintenance
- **🚀 Hot Reloading**: Instant updates during development

## 🚀 Quick Start

### Option 1: Production Mode (Recommended for users)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the web application
python start_web_app.py
```

Then open your browser to: **http://localhost:5000**

### Option 2: Development Mode (For developers)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start development servers (both Flask + Webpack)
python dev_server.py
```

Then open your browser to: **http://localhost:3000**

## 📋 Prerequisites

### Required Software

- **Python 3.7+** with pip
- **Node.js 16+** and npm
- **FFmpeg** (for audio processing)

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [FFmpeg official website](https://ffmpeg.org/download.html)

## 🛠️ Installation

### 1. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd web
npm install
cd ..
```

## 🎯 Usage

### Starting the Application

#### Production Mode
```bash
python start_web_app.py
```

This will:
- ✅ Check all dependencies
- 📦 Install frontend packages if needed
- 🔨 Build the frontend for production
- 🚀 Start Flask server on port 5000

#### Development Mode
```bash
python dev_server.py
```

This will:
- ✅ Check all dependencies
- 📦 Install frontend packages if needed
- 🌐 Start Webpack dev server on port 3000
- 🚀 Start Flask server on port 5000
- 🔄 Enable hot reloading for development

### Accessing the Application

- **Production**: http://localhost:5000
- **Development**: http://localhost:3000
- **API Endpoints**: http://localhost:5000/api/

## 🎨 Web Interface Features

### Main Dashboard
- **Download Tab**: Single video downloads with advanced options
- **Playlist Tab**: Download entire playlists
- **Downloads Tab**: View and manage downloaded files

### Download Options
- **Audio Quality**: Choose from 8 bitrate options (32-320 kbps)
- **Output Directory**: Customize where files are saved
- **File Splitting**:
  - Split large files (>16MB) into chunks
  - Split by video chapters (perfect for albums!)
- **Smart Validation**: Prevents using conflicting options

### Real-time Feedback
- **Status Messages**: Clear feedback for all operations
- **Progress Indicators**: Visual feedback during downloads
- **Error Handling**: Graceful error messages and recovery

## 🏗️ Architecture

### Backend (Flask)
```
web_app.py              # Main Flask application
├── /api/download       # Single video downloads
├── /api/playlist       # Playlist downloads
├── /api/chapters       # Video chapter information
├── /api/formats        # Available audio formats
├── /api/downloads      # List downloaded files
└── /api/bitrates       # Available quality options
```

### Frontend (TypeScript + Webpack)
```
web/src/
├── components/         # UI components
│   ├── header.ts      # Application header
│   ├── tab-manager.ts # Tab navigation
│   ├── download-form.ts # Download form
│   └── downloads-list.ts # Downloads display
├── services/          # API services
│   └── api-service.ts # HTTP client
├── app.ts            # Main application
├── index.ts          # Entry point
└── styles.css        # Global styles
```

### Build System
- **Webpack 5**: Module bundling and development server
- **TypeScript**: Type-safe JavaScript compilation
- **Tailwind CSS**: Utility-first CSS framework
- **PostCSS**: CSS processing and optimization

## 🔧 Development

### Project Structure
```
youtube-audio-extractor/
├── web_app.py              # Flask web application
├── start_web_app.py        # Production startup script
├── dev_server.py           # Development startup script
├── requirements.txt         # Python dependencies
├── web/                    # Frontend source code
│   ├── src/               # TypeScript source
│   ├── package.json       # Node.js dependencies
│   ├── webpack.config.js  # Webpack configuration
│   ├── tsconfig.json      # TypeScript configuration
│   └── tailwind.config.js # Tailwind configuration
└── downloads/              # Downloaded audio files
```

### Development Workflow

1. **Start development servers:**
   ```bash
   python dev_server.py
   ```

2. **Make changes to TypeScript files** in `web/src/`
   - Files automatically recompile
   - Browser automatically refreshes

3. **Make changes to Python files** in project root
   - Flask server automatically restarts

4. **Access development environment:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:5000

### Building for Production

```bash
# Build frontend
cd web
npm run build
cd ..

# Start production server
python start_web_app.py
```

## 🌐 API Endpoints

### Health Check
```http
GET /api/health
```

### Download Audio
```http
POST /api/download
Content-Type: application/json

{
  "url": "https://youtube.com/watch?v=...",
  "output_dir": "music",
  "bitrate": "192",
  "split_large_files": false,
  "split_by_chapters": true
}
```

### Download Playlist
```http
POST /api/playlist
Content-Type: application/json

{
  "url": "https://youtube.com/playlist?list=...",
  "output_dir": "playlists",
  "bitrate": "320",
  "start_index": 1,
  "end_index": 10
}
```

### Get Video Chapters
```http
GET /api/chapters/{encoded_url}
```

### List Downloads
```http
GET /api/downloads
```

### Get Available Bitrates
```http
GET /api/bitrates
```

## 🎨 Customization

### Styling
- **Tailwind CSS**: Modify `web/tailwind.config.js`
- **Custom Components**: Edit `web/src/styles.css`
- **Theme Colors**: Update color palette in Tailwind config

### Components
- **New Components**: Add to `web/src/components/`
- **Component Styling**: Use Tailwind classes or custom CSS
- **Event Handling**: Follow existing patterns for consistency

### API Integration
- **New Endpoints**: Add to `web_app.py`
- **API Service**: Update `web/src/services/api-service.ts`
- **Error Handling**: Use consistent error response format

## 🚨 Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
# Reinstall frontend dependencies
cd web
rm -rf node_modules package-lock.json
npm install
cd ..
```

#### Port conflicts
```bash
# Check what's using the ports
lsof -i :3000  # Check port 3000
lsof -i :5000  # Check port 5000

# Kill processes if needed
kill -9 <PID>
```

#### Build errors
```bash
# Clean and rebuild
cd web
npm run clean
npm run build
cd ..
```

#### Flask import errors
```bash
# Ensure you're in the right directory
# and virtual environment is activated
pip install -r requirements.txt
```

### Debug Mode

Enable debug logging:
```bash
# Set environment variable
export FLASK_DEBUG=1

# Or modify web_app.py
app.run(debug=True, ...)
```

### Logs

- **Flask logs**: Check terminal output
- **Webpack logs**: Check terminal output
- **Browser logs**: Open Developer Tools → Console

## 🔒 Security Notes

- **No Authentication**: This is a local development tool
- **Local Access Only**: Server binds to localhost by default
- **File System Access**: Application can read/write to downloads directory
- **YouTube Compliance**: Users must follow YouTube's Terms of Service

## 📱 Browser Support

- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Development Guidelines

- **TypeScript**: Use strict mode and proper typing
- **Components**: Keep components focused and reusable
- **Styling**: Use Tailwind CSS utilities when possible
- **Error Handling**: Provide clear user feedback
- **Accessibility**: Include ARIA labels and keyboard navigation

## 📄 License

This project is licensed under the **MIT License with Attribution Requirements**. See the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the browser console for errors
3. Check the terminal output for backend errors
4. Open an issue on GitHub with detailed information

---

**Happy downloading! 🎵**

The web UI makes it easy to extract audio from YouTube videos and playlists with a beautiful, intuitive interface. No more command-line complexity - just point, click, and download!
