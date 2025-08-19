# 🎵 YouTube Audio Extractor

A powerful, user-friendly tool to extract audio from YouTube videos and playlists. Available as both a **modern web interface** and **command-line tool** with advanced features like bitrate control, automatic file splitting, and chapter-based audio extraction.

## 🚀 Quick Start

### 🌐 **Web Interface (Recommended for Most Users)**

The easiest way to use this tool is through our beautiful web interface:

1. **Install and Start** (one command):
   ```bash
   ./start_ui.sh    # Linux/macOS
   ```
   ```cmd
   start_server.bat # Windows
   ```

2. **Open your browser** to http://localhost:5000

3. **Paste YouTube URL** and click download!

That's it! The web interface handles everything automatically.

### 🖥️ **Command Line (For Advanced Users)**

Quick CLI usage:
```bash
./yae.sh download "https://youtube.com/watch?v=VIDEO_ID"
./yae.sh playlist "https://youtube.com/playlist?list=PLAYLIST_ID"
```

---

## 📦 Installation

### Step 1: Prerequisites

- **Python 3.7+**
- **Node.js 16+** (for web interface)
- **FFmpeg** (for audio processing)

### Step 2: Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [FFmpeg official website](https://ffmpeg.org/download.html) and add to PATH.

### Step 3: Setup Project

```bash
# Clone or download this repository
git clone <repository-url>
cd yt-audio-extractor

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install Python dependencies
pip install -r requirements.txt

# Install web interface dependencies (for web UI)
cd web && npm install && cd ..
```

---

## 🌐 Web Interface Usage

### 🚀 **Option 1: Smart Startup (Recommended)**

Use our intelligent startup script that handles everything:

**Linux/macOS:**
```bash
./start_ui.sh
```

**Windows:**
```cmd
start_server.bat
```

The script will:
- ✅ Check all dependencies
- ✅ Install missing packages
- ✅ Build the web interface
- ✅ Start the server
- ✅ Give you options for development or production mode

### 🎯 **Option 2: Manual Startup**

**Production Mode (Single Server):**
```bash
# Activate virtual environment
source venv/bin/activate

# Start production server
python3 start_web_app.py
```
- **URL**: http://localhost:5000
- **Features**: Optimized, single server, production-ready

**Development Mode (Hot Reload):**
```bash
# Activate virtual environment
source venv/bin/activate

# Start development server
python3 dev_server.py
```
- **Frontend**: http://localhost:3000 (with hot reload)
- **Backend**: http://localhost:5000 (API server)
- **Features**: Live updates, development tools

### 🎨 **Web Interface Features**

- **🎯 Drag & Drop**: Drop YouTube URLs directly onto the page
- **📊 Real-time Progress**: Live download progress with speed indicators
- **🎚️ Quality Control**: Choose from 8 different audio quality levels
- **✂️ Smart Splitting**: Options for chapter-based or size-based splitting
- **📱 Mobile Friendly**: Works perfectly on phones and tablets
- **🌙 Dark Theme**: Beautiful, modern dark interface
- **📁 Auto-Open**: Automatically opens download folder when complete
- **📋 Download History**: Keep track of all your downloads

### 📱 **How to Use Web Interface**

1. **Start the server** using one of the methods above
2. **Open your browser** to the provided URL
3. **Paste or drag** a YouTube URL into the input field
4. **Choose settings**:
   - **Output folder**: Where to save files (optional)
   - **Audio quality**: 32-320 kbps (192 kbps recommended)
   - **Splitting options**: By chapters or file size
5. **Click Download** and watch the real-time progress
6. **Files automatically open** in your file manager when complete

---

## 🖥️ Command Line Usage

### 🎯 **Quick CLI Commands**

We provide convenient wrapper scripts:

**Bash (Linux/macOS):**
```bash
./yae.sh download "https://youtube.com/watch?v=VIDEO_ID"
./yae.sh playlist "https://youtube.com/playlist?list=PLAYLIST_ID"
./yae.sh --help
```

**Fish Shell:**
```bash
./yae.fish download "https://youtube.com/watch?v=VIDEO_ID"
./yae.fish playlist "https://youtube.com/playlist?list=PLAYLIST_ID"
./yae.fish --help
```

