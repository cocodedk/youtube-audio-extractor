# YouTube Audio Extractor - Chapter-Based Splitting Feature

## 🎉 **New Feature: Chapter-Based Audio Splitting!**

Your YouTube Audio Extractor now supports **automatic splitting of audio files according to YouTube video chapters**. This is perfect for albums, podcasts, educational content, and any video with well-defined sections.

## 📚 **What is Chapter-Based Splitting?**

YouTube videos can have **chapters** - timestamps that divide the video into logical sections. Examples include:
- **Music albums** with individual track timestamps
- **Podcasts** with episode segments
- **Educational videos** with lesson sections
- **Audiobooks** with chapter divisions
- **Tutorials** with step-by-step sections

## ✨ **New Commands Added**

### **1. Check if Video Has Chapters**
```bash
python youtube_audio_extractor_main.py check-chapters "YOUTUBE_URL"
```
**Output:**
- ✅ **This video has chapters!** - Use `--split-by-chapters` to split audio by chapters
- ❌ **This video doesn't have chapters** - Use `--split-large-files` to split by file size instead

### **2. List All Available Chapters**
```bash
python youtube_audio_extractor_main.py list-chapters "YOUTUBE_URL"
```
**Output:**
- 📺 Video title and duration
- 📚 Total number of chapters
- 📖 Detailed chapter information with timestamps
- 🧹 Cleaned chapter titles for filenames

### **3. Download with Chapter Splitting**
```bash
python youtube_audio_extractor_main.py download "YOUTUBE_URL" --split-by-chapters
```
**What happens:**
- 🎵 Downloads the complete audio file
- 📚 Detects video chapters automatically
- ✂️ Splits audio according to chapter timestamps
- 📁 Saves each chapter as a separate MP3 file
- 🏷️ Creates meaningful filenames based on chapter titles

## 🎯 **Perfect Use Cases**

### **🎼 Music Albums**
- **Input**: Single video with multiple tracks
- **Output**: Individual MP3 files for each song
- **Example**: `album_title_chapter01_song_name.mp3`

### **🎙️ Podcasts**
- **Input**: Long podcast episode with segments
- **Output**: Separate files for each segment
- **Example**: `podcast_chapter01_intro.mp3`, `podcast_chapter02_main_topic.mp3`

### **📚 Educational Content**
- **Input**: Tutorial video with lesson sections
- **Output**: Individual lesson files
- **Example**: `tutorial_chapter01_basics.mp3`, `tutorial_chapter02_advanced.mp3`

### **📖 Audiobooks**
- **Input**: Book reading with chapter divisions
- **Output**: Separate files for each chapter
- **Example**: `book_title_chapter01_introduction.mp3`

## 🔧 **How It Works**

### **1. Chapter Detection**
- Uses `yt-dlp` to extract video metadata
- Automatically detects chapter timestamps
- Extracts chapter titles and durations

### **2. Filename Cleaning**
- Removes problematic characters (`<>:"/\|?*`)
- Replaces spaces with underscores
- Limits filename length to 100 characters
- Creates safe, readable filenames

### **3. Audio Splitting**
- Uses FFmpeg for precise audio cutting
- Maintains audio quality during splitting
- Creates separate MP3 files for each chapter
- Organizes files in a dedicated `chapters/` subfolder

## 📁 **Output Structure**

```
downloads/
├── video_title.mp3                    # Original complete file
└── chapters/                          # Chapter-based files
    ├── video_title_chapter01_intro.mp3    # Chapter 1: Intro
    ├── video_title_chapter02_main.mp3     # Chapter 2: Main Content
    ├── video_title_chapter03_examples.mp3 # Chapter 3: Examples
    └── video_title_chapter04_summary.mp3  # Chapter 4: Summary
```

## 🚫 **Important Limitations**

