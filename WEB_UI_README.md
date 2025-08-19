# Web UI for YouTube Audio Extractor

A modern, responsive web interface for the YouTube Audio Extractor tool.

## Features

- **Modern UI**: Built with TypeScript, Tailwind CSS, and modern web technologies
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Progress Tracking**: Monitor download progress with live progress bars
- **Playlist Support**: Download entire playlists with range selection
- **Audio Quality Options**: Choose from 32 kbps to 320 kbps bitrates
- **File Splitting**: Automatic splitting of large files and chapter-based splitting
- **Dark Theme**: Easy on the eyes with a modern dark color scheme

## Progress Bar Features

The web UI now includes a comprehensive progress tracking system that provides real-time updates during downloads:

### Single Video Downloads
- **Overall Progress**: Shows download percentage and downloaded/total bytes
- **Current Step**: Displays the current operation (downloading, processing, splitting, etc.)
- **Speed & ETA**: Real-time download speed and estimated time remaining
- **Status Updates**: Live status messages throughout the process

### Playlist Downloads
- **Video Progress**: Tracks progress through individual videos in the playlist
- **Overall Progress**: Shows completion percentage for the entire playlist
- **Current Video**: Displays which video is currently being downloaded
- **Success/Failure Count**: Tracks successful and failed downloads

### Progress Bar Components
- **Main Progress Bar**: Visual representation of overall download progress
- **Step Indicator**: Shows current operation with spinning icon
- **Speed Information**: Real-time download speed and ETA
- **Status Messages**: Live updates on what's happening

## Installation

1. **Install Dependencies**:
   ```bash
   cd web
   npm install
   ```

2. **Build the Project**:
   ```bash
   npm run build
   ```

3. **Development Mode**:
   ```bash
   npm run dev
   ```

## Usage

1. **Start the Backend**: Ensure the Flask backend is running on `http://localhost:5000`
2. **Open the Web UI**: Navigate to the web interface in your browser
3. **Enter YouTube URL**: Paste a YouTube video or playlist URL
4. **Configure Options**: Set audio quality, splitting options, and output directory
5. **Monitor Progress**: Watch the real-time progress bar during downloads
6. **View Results**: Check the downloads tab for completed files

## API Endpoints

The web UI communicates with the Flask backend through these endpoints:

- `POST /api/download` - Download single video with progress tracking
- `POST /api/playlist` - Download playlist with progress tracking
- `GET /api/progress/<download_id>` - Real-time progress updates (Server-Sent Events)
- `GET /api/downloads/status` - Get status of all active downloads
- `GET /api/downloads` - List completed downloads
- `GET /api/chapters/<url>` - Get video chapters
- `GET /api/formats/<url>` - Get available formats

## Progress Tracking Architecture

The progress tracking system uses Server-Sent Events (SSE) for real-time communication:

1. **Download Initiation**: User starts download, backend generates unique download ID
2. **Progress Hooks**: Custom progress hooks capture yt-dlp progress events
3. **Real-time Updates**: Progress data sent to frontend via SSE
4. **UI Updates**: Frontend updates progress bars and status in real-time
5. **Completion Handling**: Automatic cleanup and final status display

## Development

### Project Structure
```
web/
├── src/
│   ├── components/          # React-like components
│   │   ├── download-form.ts # Main download form with progress bar
│   │   ├── downloads-list.ts
│   │   └── ...
│   ├── services/            # API communication
│   │   └── api-service.ts   # HTTP client for backend
│   ├── styles.css           # Tailwind CSS styles
│   └── index.ts             # Main entry point
├── package.json
└── webpack.config.js
```

### Key Components

#### DownloadForm
- Handles form submission and validation
- Manages progress bar display and updates
- Establishes SSE connection for real-time progress
- Updates UI elements based on progress data

#### Progress Bar
- **Overall Progress**: Main download progress with percentage
- **Step Indicator**: Current operation with animated icon
- **Playlist Progress**: Video-by-video progress for playlists
- **Speed Info**: Download speed and ETA display

### Adding New Progress Features

To extend the progress tracking:

1. **Backend**: Add new progress hook calls in core functions
2. **Frontend**: Update progress bar component to handle new data
3. **API**: Ensure new progress data is sent via SSE

## Troubleshooting

### Progress Bar Not Showing
- Check browser console for JavaScript errors
- Verify backend is running and accessible
- Check SSE connection in Network tab

### Progress Updates Not Working
- Ensure download ID is properly generated
- Check progress hook integration in core functions
- Verify SSE endpoint is working

### Build Errors
- Run `npm install` to ensure all dependencies
- Check TypeScript compilation with `npm run build`
- Verify webpack configuration

## Browser Support

- **Chrome/Edge**: Full support for all features
- **Firefox**: Full support for all features
- **Safari**: Full support for all features
- **Mobile Browsers**: Responsive design with touch-friendly controls

## Performance

- **Lazy Loading**: Components load only when needed
- **Efficient Updates**: Minimal DOM manipulation during progress updates
- **Memory Management**: Automatic cleanup of completed downloads
- **Optimized Builds**: Production builds with tree shaking and minification
