"""
Utility endpoints for health checks, file listings, and system operations
"""

import os
import subprocess
import platform
from pathlib import Path
from flask import Blueprint, jsonify, request, Response
from youtube_audio_extractor.core import validate_youtube_url
from youtube_audio_extractor.chapters import get_video_chapters, has_chapters
from youtube_audio_extractor.formats import list_formats
from .shared import download_progress
from .logging_utils import main_logger

utils_bp = Blueprint('utils', __name__)


@utils_bp.route('/api/health')
def health():
    """Health check endpoint"""
    main_logger.debug("Health check requested")
    return jsonify({
        'status': 'healthy',
        'message': 'YouTube Audio Extractor API is running'
    })


@utils_bp.route('/api/downloads/<download_id>/location', methods=['GET', 'OPTIONS'])
def get_download_location(download_id):
    """Get the location and file information for a completed download"""
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = Response()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        return response

    main_logger.info(f"Download location requested for: {download_id[:8]}")

    try:
        if download_id not in download_progress:
            main_logger.warning(f"Location request for unknown download: {download_id[:8]}")
            return jsonify({'error': 'Download not found'}), 404

        download_info = download_progress[download_id]

        if download_info['status'] != 'completed':
            main_logger.warning(f"Location request for incomplete download: {download_id[:8]} (status: {download_info['status']})")
            return jsonify({'error': 'Download not completed yet'}), 400

        # Get the downloads directory path
        downloads_dir = os.path.abspath('downloads')

        # Find the most recent MP3 file in the downloads directory
        mp3_files = list(Path(downloads_dir).glob("*.mp3"))
        if not mp3_files:
            main_logger.error(f"No MP3 files found for download: {download_id[:8]}")
            return jsonify({'error': 'No MP3 files found'}), 404

        # Get the most recent MP3 file
        latest_file = max(mp3_files, key=lambda f: f.stat().st_mtime)
        main_logger.info(f"Found download file: {latest_file.name} ({latest_file.stat().st_size} bytes)")

        response = jsonify({
            'downloads_dir': downloads_dir,
            'file_path': str(latest_file),
            'file_name': latest_file.name,
            'file_size': latest_file.stat().st_size,
            'file_size_mb': round(latest_file.stat().st_size / (1024 * 1024), 2)
        })

        # Add CORS headers
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        return response

    except Exception as e:
        main_logger.error(f"Error getting download location for {download_id[:8]}: {e}")
        return jsonify({'error': f'Error getting download location: {str(e)}'}), 500


@utils_bp.route('/api/chapters/<path:url>')
def get_chapters(url):
    """Get video chapters for a YouTube URL"""
    main_logger.info(f"Chapters requested for URL: {url}")
    try:
        if not validate_youtube_url(url):
            main_logger.warning(f"Invalid URL for chapters request: {url}")
            return jsonify({'error': 'Invalid YouTube URL'}), 400

        chapters = get_video_chapters(url)
        has_chapters_info = has_chapters(url)

        main_logger.info(f"Found {len(chapters) if chapters else 0} chapters for video")

        return jsonify({
            'chapters': chapters,
            'has_chapters': has_chapters_info
        })

    except Exception as e:
        main_logger.error(f"Error getting chapters for {url}: {e}")
        return jsonify({'error': str(e)}), 500


@utils_bp.route('/api/formats/<path:url>')
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


@utils_bp.route('/api/downloads')
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


@utils_bp.route('/api/bitrates')
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


@utils_bp.route('/api/open-folder', methods=['POST'])
def open_folder():
    """Open file browser at specified location"""
    try:
        data = request.get_json()
        folder_path = data.get('path')

        if not folder_path:
            main_logger.warning("Open folder request without path")
            return jsonify({'error': 'Path is required'}), 400

        main_logger.info(f"Open folder request for: {folder_path}")

        # Ensure the path is within the downloads directory for security
        downloads_dir = Path('downloads').resolve()
        target_path = Path(folder_path).resolve()

        if not target_path.is_relative_to(downloads_dir):
            main_logger.warning(f"Security violation: Path outside downloads directory: {folder_path}")
            return jsonify({'error': 'Access denied: Path outside downloads directory'}), 403

        # Open file browser based on platform
        system = platform.system().lower()
        main_logger.debug(f"Opening folder on {system} system: {target_path}")

        try:
            if system == 'darwin':  # macOS
                subprocess.run(['open', str(target_path)], check=True)
                main_logger.info(f"Opened folder with macOS Finder: {target_path}")
            elif system == 'windows':
                subprocess.run(['explorer', str(target_path)], check=True)
                main_logger.info(f"Opened folder with Windows Explorer: {target_path}")
            else:  # Linux and others
                # Try common file managers
                file_managers = ['xdg-open', 'nautilus', 'dolphin', 'thunar', 'pcmanfm']
                for manager in file_managers:
                    try:
                        subprocess.run([manager, str(target_path)], check=True)
                        main_logger.info(f"Opened folder with {manager}: {target_path}")
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
                else:
                    # Fallback to xdg-open which should work on most Linux systems
                    subprocess.run(['xdg-open', str(target_path)], check=True)
                    main_logger.info(f"Opened folder with xdg-open: {target_path}")

            return jsonify({
                'message': 'File browser opened successfully',
                'path': str(target_path)
            })

        except subprocess.CalledProcessError as e:
            main_logger.error(f"Failed to open file browser: {e}")
            return jsonify({'error': f'Failed to open file browser: {str(e)}'}), 500
        except FileNotFoundError:
            main_logger.error("No suitable file browser found")
            return jsonify({'error': 'No suitable file browser found'}), 500

    except Exception as e:
        main_logger.error(f"Error in open_folder: {e}")
        return jsonify({'error': str(e)}), 500