### **Mutual Exclusivity**
- **Cannot use both** `--split-large-files` and `--split-by-chapters`
- **Chapter splitting takes priority** when both are specified
- **Clear error message** guides users to choose one method

### **Chapter Availability**
- **Not all videos have chapters**
- **Warning displayed** if chapters not found
- **Graceful fallback** - continues with normal download
- **No error** - just informational message

### **Chapter Quality**
- **Depends on video creator** adding chapter timestamps
- **Automatic detection** - no manual configuration needed
- **Best results** with well-structured videos

## 💡 **Best Practices**

### **Before Downloading**
1. **Check if video has chapters**: `check-chapters` command
2. **Review chapter structure**: `list-chapters` command
3. **Choose appropriate splitting method**

### **For Best Results**
- Use videos with **clear chapter divisions**
- Ensure **chapter titles are descriptive**
- Consider **audio quality** (bitrate) for your needs
- **Test with a small video** first

### **File Management**
- Chapter files are in **dedicated subfolder**
- **Meaningful filenames** make organization easy
- **Original file can be removed** after splitting
- **Consistent naming convention** across all files

## 🔍 **Example Workflow**

### **Step 1: Check Video**
```bash
python youtube_audio_extractor_main.py check-chapters "https://youtu.be/example"
```

### **Step 2: Review Chapters**
```bash
python youtube_audio_extractor_main.py list-chapters "https://youtu.be/example"
```

### **Step 3: Download with Chapter Splitting**
```bash
python youtube_audio_extractor_main.py download "https://youtu.be/example" --bitrate 320 --split-by-chapters
```

### **Step 4: Enjoy Organized Audio Files**
- 📁 Check the `chapters/` subfolder
- 🎵 Each chapter as a separate MP3 file
- 🏷️ Meaningful filenames for easy identification
- 📱 Perfect for mobile devices and organization

## 🎵 **Real-World Examples**

### **Music Album**
```
Input: "Best of 2024 - Complete Album" (45 minutes)
Output:
├── best_of_2024_chapter01_intro_track.mp3
├── best_of_2024_chapter02_hit_song_1.mp3
├── best_of_2024_chapter03_hit_song_2.mp3
└── best_of_2024_chapter04_outro_track.mp3
```

### **Podcast Episode**
```
Input: "Weekly Tech News - Episode 50" (60 minutes)
Output:
├── weekly_tech_news_chapter01_intro.mp3
├── weekly_tech_news_chapter02_ai_news.mp3
├── weekly_tech_news_chapter03_gaming_updates.mp3
└── weekly_tech_news_chapter04_q_and_a.mp3
```

### **Educational Tutorial**
```
Input: "Complete Python Course for Beginners" (90 minutes)
Output:
├── python_course_chapter01_installation.mp3
├── python_course_chapter02_basic_syntax.mp3
├── python_course_chapter03_functions.mp3
└── python_course_chapter04_practice_exercises.mp3
```

## 🚀 **Benefits of Chapter Splitting**

### **✅ Organization**
- **Logical file structure** based on content
- **Easy navigation** between sections
- **Professional appearance** for shared content

### **✅ Usability**
- **Skip to specific sections** without seeking
- **Individual file management** for different purposes
- **Mobile-friendly** file sizes

### **✅ Accessibility**
- **Clear content identification** through filenames
- **Easy sharing** of specific sections
- **Better organization** for playlists

## 🎉 **Summary**

The new **Chapter-Based Splitting** feature transforms your YouTube Audio Extractor into a powerful tool for:

- 🎼 **Music albums** → Individual track files
- 🎙️ **Podcasts** → Episode segments
- 📚 **Educational content** → Lesson files
- 📖 **Audiobooks** → Chapter divisions
- 🎯 **Any structured content** → Organized sections

**Your audio library will never be the same!** 🎵✨

---

**Ready to try it?** Start with:
```bash
python youtube_audio_extractor_main.py check-chapters "YOUR_YOUTUBE_URL"
```