### 🎬 **Single Video Downloads**

```bash
# Basic download (saves to downloads/)
python3 youtube_audio_extractor_main.py download "YOUR_YOUTUBE_URL"

# Custom folder (saves to downloads/music/)
python3 youtube_audio_extractor_main.py download "YOUR_YOUTUBE_URL" --output-dir music

# High quality (320 kbps)
python3 youtube_audio_extractor_main.py download "YOUR_YOUTUBE_URL" --bitrate 320

# Split by chapters (perfect for albums!)
python3 youtube_audio_extractor_main.py download "YOUR_YOUTUBE_URL" --split-by-chapters

# Split large files automatically
python3 youtube_audio_extractor_main.py download "YOUR_YOUTUBE_URL" --split-large-files
```

### 📚 **Playlist Downloads**

```bash
# Download entire playlist
python3 youtube_audio_extractor_main.py playlist "YOUR_PLAYLIST_URL"

# High-quality playlist
python3 youtube_audio_extractor_main.py playlist "YOUR_PLAYLIST_URL" --bitrate 320

# Download specific range (videos 5-10)
python3 youtube_audio_extractor_main.py playlist "YOUR_PLAYLIST_URL" --start-index 5 --end-index 10

# Playlist with chapter splitting
python3 youtube_audio_extractor_main.py playlist "YOUR_PLAYLIST_URL" --split-by-chapters
```

### 🔍 **Information Commands**

```bash
# Show available audio qualities
python3 youtube_audio_extractor_main.py bitrates

# List video chapters
python3 youtube_audio_extractor_main.py list-chapters "YOUR_YOUTUBE_URL"

# List playlist videos
python3 youtube_audio_extractor_main.py list-playlist "YOUR_PLAYLIST_URL"

# Show all available formats
python3 youtube_audio_extractor_main.py list-formats "YOUR_YOUTUBE_URL"

# Check if video has chapters
python3 youtube_audio_extractor_main.py check-chapters "YOUR_YOUTUBE_URL"

# Show help
python3 youtube_audio_extractor_main.py --help
```

---

## 🎚️ Audio Quality Guide

| Bitrate | Quality    | File Size (per min) | Best For                    |
|---------|------------|--------------------|-----------------------------|
| 32      | Very Low   | 0.24 MB            | Podcasts, voice recordings  |
| 64      | Low        | 0.48 MB            | Basic audio, voice          |
| 96      | Fair       | 0.72 MB            | Good balance               |
| 128     | Good       | 0.96 MB            | Music, general use         |
| 160     | Better     | 1.2 MB             | High-quality music         |
| **192** | **High**   | **1.44 MB**        | **🎯 Recommended default** |
| 256     | Very High  | 1.92 MB            | Lossless-like quality      |
| 320     | Maximum    | 2.4 MB             | Studio quality             |

**💡 Recommendation**: 192 kbps offers the best balance of quality and file size for most users.

---

## ✨ Advanced Features

### ✂️ **Smart File Splitting**

**Chapter-Based Splitting** (`--split-by-chapters`):
- 🎵 Perfect for music albums
- 📚 Great for educational content
- 🎧 Ideal for podcasts with segments
- ✨ Creates meaningful filenames automatically

**Size-Based Splitting** (`--split-large-files`):
- 📱 Creates mobile-friendly file sizes
- 💾 Splits files larger than 16MB
- 🔄 Works with any bitrate setting
- 📁 Organized in `split_chunks/` folder

### 📁 **Output Structure**

**Single Video:**
```
downloads/
├── video_title.mp3                    # Main file
├── chapters/                          # If using --split-by-chapters
│   ├── video_title_01_intro.mp3
│   ├── video_title_02_main_content.mp3
│   └── video_title_03_conclusion.mp3
└── split_chunks/                      # If using --split-large-files
    ├── video_title_part01.mp3
    └── video_title_part02.mp3
```

**Playlist:**
```
downloads/
└── playlist_title/
    ├── 01_first_video/
    │   ├── first_video.mp3
    │   └── chapters/              # If chapter splitting enabled
    ├── 02_second_video/
    │   └── second_video.mp3
    └── 03_third_video/
        └── third_video.mp3
```

