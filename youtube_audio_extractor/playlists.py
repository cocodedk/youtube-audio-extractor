"""
Playlist functionality for YouTube Audio Extractor.
Handles downloading entire playlists with optional chapter splitting.
"""

import os
import click
import yt_dlp
from pathlib import Path
from urllib.parse import urlparse
from .core import validate_youtube_url
from .chapters import has_chapters, get_video_chapters, split_audio_by_chapters
from .splitting import split_audio_file


def validate_playlist_url(url):
    """Validate if the URL is a valid YouTube URL that can contain multiple videos."""
    if not validate_youtube_url(url):
        return False

    # Check if it's a playlist URL, channel URL, or search URL
    parsed = urlparse(url)
    return ('playlist' in parsed.query or 'list=' in parsed.query or
            'channel' in parsed.path or 'c/' in parsed.path or
            'user/' in parsed.path or 'search_query' in parsed.query)


def get_playlist_info(url):
    """Get information about a YouTube playlist, channel, or search results."""
    if not validate_playlist_url(url):
        click.echo("❌ Invalid YouTube URL provided!")
        return None, None

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # Don't download, just get info
        'playlist_items': '1-50',  # Limit to first 50 items for testing
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if not info:
                click.echo("❌ Could not extract information from URL")
                return None, None

            # Handle different types of URLs
            if 'entries' in info and info['entries']:
                # This is a playlist, channel, or search result
                title = info.get('title', 'Unknown Collection')
                entries = info.get('entries', [])

                if not entries:
                    click.echo("❌ No videos found")
                    return None, None

                # Filter out None entries (failed extractions)
                valid_entries = [entry for entry in entries if entry is not None]

                if not valid_entries:
                    click.echo("❌ No valid videos found")
                    return None, None

                click.echo(f"📚 Collection: {title}")
                click.echo(f"🎬 Videos found: {len(valid_entries)}")

                return title, valid_entries
            else:
                # Single video
                click.echo("❌ This appears to be a single video, not a collection")
                return None, None

    except Exception as e:
        click.echo(f"❌ Error extracting information: {e}")
        return None, None


def download_playlist(url, output_dir="downloads", quality="best", bitrate="192",
                      split_large_files=False, split_by_chapters=False,
                      start_index=1, end_index=None):
    """Download entire YouTube playlist, channel, or search results."""
    if not validate_playlist_url(url):
        click.echo("❌ Invalid YouTube URL provided!")
        return False

    # Get playlist information
    playlist_title, entries = get_playlist_info(url)
    if not playlist_title or not entries:
        return False

    # Ensure output directory is always within the downloads folder
    if output_dir == "downloads":
        final_output_dir = "downloads"
    else:
        # Create a clean subfolder name and place it in downloads/
        clean_dir_name = clean_directory_name(output_dir)
        final_output_dir = Path("downloads") / clean_dir_name

    # Create playlist output directory within the downloads folder
    playlist_dir = Path(final_output_dir) / clean_filename(playlist_title)
    playlist_dir.mkdir(parents=True, exist_ok=True)

    click.echo(f"📁 Output directory: {playlist_dir}")
    click.echo(f"🎚️  Audio quality: {bitrate} kbps")

    if split_large_files:
        click.echo(f"✂️  Large file splitting: Enabled (max 16MB per chunk)")

    if split_by_chapters:
        click.echo(f"📚  Chapter-based splitting: Enabled")

    # Determine range of videos to download
    total_videos = len(entries)
    start_idx = max(1, start_index) - 1  # Convert to 0-based index
    end_idx = min(total_videos, end_index) if end_index else total_videos

    videos_to_download = entries[start_idx:end_idx]
    click.echo(f"🎯 Downloading videos {start_idx + 1} to {end_idx} of {total_videos}")

    # Download each video in the playlist
    successful_downloads = 0
    failed_downloads = 0

    for i, entry in enumerate(videos_to_download, start=start_idx + 1):
        video_url = entry.get('url')
        video_title = entry.get('title', f'Video {i}')

        if not video_url:
            click.echo(f"❌ Skipping video {i}: No URL available")
            failed_downloads += 1
            continue

        click.echo(f"\n🎵 [{i}/{end_idx}] Downloading: {video_title}")

        # Create video-specific output directory
        video_dir = playlist_dir / f"{i:02d}_{clean_filename(video_title)}"
        video_dir.mkdir(exist_ok=True)

        # Download the video
        if download_playlist_video(video_url, str(video_dir), quality, bitrate,
                                  split_large_files, split_by_chapters):
            successful_downloads += 1
            click.echo(f"✅ [{i}/{end_idx}] Successfully downloaded: {video_title}")
        else:
            failed_downloads += 1
            click.echo(f"❌ [{i}/{end_idx}] Failed to download: {video_title}")

    # Summary
    click.echo(f"\n🎯 Download completed!")
    click.echo(f"✅ Successful: {successful_downloads}")
    click.echo(f"❌ Failed: {failed_downloads}")
    click.echo(f"📁 All files saved to: {playlist_dir}")

    return successful_downloads > 0


