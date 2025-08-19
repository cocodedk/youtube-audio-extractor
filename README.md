# 🎵 YouTube Audio Extractor

A powerful Python command-line tool to extract audio from YouTube videos and **playlists** with advanced features like bitrate control, automatic file splitting, and chapter-based audio dissection.

## 📄 License

This project is licensed under the **MIT License with Attribution Requirements**. See the [LICENSE](LICENSE) file for details.

**Key License Terms:**
- ✅ **Open Source**: Free to use, modify, and distribute
- ✅ **Commercial Use**: Permitted with proper attribution
- ✅ **Attribution Required**: Must credit original author and link to repository
- ✅ **No Warranty**: Software provided "as is"
- ✅ **No Liability**: Author not responsible for damages or misuse
- ✅ **YouTube Compliance**: Users must follow YouTube's Terms of Service

## ✨ Features

- **🎬 Video Downloads**: Download audio from individual YouTube videos
- **📚 Playlist Downloads**: Download entire YouTube playlists with organized folder structure
- **🎚️ Bitrate Control**: Choose from 8 different audio quality levels (32-320 kbps)
- **✂️ Smart Splitting**: Automatically split large files into manageable chunks
- **📖 Chapter Splitting**: Split audio according to YouTube video chapters (perfect for albums!)
- **🔄 Format Conversion**: Convert to MP3 with custom quality settings
- **📁 Organized Output**: Clean folder structure for easy management

## 🚀 Installation

### Prerequisites