---

## 🎯 Common Use Cases

### 🎵 **Music Lovers**
```bash
# Download album with chapters
./yae.sh download "https://youtube.com/watch?v=ALBUM_URL" --bitrate 320 --split-by-chapters
```

### 🎧 **Podcast Enthusiasts**
```bash
# Download podcast series
./yae.sh playlist "https://youtube.com/playlist?list=PODCAST_PLAYLIST" --bitrate 128
```

### 📚 **Educational Content**
```bash
# Download lecture series with chapters
./yae.sh playlist "https://youtube.com/playlist?list=COURSE_PLAYLIST" --split-by-chapters
```

### 🎬 **Content Creators**
```bash
# Batch download for audio editing
./yae.sh playlist "https://youtube.com/playlist?list=CONTENT_PLAYLIST" --bitrate 256
```

---

## 🛠️ Troubleshooting

### **Web Interface Issues**

**Server won't start:**
```bash
# Check if port is in use
lsof -i :5000  # Linux/macOS
netstat -an | findstr :5000  # Windows

# Try different port
python3 start_web_app.py --port 8080
```

**Web page won't load:**
- Check firewall settings
- Try http://127.0.0.1:5000 instead of localhost
- Ensure virtual environment is activated

### **CLI Issues**

**"FFmpeg not found":**
- Install FFmpeg using instructions above
- Ensure FFmpeg is in your system PATH
- Test with: `ffmpeg -version`

**"Invalid YouTube URL":**
- Ensure URL is a valid YouTube video/playlist
- For playlists, URL must contain `list=` parameter
- Try copying URL directly from browser

**Download failures:**
- Check internet connection
- Verify video/playlist is publicly accessible
- Try different bitrate setting
- Check if video has age restrictions

### **Permission Issues**

**Linux/macOS:**
```bash
# Make scripts executable
chmod +x start_ui.sh yae.sh yae.fish
```

**Windows:**
```cmd
# Run as administrator if needed
# Or use PowerShell: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📋 Startup Scripts Reference

We provide several startup scripts for different needs:

| Script | Platform | Purpose |
|--------|----------|---------|
| `start_ui.sh` | Linux/macOS | Smart interactive startup |
| `start_server.sh` | Linux/macOS | Production server startup |
| `start_server.bat` | Windows | Windows batch startup |
| `start_server.ps1` | Windows | PowerShell startup |
| `yae.sh` | Linux/macOS | CLI wrapper (Bash) |
| `yae.fish` | Fish Shell | CLI wrapper (Fish) |

**For detailed startup options, see:** [STARTUP_SCRIPTS_README.md](STARTUP_SCRIPTS_README.md)

---

## 🚨 Important Notes

- **⚖️ Legal Compliance**: Users must comply with YouTube's Terms of Service and copyright laws
- **🔒 Personal Use**: This tool is for educational and personal use only
- **📁 Auto-Gitignore**: All downloads are automatically excluded from version control
- **🚫 Splitting Limits**: Cannot use both splitting methods simultaneously
- **📺 Chapter Requirement**: Chapter splitting only works with videos that have chapters
- **⏱️ Large Playlists**: May take significant time to download

---

## 📄 License

This project is licensed under the **MIT License with Attribution Requirements**.

**Key Points:**
- ✅ Free to use, modify, and distribute
- ✅ Commercial use permitted with attribution
- ✅ Must credit original author
- ⚠️ No warranty provided
- ⚠️ Users responsible for YouTube ToS compliance

**Full license:** [LICENSE](LICENSE)

---

## 🤝 Contributing

We welcome contributions! Please:

1. **Follow license terms** - Maintain attribution requirements
2. **Respect copyright** - Don't enable unauthorized content downloading
3. **Test thoroughly** - Ensure changes work across platforms
4. **Document changes** - Update README and code comments

---

## 📞 Support

**For questions or issues:**
- 📧 Contact: COCODE.DK
- 📖 Check troubleshooting section above
- 🐛 Report bugs with detailed error messages

---

**⚠️ Disclaimer**: This tool is for educational and personal use only. Users are responsible for complying with YouTube's Terms of Service and applicable copyright laws. The authors do not condone unauthorized downloading of copyrighted content.
