"""
Shared utilities and global state for the YouTube Audio Extractor API
"""

import time
import queue
import uuid
from typing import Dict, Any, Callable
from .logging_utils import main_logger, log_download_progress, get_download_logger

# Global storage for download progress and queues
download_progress: Dict[str, Dict[str, Any]] = {}
download_queues: Dict[str, queue.Queue] = {}


def progress_hook(d: Dict[str, Any], download_id: str) -> None:
    """Progress hook for download progress that sends updates to the frontend."""
    logger = get_download_logger(download_id)

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
            logger.info("Download finished, processing audio...")

        try:
            download_queues[download_id].put(progress_data)
        except Exception as e:
            logger.error(f"Error sending progress data: {e}")
            pass  # Queue might be closed
    else:
        logger.warning(f"Download ID {download_id} not found in queues")


def create_progress_hook(download_id: str) -> Callable[[Dict[str, Any]], None]:
    """Create a progress hook function for a specific download."""
    return lambda d: progress_hook(d, download_id)


def generate_download_id() -> str:
    """Generate a unique download ID."""
    return str(uuid.uuid4())


def initialize_download(download_id: str, url: str, output_dir: str, download_type: str = 'single') -> None:
    """Initialize download progress tracking."""
    from .logging_utils import setup_download_logger

    # Set up logger for this download
    logger = setup_download_logger(download_id, url)

    download_queues[download_id] = queue.Queue()
    download_progress[download_id] = {
        'status': 'starting',
        'url': url,
        'output_dir': output_dir,
        'start_time': time.time(),
        'current_step': f'Initializing {"playlist " if download_type == "playlist" else ""}download...'
    }

    if download_type == 'playlist':
        download_progress[download_id]['type'] = 'playlist'

    logger.info(f"Download initialized - Type: {download_type}, Output: {output_dir}")
    main_logger.info(f"New download started: {download_id[:8]} - {url}")


def send_end_signal(download_id: str) -> None:
    """Send the final 'end' signal to close the SSE stream."""
    logger = get_download_logger(download_id)
    try:
        if download_id in download_queues:
            download_queues[download_id].put({
                'status': 'end',
                'message': 'Stream ended',
                'timestamp': time.time()
            })
        else:
            logger.warning("Cannot send end signal - download queue not found")
    except Exception as e:
        logger.error(f"Error sending 'end' status: {e}")
        pass
