"""
Download endpoints for single videos and playlists
"""

import threading
import time
from flask import Blueprint, request, jsonify
from youtube_audio_extractor.core import validate_youtube_url
from .shared import (
    download_progress, download_queues, create_progress_hook,
    generate_download_id, initialize_download, send_end_signal
)
from .logging_utils import main_logger, get_download_logger, cleanup_download_logger, log_download_error

downloads_bp = Blueprint('downloads', __name__)


def create_cleanup_thread(download_id: str) -> None:
    """Create a cleanup thread to remove download data after a delay."""
    def cleanup():
        time.sleep(30)  # Keep progress data for 30 seconds

        if download_id in download_progress:
            del download_progress[download_id]
        if download_id in download_queues:
            del download_queues[download_id]

        cleanup_download_logger(download_id)

    cleanup_thread = threading.Thread(target=cleanup)
    cleanup_thread.daemon = True
    cleanup_thread.start()


@downloads_bp.route('/api/download', methods=['POST'])
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

        # Generate unique download ID and initialize
        download_id = generate_download_id()
        main_logger.info(f"=== NEW SINGLE VIDEO DOWNLOAD ===")
        main_logger.info(f"Download ID: {download_id}")
        main_logger.info(f"URL: {url}")
        main_logger.info(f"Output dir: {output_dir}")
        main_logger.info(f"Bitrate: {bitrate}")
        main_logger.info(f"Split large files: {split_large_files}")
        main_logger.info(f"Split by chapters: {split_by_chapters}")

        initialize_download(download_id, url, output_dir, 'single')

                # Start download in background thread
        logger = get_download_logger(download_id)

        def download_task():
            logger = get_download_logger(download_id)
            try:
                # Create custom progress hook for this download
                custom_progress_hook = create_progress_hook(download_id)

                # Update progress
                download_progress[download_id]['status'] = 'downloading'
                download_progress[download_id]['current_step'] = 'Starting download...'

                # Import here to avoid circular imports
                try:
                    from youtube_audio_extractor.core import download_audio_with_progress
                except ImportError as e:
                    log_download_error(download_id, e, "Failed to import core module")
                    raise

                # Use the modified download function with progress tracking
                try:
                    success = download_audio_with_progress(
                        url=url,
                        output_dir=output_dir,
                        bitrate=bitrate,
                        split_large_files=split_large_files,
                        split_by_chapters=split_by_chapters,
                        progress_hook=custom_progress_hook,
                        download_id=download_id
                    )
                except Exception as e:
                    log_download_error(download_id, e, "Error during download_audio_with_progress")
                    raise

                if success:
                    download_progress[download_id]['status'] = 'completed'
                    download_progress[download_id]['current_step'] = 'Download completed successfully!'
                    send_end_signal(download_id)
                else:
                    download_progress[download_id]['status'] = 'failed'
                    download_progress[download_id]['current_step'] = 'Download failed - video may be restricted or unavailable'
                    send_end_signal(download_id)

            except Exception as e:
                download_progress[download_id]['status'] = 'failed'
                download_progress[download_id]['current_step'] = f'Error: {str(e)}'
                log_download_error(download_id, e, "Download task failed")
                send_end_signal(download_id)
            finally:
                create_cleanup_thread(download_id)

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


@downloads_bp.route('/api/playlist', methods=['POST'])
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

        # Generate unique download ID and initialize
        download_id = generate_download_id()
        main_logger.info(f"=== NEW PLAYLIST DOWNLOAD ===")
        main_logger.info(f"Download ID: {download_id}")
        main_logger.info(f"URL: {url}")
        main_logger.info(f"Start index: {start_index}, End index: {end_index}")

        initialize_download(download_id, url, output_dir, 'playlist')

        # Start download in background thread
        def download_task():
            logger = get_download_logger(download_id)
            try:

                # Update progress
                download_progress[download_id]['status'] = 'downloading'
                download_progress[download_id]['current_step'] = 'Starting playlist download...'

                # Import here to avoid circular imports
                try:
                    from youtube_audio_extractor.playlists import download_playlist_with_progress
                except ImportError as e:
                    log_download_error(download_id, e, "Failed to import playlist module")
                    raise

                # Use the modified playlist download function with progress tracking
                try:
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
                except Exception as e:
                    log_download_error(download_id, e, "Error during playlist download")
                    raise

                if success:
                    download_progress[download_id]['status'] = 'completed'
                    download_progress[download_id]['current_step'] = 'Playlist download completed successfully!'
                    send_end_signal(download_id)
                else:
                    download_progress[download_id]['status'] = 'failed'
                    download_progress[download_id]['current_step'] = 'Playlist download failed'
                    send_end_signal(download_id)

            except Exception as e:
                download_progress[download_id]['status'] = 'failed'
                download_progress[download_id]['current_step'] = f'Error: {str(e)}'
                log_download_error(download_id, e, "Playlist download task failed")
                send_end_signal(download_id)
            finally:
                create_cleanup_thread(download_id)

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
