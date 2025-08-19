"""
Format handling for YouTube Audio Extractor.
Contains functions for listing and managing audio formats.
"""

import click
import yt_dlp


def get_audio_formats(ydl_opts, url):
    """Get available audio formats for the video."""
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

            # Filter audio-only formats
            audio_formats = []
            for fmt in formats:
                if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                    audio_formats.append(fmt)

            return audio_formats, info
    except Exception as e:
        click.echo(f"Error extracting video info: {e}")
        return None, None


def list_formats(url):
    """List available audio formats for the video."""
    from .core import validate_youtube_url

    if not validate_youtube_url(url):
        click.echo("❌ Invalid YouTube URL provided!")
        return

    ydl_opts = {'quiet': True}
    audio_formats, info = get_audio_formats(ydl_opts, url)

    if not audio_formats:
        click.echo("❌ No audio formats found!")
        return

    click.echo(f"\n📺 Video: {info.get('title', 'Unknown')}")
    click.echo(f"⏱️  Duration: {info.get('duration', 'Unknown')} seconds")
    click.echo(f"👁️  Views: {info.get('view_count', 'Unknown')}")
    click.echo("\n🎵 Available Audio Formats:")
    click.echo("-" * 80)

    for fmt in audio_formats:
        format_id = fmt.get('format_id', 'N/A')
        ext = fmt.get('ext', 'N/A')
        filesize = fmt.get('filesize', 'N/A')
        if filesize != 'N/A':
            filesize = f"{filesize / 1024 / 1024:.1f} MB"

        click.echo(f"ID: {format_id:>5} | Format: {ext:>4} | Size: {filesize:>8}")
