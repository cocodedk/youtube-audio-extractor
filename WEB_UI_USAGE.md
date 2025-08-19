# 🎵 YouTube Audio Extractor - Web UI Usage Guide

A step-by-step guide to using the beautiful dark-themed web interface for downloading YouTube audio.

## 🚀 Quick Start

### 1. Start the Web Application
```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Start the web app
python start_web_app.py
```

### 2. Open Your Browser
Navigate to: **http://localhost:5000**

The app will automatically redirect you to the web interface.

## 🎯 Main Features

### **Download Tab** - Single Video Downloads
Perfect for downloading individual YouTube videos.

#### How to Use:
1. **Enter YouTube URL**: Paste any YouTube video URL
2. **Choose Quality**: Select from 8 bitrate options (32-320 kbps)
3. **Set Output Directory**: Optional custom folder name
4. **Configure Splitting**: Choose file splitting options
5. **Click Download**: Start the audio extraction

#### Example URLs:
- `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- `https://youtu.be/dQw4w9WgXcQ`

### **Playlist Tab** - Multiple Video Downloads
Ideal for downloading entire YouTube playlists or specific ranges.

#### How to Use:
1. **Enter Playlist URL**: Paste a YouTube playlist URL
2. **Set Video Range**: Choose start and end video numbers
3. **Configure Options**: Same quality and splitting options
4. **Click Download Playlist**: Start batch download

#### Example Playlist URLs:
- `https://www.youtube.com/playlist?list=PLxxxxxxxx`
- `https://youtube.com/playlist?list=PLxxxxxxxx`

#### Range Selection Examples:
- **Videos 1-10**: Start: 1, End: 10
- **Videos 5-15**: Start: 5, End: 15
- **All videos**: Start: 1, End: (leave empty)

### **Downloads Tab** - File Management
View and manage all your downloaded audio files.

#### Features:
- **File List**: See all downloaded MP3s and folders
- **File Information**: Size, date, and modification time
- **Folder Support**: Organized by playlists and custom directories
- **Refresh**: Update the list after new downloads
- **Open in File Browser**: Click "Open" button to open any folder in your system's file browser
- **Search Filter**: Real-time search through downloads by name, type, file count, size, or date

### **About Tab** - Project Information
Learn more about the YouTube Audio Extractor project and its contributors.

#### Features:
- **Project Overview**: Detailed description and key features
- **Technology Stack**: Backend, frontend, audio processing, and build tools
- **Project Links**: GitHub repository, PyPI package, and issue reporting
- **Credits & Support**: Information about contributors and licensing
- **Special Thanks**: Recognition of cocode.dk and other supporters

## ⚙️ Configuration Options

### **Audio Quality Settings**
| Bitrate | Quality | File Size (per 1 min) | Best For |
|----------|---------|----------------------|-----------|
| 32 kbps | Very Low | 0.24 MB | Podcasts, voice recordings |
| 64 kbps | Low | 0.48 MB | Basic audio, voice |
| 96 kbps | Fair | 0.72 MB | Good balance |
| 128 kbps | Good | 0.96 MB | Music, general use |
| 160 kbps | Better | 1.2 MB | High-quality music |
| **192 kbps** | **High** | **1.44 MB** | **Default - Best balance** |
| 256 kbps | Very High | 1.92 MB | Lossless-like quality |
| 320 kbps | Maximum | 2.4 MB | Studio quality |

### **File Splitting Options**

#### **Split Large Files** (>16MB)
- Automatically splits files larger than 16MB
- Creates manageable chunks for mobile devices
- Works with any bitrate setting

#### **Split by Video Chapters**
- Splits audio according to YouTube video chapters
- Perfect for music albums and educational content
- Creates meaningful filenames automatically

⚠️ **Note**: You cannot use both splitting methods simultaneously

### **Output Directory**
- **Default**: Files save to `downloads/` folder
- **Custom**: Enter folder name (e.g., "music", "podcasts")
- **Result**: Files save to `downloads/your_folder_name/`

