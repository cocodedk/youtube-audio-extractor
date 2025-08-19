"""
Logging utilities for YouTube Audio Extractor
Provides centralized logging configuration and per-download loggers
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict


# Global logger cache to avoid creating duplicate loggers
_loggers: Dict[str, logging.Logger] = {}


def setup_main_logger() -> logging.Logger:
    """Set up the main application logger."""
    logger = logging.getLogger('yt_audio_extractor')

    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(logging.INFO)

    # Create logs directory if it doesn't exist
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler for main application log
    main_log_file = logs_dir / 'app.log'
    file_handler = logging.FileHandler(main_log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def setup_download_logger(download_id: str, url: str = None) -> logging.Logger:
    """Set up a logger for a specific download."""
    logger_name = f'download_{download_id}'

    # Return existing logger if already created
    if logger_name in _loggers:
        return _loggers[logger_name]

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Create logs directory if it doesn't exist
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)

    # Create formatter with download ID
    formatter = logging.Formatter(
        f'%(asctime)s - {download_id[:8]} - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create log file with timestamp and download ID
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'download_{timestamp}_{download_id[:8]}.log'
    log_file = logs_dir / log_filename

    # File handler for this specific download
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Cache the logger
    _loggers[logger_name] = logger

    # Log initial information
    logger.info(f"Download started - ID: {download_id}")
    if url:
        logger.info(f"URL: {url}")
    logger.info(f"Log file: {log_file}")

    return logger


def get_download_logger(download_id: str) -> logging.Logger:
    """Get an existing download logger."""
    logger_name = f'download_{download_id}'
    return _loggers.get(logger_name, setup_main_logger())


def cleanup_download_logger(download_id: str):
    """Clean up a download logger after completion."""
    logger_name = f'download_{download_id}'
    if logger_name in _loggers:
        logger = _loggers[logger_name]
        logger.info("Download completed - cleaning up logger")

        # Close all handlers
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

        # Remove from cache
        del _loggers[logger_name]


def log_download_progress(download_id: str, message: str, level: str = 'info'):
    """Log a progress message for a specific download."""
    logger = get_download_logger(download_id)

    if level.lower() == 'debug':
        logger.debug(message)
    elif level.lower() == 'warning':
        logger.warning(message)
    elif level.lower() == 'error':
        logger.error(message)
    else:
        logger.info(message)


def log_download_error(download_id: str, error: Exception, context: str = None):
    """Log an error for a specific download."""
    logger = get_download_logger(download_id)

    if context:
        logger.error(f"{context}: {str(error)}")
    else:
        logger.error(f"Error: {str(error)}")

    # Log the full traceback at debug level
    logger.debug(f"Full traceback:", exc_info=True)


# Initialize main logger when module is imported
main_logger = setup_main_logger()
