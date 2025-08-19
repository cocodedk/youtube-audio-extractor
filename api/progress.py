"""
Progress tracking and Server-Sent Events endpoints
"""

import json
import time
from flask import Blueprint, Response
from queue import Empty
from .shared import download_progress, download_queues
from .logging_utils import main_logger

progress_bp = Blueprint('progress', __name__)


@progress_bp.route('/api/progress/<download_id>', methods=['OPTIONS'])
def progress_options(download_id):
    """Handle preflight OPTIONS request for progress endpoint"""
    response = Response()
    # Let Flask-CORS handle CORS headers instead of hardcoding them
    return response


@progress_bp.route('/api/progress/<download_id>')
def get_progress(download_id):
    """Get download progress via Server-Sent Events"""
    main_logger.info(f"SSE connection requested for download: {download_id[:8]}")

    def generate():
        if download_id not in download_queues:
            main_logger.warning(f"SSE request for unknown download: {download_id[:8]}")
            yield f"data: {json.dumps({'error': 'Download not found'})}\n\n"
            return

        queue = download_queues[download_id]

        # Send initial progress
        if download_id in download_progress:
            initial_data = download_progress[download_id]
            yield f"data: {json.dumps(initial_data)}\n\n"

        try:
            while True:
                try:
                    # Get progress update with timeout
                    progress_data = queue.get(timeout=1)
                    yield f"data: {json.dumps(progress_data)}\n\n"

                    # Log significant progress events
                    status = progress_data.get('status')
                    if status in ['completed', 'failed', 'error']:
                        main_logger.info(f"Download {download_id[:8]} status: {status}")
                    elif status == 'end':
                        main_logger.info(f"SSE stream ended for download: {download_id[:8]}")

                    # If download is completed, failed, or ended, send final update and close
                    if status in ['completed', 'failed', 'end']:
                        if status != 'end':  # Don't duplicate the end message
                            final_data = download_progress.get(download_id, {})
                            yield f"data: {json.dumps(final_data)}\n\n"
                        break

                except Empty:
                    # Send heartbeat to keep connection alive
                    yield f"data: {json.dumps({'heartbeat': time.time()})}\n\n"

        except GeneratorExit:
            # Client disconnected
            pass
        finally:
            # Don't delete the queue here - let the download task handle cleanup
            # This prevents race conditions where the queue is deleted before "end" status is sent
            pass

    response = Response(generate(), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    # Let Flask-CORS handle CORS headers instead of hardcoding them
    return response


@progress_bp.route('/api/downloads/status')
def get_downloads_status():
    """Get status of all active downloads"""
    from flask import jsonify
    return jsonify({
        'downloads': download_progress
    })