- **Python 3.7+**
- **FFmpeg** (required for audio processing)

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [FFmpeg official website](https://ffmpeg.org/download.html)

### Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage

### 🎬 Single Video Downloads

```bash
# Basic download (saves to downloads/)
python youtube_audio_extractor_main.py download "YOUR_YOUTUBE_URL"

# Custom subfolder (saves to downloads/music/)
python youtube_audio_extractor_main.py download "YOUR_YOUTUBE_URL" --output-dir music

# Custom bitrate (192 kbps)
python youtube_audio_extractor_main.py download "YOUR_YOUTUBE_URL" --bitrate 192

# Split large files automatically
python youtube_audio_extractor_main.py download "YOUR_YOUTUBE_URL" --split-large-files

# Split by video chapters
python youtube_audio_extractor_main.py download "YOUR_YOUTUBE_URL" --split-by-chapters
```

### 📚 Playlist Downloads

```bash
# Download entire playlist (saves to downloads/playlist_title/)
python youtube_audio_extractor_main.py playlist "YOUR_PLAYLIST_URL"

# High-quality playlist download
python youtube_audio_extractor_main.py playlist "YOUR_PLAYLIST_URL" --bitrate 320

# Download specific range of videos (videos 5-10)
python youtube_audio_extractor_main.py playlist "YOUR_PLAYLIST_URL" --start-index 5 --end-index 10

# Playlist with chapter splitting
python youtube_audio_extractor_main.py playlist "YOUR_PLAYLIST_URL" --split-by-chapters

# Playlist with size-based splitting
python youtube_audio_extractor_main.py playlist "YOUR_PLAYLIST_URL" --split-large-files

# Custom playlist folder (saves to downloads/my_playlists/)
python youtube_audio_extractor_main.py playlist "YOUR_PLAYLIST_URL" --output-dir my_playlists
```

### 🔍 Information Commands

```bash
# List available audio formats
python youtube_audio_extractor_main.py list-formats "YOUR_YOUTUBE_URL"

# List video chapters
python youtube_audio_extractor_main.py list-chapters "YOUR_YOUTUBE_URL"

# Check if video has chapters
python youtube_audio_extractor_main.py check-chapters "YOUR_YOUTUBE_URL"

# List playlist videos
python youtube_audio_extractor_main.py list-playlist "YOUR_PLAYLIST_URL"

# Show bitrate options
python youtube_audio_extractor_main.py bitrates

# Show help
python youtube_audio_extractor_main.py --help
```

## 🎚️ Audio Quality Options

| Bitrate | Quality    | File Size (per 1 min) | Use Case                    |
|---------|------------|----------------------|----------------------------|
| 32      | Very Low   | 0.24 MB             | Podcasts, voice recordings |
| 64      | Low        | 0.48 MB             | Basic audio, voice         |
| 96      | Fair       | 0.72 MB             | Good balance               |
| 128     | Good       | 0.96 MB             | Music, general use         |
| 160     | Better     | 1.2 MB              | High-quality music         |
| 192     | High       | 1.44 MB             | **Default** - Best balance |
| 256     | Very High  | 1.92 MB             | Lossless-like quality      |
| 320     | Maximum    | 2.4 MB              | Studio quality             |

## 📁 Output Structure

### Single Video Download
```
downloads/
├── video_title.mp3                    # Default location
├── custom_folder/                      # If --output-dir specified
│   ├── video_title.mp3
│   ├── chapters/                       # If --split-by-chapters used
│   └── split_chunks/                   # If --split-large-files used
├── chapters/                           # If --split-by-chapters used (default)
│   ├── video_title_chapter01_intro.mp3
│   ├── video_title_chapter02_main_content.mp3
│   └── ...
└── split_chunks/                       # If --split-large-files used (default)
    ├── video_title_part01.mp3
    ├── video_title_part02.mp3
    └── ...
```

### Playlist Download
```
downloads/
├── playlist_title/                     # Default location
│   ├── 01_video_title_1/
│   │   ├── video_title_1.mp3
│   │   ├── chapters/                   # If --split-by-chapters used
│   │   └── split_chunks/               # If --split-large-files used
│   ├── 02_video_title_2/
│   │   └── ...
│   └── 03_video_title_3/
│       └── ...
└── custom_folder/                       # If --output-dir specified
    └── playlist_title/
        ├── 01_video_title_1/
        │   └── ...
        └── 02_video_title_2/
            └── ...
```

### 🎯 **Important: All Downloads Go to Downloads Folder**

- **Default behavior**: Files are saved directly in `downloads/`
- **Custom folders**: If you specify `--output-dir music`, files go to `downloads/music/`
- **Playlists**: If you specify `--output-dir my_playlist`, it becomes `downloads/my_playlist/`
- **Always organized**: All content stays within the main `downloads/` directory
- **Git ignored**: The entire `downloads/` folder is excluded from version control

## 🔧 Advanced Features

### ✂️ File Splitting

**Size-Based Splitting** (`--split-large-files`):
- Automatically splits files larger than 16MB
- Creates manageable chunks for mobile devices
- Works with any bitrate setting

**Chapter-Based Splitting** (`--split-by-chapters`):
- Splits audio according to YouTube video chapters
- Perfect for music albums and educational content
- Creates meaningful filenames automatically

### 📚 Chapter Splitting Example

**Input**: "Best of 2024 - Complete Album" (45 minutes)
**Output**:
```
chapters/
├── best_of_2024_chapter01_intro_track.mp3
├── best_of_2024_chapter02_hit_song_1.mp3
├── best_of_2024_chapter03_featured_artist.mp3
└── ...
```

### 🎯 Playlist Features

- **Range Selection**: Download specific videos from a playlist
- **Organized Structure**: Each video gets its own numbered folder
- **Full Integration**: All splitting options work with playlists
- **Progress Tracking**: Shows download progress for each video

## 💡 Use Cases

### 🎵 Music Lovers
- Download complete albums with chapter splitting
- Convert playlists to MP3 collections
- High-quality audio for offline listening

### 🎧 Podcast Enthusiasts
- Download podcast series as playlists
- Split long episodes by chapters
- Optimize file sizes for mobile devices

### 📚 Educational Content
- Download lecture series
- Split long videos by topic sections
- Create organized audio libraries

### 🎬 Content Creators
- Extract audio from video content
- Create audio versions of playlists
- Batch process multiple videos

## 🚨 Important Notes

- **Cannot use both splitting methods** (`--split-large-files` and `--split-by-chapters`) simultaneously
- **FFmpeg is required** for audio processing and splitting
- **Playlist URLs** must contain `playlist` or `list=` parameter
- **Chapter splitting** only works with videos that have chapters
- **Large playlists** may take significant time to download
- **Users must comply** with YouTube's Terms of Service and copyright laws
- **Download folders are gitignored** - All downloaded content is automatically excluded from version control

## 📁 Repository Structure

This repository is configured to automatically exclude all downloaded content:

```
youtube-audio-extractor/
├── youtube_audio_extractor/     # Source code
├── downloads/                    # ⚠️ Gitignored - Downloaded content
├── python_basics_test/          # ⚠️ Gitignored - Test downloads
├── python_course_chapters/      # ⚠️ Gitignored - Test downloads
├── air_moon_safari_album/       # ⚠️ Gitignored - Test downloads
├── .gitignore                   # Excludes all download folders
├── README.md                    # This file
└── LICENSE                      # License file
```

**Note:** All download folders and their contents are automatically excluded from Git via `.gitignore` to keep the repository clean and avoid committing large audio files.

## 🛠️ Troubleshooting

### Common Issues

**"FFmpeg not found" error:**
- Install FFmpeg using the instructions above
- Ensure FFmpeg is in your system PATH

**"Invalid YouTube URL" error:**
- Check that the URL is a valid YouTube video or playlist
- For playlists, ensure the URL contains playlist information

**"No chapters found" warning:**
- Not all videos have chapters
- Use `--split-large-files` instead for size-based splitting

**Download failures:**
- Check your internet connection
- Verify the video/playlist is publicly accessible
- Try with a different bitrate setting

## 🔄 Shell Wrappers

For convenience, shell wrapper scripts are provided:

**Bash:**
```bash
./yae.sh download "YOUR_YOUTUBE_URL"
./yae.sh playlist "YOUR_PLAYLIST_URL"
```

**Fish:**
```fish
./yae.fish download "YOUR_YOUTUBE_URL"
./yae.fish playlist "YOUR_PLAYLIST_URL"
```

## 📝 Examples

### Download a Music Album with Chapters
```bash
python youtube_audio_extractor_main.py download "https://youtu.be/album_url" --bitrate 320 --split-by-chapters
```

### Download a Podcast Playlist
```bash
python youtube_audio_extractor_main.py playlist "https://youtube.com/playlist?list=playlist_id" --bitrate 128
```

### Download Specific Videos from a Playlist
```bash
python youtube_audio_extractor_main.py playlist "https://youtube.com/playlist?list=playlist_id" --start-index 5 --end-index 10 --bitrate 192
```

## 🤝 Contributing

We welcome contributions! Please ensure you:

1. **Follow the license terms** - Maintain attribution requirements
2. **Respect copyright** - Don't use for unauthorized content
3. **Test thoroughly** - Ensure changes don't break existing functionality
4. **Document changes** - Update README and code comments

## 📄 License Details

This project uses a **custom MIT license with mandatory attribution requirements**. The key differences from standard MIT:

- **Attribution is mandatory** and cannot be waived
- **Clear liability limitations** protect the author
- **YouTube compliance requirements** are explicitly stated
- **Commercial use is permitted** with proper attribution

**Full license text:** [LICENSE](LICENSE)

## 📞 Contact

For questions about this license or the project, please contact: [Your Contact Information]

---

**Disclaimer**: This tool is for educational and personal use only. Users are responsible for complying with YouTube's Terms of Service and applicable copyright laws. The authors do not condone unauthorized downloading of copyrighted content.
