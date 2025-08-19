#!/usr/bin/env python3
"""
Flask web application for YouTube Audio Extractor
Provides a REST API for the web UI
"""

import os
import json
import threading
import time
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from youtube_audio_extractor.core import download_audio, validate_youtube_url
from youtube_audio_extractor.playlists import download_playlist
from youtube_audio_extractor.chapters import get_video_chapters, has_chapters
from youtube_audio_extractor.formats import list_formats
import subprocess
import platform
import queue
import uuid
from queue import Empty

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Global storage for download progress
download_progress = {}
download_queues = {}

# Frontend is served by Webpack dev server in development
# No need to serve or redirect from Flask

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'YouTube Audio Extractor API is running'
    })

def progress_hook(d, download_id):
    """Progress hook for download progress that sends updates to the frontend."""
    if download_id in download_queues:
        progress_data = {
            'status': d['status'],
            'timestamp': time.time()
        }

        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                progress_data.update({
                    'downloaded_bytes': d['downloaded_bytes'],
                    'total_bytes': d['total_bytes'],
                    'percent': percent,
                    'speed': d.get('speed', 0),
                    'eta': d.get('eta', 0)
                })
            elif 'downloaded_bytes' in d:
                progress_data.update({
                    'downloaded_bytes': d['downloaded_bytes'],
                    'percent': 0
                })
        elif d['status'] == 'finished':
            progress_data.update({
                'percent': 100,
                'message': 'Download completed, processing audio...'
            })

        try:
            download_queues[download_id].put(progress_data)
        except:
            pass  # Queue might be closed

def create_progress_hook(download_id):
    """Create a progress hook function for a specific download."""
    return lambda d: progress_hook(d, download_id)