def download_playlist_video(url, output_dir, quality, bitrate, split_large_files, split_by_chapters):
    """Download a single video from a playlist."""
    try:
        # Configure yt-dlp options for this video
        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'format': f'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio' if quality == "best" else quality,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate,
            }],
            'quiet': True,  # Less verbose for playlist downloads
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find the downloaded MP3 file
        mp3_files = list(Path(output_dir).glob("*.mp3"))
        if not mp3_files:
            return False

        downloaded_file = mp3_files[-1]  # Get the most recent MP3 file
        file_size_mb = downloaded_file.stat().st_size / (1024 * 1024)

        # Handle chapter-based splitting first (if requested)
        if split_by_chapters:
            chapters, _ = get_video_chapters(url)
            if chapters:
                if split_audio_by_chapters(str(downloaded_file), output_dir, chapters, bitrate):
                    # Remove original file after successful chapter splitting
                    downloaded_file.unlink()
                else:
                    click.echo(f"⚠️  Chapter splitting failed for video")
            else:
                click.echo(f"ℹ️  No chapters found, keeping original file")

        # Handle size-based splitting (if requested and not already handled by chapters)
        elif split_large_files and file_size_mb > 16:
            if split_audio_file(str(downloaded_file), output_dir, 16, bitrate):
                # Remove original file after successful splitting
                downloaded_file.unlink()
            else:
                click.echo(f"⚠️  File splitting failed for video")

        return True

    except Exception as e:
        click.echo(f"❌ Error downloading video: {e}")
        return False


def clean_filename(filename):
    """Clean filename for safe file system usage."""
    import re

    # Remove or replace problematic characters
    clean = re.sub(r'[<>:"/\\|?*]', '_', filename)
    clean = re.sub(r'\s+', ' ', clean)  # Replace multiple spaces with single space
    clean = clean.strip()

    # Limit length to avoid extremely long filenames
    if len(clean) > 100:
        clean = clean[:97] + "..."

    return clean


def clean_directory_name(name):
    """Clean directory name for safe file system usage."""
    import re

    # Remove or replace problematic characters
    clean = re.sub(r'[<>:"/\\|?*]', '_', name)
    clean = re.sub(r'\s+', ' ', clean)  # Replace multiple spaces with single space
    clean = clean.strip()

    # Limit length to avoid extremely long directory names
    if len(clean) > 50:
        clean = clean[:47] + "..."

    return clean


def list_playlist_videos(url):
    """List all videos in a YouTube playlist, channel, or search results."""
    playlist_title, entries = get_playlist_info(url)

    if not playlist_title or not entries:
        return

    click.echo(f"\n📚 Collection: {playlist_title}")
    click.echo(f"🎬 Total Videos: {len(entries)}")
    click.echo("\n📺 Video List:")
    click.echo("-" * 80)

    for i, entry in enumerate(entries, 1):
        title = entry.get('title', f'Unknown Title {i}')
        duration = entry.get('duration', 'Unknown')

        # Handle duration formatting
        if duration != 'Unknown' and duration is not None:
            try:
                duration_int = int(duration)
                duration_str = f"{duration_int//60:02d}:{duration_int%60:02d}"
            except (ValueError, TypeError):
                duration_str = 'Unknown'
        else:
            duration_str = 'Unknown'

        click.echo(f"{i:3d}. {title}")
        click.echo(f"     Duration: {duration_str}")

        # Check if video has chapters
        video_url = entry.get('url')
        if video_url and has_chapters(video_url):
            click.echo(f"     📚 Has chapters")
        click.echo()