## 🌙 Dark Mode Theme

The web interface features a modern, eye-friendly dark theme designed for comfortable use in any lighting condition:

- **Dark Backgrounds**: Deep, rich dark colors that reduce eye strain
- **High Contrast**: Clear text and elements for excellent readability
- **Modern Aesthetics**: Sleek, professional appearance with smooth transitions
- **Accessibility**: Optimized color combinations for better visibility

## 📱 User Interface Guide

### **Header Section**
- **Logo**: Click to return to main view
- **Title**: Shows current application name
- **GitHub Link**: Access source code and documentation

### **Tab Navigation**
- **Download**: Single video download form
- **Playlist**: Playlist download form with range options
- **Downloads**: File management and viewing

### **Form Elements**
- **URL Input**: Paste YouTube URLs here
- **Quality Dropdown**: Select audio bitrate
- **Checkboxes**: Enable/disable splitting options
- **Action Buttons**: Start downloads or refresh lists

### **Status Messages**
- **Blue**: Information and progress updates
- **Green**: Success confirmations
- **Red**: Error messages and warnings
- **Yellow**: Important notices

## 🔄 Download Process

### **Step-by-Step Workflow**

1. **Prepare**
   - Copy YouTube URL from browser
   - Decide on quality and splitting preferences

2. **Configure**
   - Paste URL into the form
   - Select desired options
   - Choose output directory (optional)

3. **Download**
   - Click appropriate download button
   - Watch for status messages
   - Monitor progress indicators

4. **Complete**
   - Check status message for confirmation
   - View files in Downloads tab
   - Access files in your downloads folder

### **What Happens During Download**

1. **URL Validation**: Checks if URL is valid YouTube link
2. **Video Analysis**: Extracts video information and available formats
3. **Audio Extraction**: Downloads and converts to MP3
4. **File Processing**: Applies splitting if enabled
5. **Organization**: Saves to appropriate folder structure

## 📁 File Organization

### **🔍 Search & Filter System**
The downloads list includes a powerful real-time search and filter system:

- **Instant Search**: Type to search as you type
- **Multi-Field Search**: Searches across name, type, file count, size, and date
- **Smart Filtering**: Automatically filters results in real-time
- **Clear Search**: Easy one-click clear button to reset search
- **Result Counter**: Shows how many results match your search

**Searchable Fields:**
- **File/Folder Names**: Search by exact or partial names
- **Types**: Search for "folder", "file", "mp3", etc.
- **File Counts**: Search by number of MP3s in folders
- **File Sizes**: Search by size (e.g., "128 MB", "2.5 GB")
- **Dates**: Search by modification date

### **🌐 File Browser Integration**
The web interface includes a powerful feature to open any download location directly in your system's file browser:

- **Cross-Platform Support**: Works on Linux, macOS, and Windows
- **Smart Detection**: Automatically detects your operating system
- **Security**: Only allows opening folders within the downloads directory
- **Easy Access**: Click the "Open" button next to any folder or file

**How it works:**
- **Linux**: Uses `xdg-open` or common file managers (Nautilus, Dolphin, Thunar)
- **macOS**: Uses the native `open` command
- **Windows**: Uses Windows Explorer

### **Single Video Downloads**
```
downloads/
├── video_title.mp3                    # Default location
├── custom_folder/                      # If --output-dir specified
│   ├── video_title.mp3
│   ├── chapters/                       # If --split-by-chapters used
│   └── split_chunks/                   # If --split-large-files used
```

### **Playlist Downloads**
```
downloads/
├── playlist_title/                     # Default location
│   ├── 01_video_title_1/
│   │   ├── video_title_1.mp3
│   │   ├── chapters/                   # If --split-by-chapters used
│   │   └── split_chunks/               # If --split-large-files used
│   ├── 02_video_title_2/
│   └── 03_video_title_3/
```