@app.route('/api/download', methods=['POST'])
def download_video():
    """Download audio from a single YouTube video"""
    try:
        data = request.get_json()
        url = data.get('url')
        output_dir = data.get('output_dir', 'downloads')
        bitrate = data.get('bitrate', '192')
        split_large_files = data.get('split_large_files', False)
        split_by_chapters = data.get('split_by_chapters', False)

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        if not validate_youtube_url(url):
            return jsonify({'error': 'Invalid YouTube URL'}), 400

        # Generate unique download ID
        download_id = str(uuid.uuid4())
        download_queues[download_id] = queue.Queue()
        download_progress[download_id] = {
            'status': 'starting',
            'url': url,
            'output_dir': output_dir,
            'start_time': time.time(),
            'current_step': 'Initializing download...'
        }

        # Start download in background thread
        def download_task():
            try:
                # Create custom progress hook for this download
                custom_progress_hook = create_progress_hook(download_id)

                # Update progress
                download_progress[download_id]['status'] = 'downloading'
                download_progress[download_id]['current_step'] = 'Starting download...'

                # Import here to avoid circular imports
                from youtube_audio_extractor.core import download_audio_with_progress

                # Use the modified download function with progress tracking
                success = download_audio_with_progress(
                    url=url,
                    output_dir=output_dir,
                    bitrate=bitrate,
                    split_large_files=split_large_files,
                    split_by_chapters=split_by_chapters,
                    progress_hook=custom_progress_hook,
                    download_id=download_id
                )

                if success:
                    download_progress[download_id]['status'] = 'completed'
                    download_progress[download_id]['current_step'] = 'Download completed successfully!'

                    # Send completion status to frontend
                    try:
                        if download_id in download_queues:
                            download_queues[download_id].put({
                                'status': 'completed',
                                'percent': 100,
                                'message': 'Download completed successfully!',
                                'timestamp': time.time()
                            })
                    except:
                        pass
                else:
                    download_progress[download_id]['status'] = 'failed'
                    download_progress[download_id]['current_step'] = 'Download failed - video may be restricted or unavailable'

                    # Send failure status to frontend
                    try:
                        if download_id in download_queues:
                            download_queues[download_id].put({
                                'status': 'failed',
                                'message': 'Download failed - video may be restricted or unavailable',
                                'timestamp': time.time()
                            })
                    except:
                        pass

            except Exception as e:
                download_progress[download_id]['status'] = 'failed'
                download_progress[download_id]['current_step'] = f'Error: {str(e)}'
                print(f"Download error: {e}")

                # Send error message to progress queue
                try:
                    if download_id in download_queues:
                        download_queues[download_id].put({
                            'status': 'error',
                            'message': f'Download failed: {str(e)}',
                            'timestamp': time.time()
                        })
                except:
                    pass
            finally:
                # Clean up after a delay
                def cleanup():
                    time.sleep(30)  # Keep progress data for 30 seconds
                    if download_id in download_progress:
                        del download_progress[download_id]
                    if download_id in download_queues:
                        del download_queues[download_id]

                cleanup_thread = threading.Thread(target=cleanup)
                cleanup_thread.daemon = True
                cleanup_thread.start()

        thread = threading.Thread(target=download_task)
        thread.daemon = True
        thread.start()

        return jsonify({
            'message': 'Download started successfully',
            'download_id': download_id,
            'url': url,
            'output_dir': output_dir
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/playlist', methods=['POST'])
def download_playlist_endpoint():
    """Download audio from a YouTube playlist"""
    try:
        data = request.get_json()
        url = data.get('url')
        output_dir = data.get('output_dir', 'downloads')
        bitrate = data.get('bitrate', '192')
        split_large_files = data.get('split_large_files', False)
        split_by_chapters = data.get('split_by_chapters', False)
        start_index = data.get('start_index', 1)
        end_index = data.get('end_index')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        if not validate_youtube_url(url):
            return jsonify({'error': 'Invalid YouTube URL'}), 400

        # Generate unique download ID
        download_id = str(uuid.uuid4())
        download_queues[download_id] = queue.Queue()
        download_progress[download_id] = {
            'status': 'starting',
            'url': url,
            'output_dir': output_dir,
            'start_time': time.time(),
            'current_step': 'Initializing playlist download...',
            'type': 'playlist'
        }

        # Start download in background thread
        def download_task():
            try:
                # Update progress
                download_progress[download_id]['status'] = 'downloading'
                download_progress[download_id]['current_step'] = 'Starting playlist download...'

                # Import here to avoid circular imports
                from youtube_audio_extractor.playlists import download_playlist_with_progress

                # Use the modified playlist download function with progress tracking
                success = download_playlist_with_progress(
                    url=url,
                    output_dir=output_dir,
                    bitrate=bitrate,
                    split_large_files=split_large_files,
                    split_by_chapters=split_by_chapters,
                    start_index=start_index,
                    end_index=end_index,
                    progress_hook=create_progress_hook(download_id),
                    download_id=download_id
                )

                if success:
                    download_progress[download_id]['status'] = 'completed'
                    download_progress[download_id]['current_step'] = 'Playlist download completed successfully!'
                else:
                    download_progress[download_id]['status'] = 'failed'
                    download_progress[download_id]['current_step'] = 'Playlist download failed'

            except Exception as e:
                download_progress[download_id]['status'] = 'failed'
                download_progress[download_id]['current_step'] = f'Error: {str(e)}'
                print(f"Playlist download error: {e}")
            finally:
                # Clean up after a delay
                def cleanup():
                    time.sleep(30)  # Keep progress data for 30 seconds
                    if download_id in download_progress:
                        del download_progress[download_id]
                    if download_id in download_queues:
                        del download_queues[download_id]

                cleanup_thread = threading.Thread(target=cleanup)
                cleanup_thread.daemon = True
                cleanup_thread.start()

        thread = threading.Thread(target=download_task)
        thread.daemon = True
        thread.start()

        return jsonify({
            'message': 'Playlist download started successfully',
            'download_id': download_id,
            'url': url,
            'output_dir': output_dir
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress/<download_id>', methods=['OPTIONS'])
def progress_options(download_id):
    """Handle preflight OPTIONS request for progress endpoint"""
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Max-Age'] = '86400'
    return response

@app.route('/api/progress/<download_id>')
def get_progress(download_id):
    """Get download progress via Server-Sent Events"""
    def generate():
        if download_id not in download_queues:
            yield f"data: {json.dumps({'error': 'Download not found'})}\n\n"
            return

        queue = download_queues[download_id]

        # Send initial progress
        if download_id in download_progress:
            yield f"data: {json.dumps(download_progress[download_id])}\n\n"

        try:
            while True:
                try:
                    # Get progress update with timeout
                    progress_data = queue.get(timeout=1)
                    yield f"data: {json.dumps(progress_data)}\n\n"

                    # If download is completed or failed, send final update and close
                    if progress_data.get('status') in ['completed', 'failed']:
                        yield f"data: {json.dumps(download_progress.get(download_id, {}))}\n\n"
                        break

                except Empty:
                    # Send heartbeat to keep connection alive
                    yield f"data: {json.dumps({'heartbeat': time.time()})}\n\n"

        except GeneratorExit:
            # Client disconnected
            pass
        finally:
            # Clean up
            if download_id in download_queues:
                del download_queues[download_id]

    response = Response(generate(), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/downloads/status')
def get_downloads_status():
    """Get status of all active downloads"""
    return jsonify({
        'downloads': download_progress
    })

@app.route('/api/chapters/<path:url>')
def get_chapters(url):
    """Get video chapters for a YouTube URL"""
    try:
        if not validate_youtube_url(url):
            return jsonify({'error': 'Invalid YouTube URL'}), 400

        chapters = get_video_chapters(url)
        has_chapters_info = has_chapters(url)

        return jsonify({
            'chapters': chapters,
            'has_chapters': has_chapters_info
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/formats/<path:url>')
def get_formats(url):
    """Get available formats for a YouTube URL"""
    try:
        if not validate_youtube_url(url):
            return jsonify({'error': 'Invalid YouTube URL'}), 400

        formats = list_formats(url)

        return jsonify({
            'formats': formats
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/downloads')
def list_downloads():
    """List all downloaded files and folders"""
    try:
        downloads_dir = Path('downloads')
        if not downloads_dir.exists():
            return jsonify({'downloads': []})

        downloads = []

        for item in downloads_dir.iterdir():
            if item.is_file() and item.suffix.lower() == '.mp3':
                # MP3 file
                downloads.append({
                    'name': item.name,
                    'type': 'file',
                    'size': item.stat().st_size,
                    'modified': item.stat().st_mtime
                })
            elif item.is_dir():
                # Folder - count MP3 files inside
                mp3_count = len(list(item.glob('*.mp3')))
                downloads.append({
                    'name': item.name,
                    'type': 'folder',
                    'mp3_count': mp3_count,
                    'modified': item.stat().st_mtime
                })

        # Sort by modification time (newest first)
        downloads.sort(key=lambda x: x['modified'], reverse=True)

        return jsonify({'downloads': downloads})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bitrates')
def get_bitrates():
    """Get available bitrate options"""
    return jsonify({
        'bitrates': [
            {'value': '32', 'label': '32 kbps - Very Low (Podcasts, voice)'},
            {'value': '64', 'label': '64 kbps - Low (Basic audio)'},
            {'value': '96', 'label': '96 kbps - Fair (Good balance)'},
            {'value': '128', 'label': '128 kbps - Good (Music, general use)'},
            {'value': '160', 'label': '160 kbps - Better (High-quality music)'},
            {'value': '192', 'label': '192 kbps - High (Default - Best balance)'},
            {'value': '256', 'label': '256 kbps - Very High (Lossless-like)'},
            {'value': '320', 'label': '320 kbps - Maximum (Studio quality)'}
        ]
    })

@app.route('/api/open-folder', methods=['POST'])
def open_folder():
    """Open file browser at specified location"""
    try:
        data = request.get_json()
        folder_path = data.get('path')

        if not folder_path:
            return jsonify({'error': 'Path is required'}), 400

        # Ensure the path is within the downloads directory for security
        downloads_dir = Path('downloads').resolve()
        target_path = Path(folder_path).resolve()

        if not target_path.is_relative_to(downloads_dir):
            return jsonify({'error': 'Access denied: Path outside downloads directory'}), 403

        # Open file browser based on platform
        system = platform.system().lower()

        try:
            if system == 'darwin':  # macOS
                subprocess.run(['open', str(target_path)], check=True)
            elif system == 'windows':
                subprocess.run(['explorer', str(target_path)], check=True)
            else:  # Linux and others
                # Try common file managers
                file_managers = ['xdg-open', 'nautilus', 'dolphin', 'thunar', 'pcmanfm']
                for manager in file_managers:
                    try:
                        subprocess.run([manager, str(target_path)], check=True)
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
                else:
                    # Fallback to xdg-open which should work on most Linux systems
                    subprocess.run(['xdg-open', str(target_path)], check=True)

            return jsonify({
                'message': 'File browser opened successfully',
                'path': str(target_path)
            })

        except subprocess.CalledProcessError as e:
            return jsonify({'error': f'Failed to open file browser: {str(e)}'}), 500
        except FileNotFoundError:
            return jsonify({'error': 'No suitable file browser found'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
