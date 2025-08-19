"""
YouTube Audio Extractor Package

A comprehensive tool for downloading audio from YouTube videos and playlists
with support for bitrate control, file splitting, and chapter-based splitting.
"""

from .core import download_audio, validate_youtube_url
from .formats import list_formats, get_audio_formats
from .splitting import split_audio_file
from .chapters import get_video_chapters, split_audio_by_chapters, list_chapters, has_chapters
from .playlists import download_playlist, list_playlist_videos, validate_playlist_url
from .cli import cli

__version__ = "1.0.0"
__author__ = "YouTube Audio Extractor"

__all__ = [
    'download_audio', 'validate_youtube_url', 'list_formats', 'get_audio_formats',
    'split_audio_file', 'get_video_chapters', 'split_audio_by_chapters',
    'list_chapters', 'has_chapters', 'download_playlist', 'list_playlist_videos',
    'validate_playlist_url', 'cli'
]