### **Custom Output Directories**
```
downloads/
├── music/                              # Custom folder
│   ├── video_title.mp3
│   └── playlist_title/
├── podcasts/                           # Another custom folder
└── albums/                             # Yet another custom folder
```

## 🚨 Troubleshooting

### **Common Issues & Solutions**

#### **"Invalid YouTube URL" Error**
- **Problem**: URL format not recognized
- **Solution**: Ensure URL starts with `https://www.youtube.com/` or `https://youtu.be/`
- **Check**: URL contains video ID or playlist ID

#### **Download Fails to Start**
- **Problem**: No error message, but download doesn't begin
- **Solution**: Check browser console for JavaScript errors
- **Check**: Ensure Flask backend is running on port 5000

#### **Empty Downloads List**
- **Problem**: Downloads tab shows no files
- **Solution**: Click the "Refresh" button
- **Check**: Ensure files were actually downloaded to the correct folder

#### **Page Shows Empty/White**
- **Problem**: Web interface doesn't load
- **Solution**: Check if Webpack dev server is running on port 3000
- **Check**: Browser console for JavaScript errors

#### **API Errors (500/404)**
- **Problem**: Backend API calls fail
- **Solution**: Restart Flask server
- **Check**: Ensure all Python dependencies are installed

### **Browser Compatibility**
- **Chrome**: 90+ (Recommended)
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

### **System Requirements**
- **Python**: 3.7+
- **Node.js**: 16+
- **FFmpeg**: Required for audio processing
- **Memory**: At least 2GB RAM
- **Storage**: Sufficient space for audio files

## 💡 Pro Tips

### **For Music Lovers**
- Use **320 kbps** for high-quality music
- Enable **chapter splitting** for albums
- Create **custom folders** for different genres

### **For Podcast Enthusiasts**
- Use **128 kbps** for good quality/size balance
- Enable **large file splitting** for long episodes
- Use **playlist downloads** for series

### **For Educational Content**
- Use **192 kbps** for clear speech
- Enable **chapter splitting** for organized lectures
- Create **topic-based folders** for organization

### **For Mobile Users**
- Enable **large file splitting** for mobile compatibility
- Use **lower bitrates** (96-128 kbps) to save space
- Create **mobile-friendly folder names**

### **For File Management**
- Use the **"Open" button** to quickly access downloaded files in your file browser
- **Organize downloads** by creating custom output directories
- **Browse playlists** easily by opening their folders directly
- **Use search filters** to quickly find specific files or folders
- **Search by date** to find recent downloads
- **Filter by size** to locate large audio files

## 🔒 Privacy & Security

### **Local Processing**
- **No Uploads**: Videos are processed locally on your machine
- **No Tracking**: No user data is sent to external servers
- **Private**: All downloads stay on your local system

### **YouTube Compliance**
- **Terms of Service**: Must follow YouTube's ToS
- **Copyright**: Respect intellectual property rights
- **Personal Use**: Intended for personal, non-commercial use

### **File Management**
- **Downloads Folder**: All content goes to local downloads directory
- **No Cloud**: Files are not uploaded anywhere
- **Full Control**: You control all downloaded content

## 📞 Getting Help

### **Self-Service**
1. **Check this guide** for common solutions
2. **Review error messages** in the web interface
3. **Check browser console** for JavaScript errors
4. **Verify server status** in terminal output

### **When to Seek Help**
- **Persistent errors** that don't resolve with restart
- **Feature requests** for new functionality
- **Bug reports** for unexpected behavior
- **Installation issues** on specific systems

### **How to Report Issues**
1. **Describe the problem** clearly
2. **Include error messages** from interface and console
3. **Specify your system** (OS, browser, versions)
4. **Provide steps** to reproduce the issue

---

## 🎉 You're Ready!

The web UI makes YouTube audio extraction simple and beautiful. Start with a single video download to get familiar, then explore playlists and advanced features.

**Happy downloading! 🎵**

---

*This guide covers the web interface. For command-line usage, see the main README.md file.*
