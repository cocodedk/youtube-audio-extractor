"""
Core functionality for YouTube Audio Extractor.
Contains main download logic and URL validation.
"""

import os
import click
import yt_dlp
from pathlib import Path
from urllib.parse import urlparse
from .splitting import split_audio_file
from .chapters import get_video_chapters, split_audio_by_chapters, has_chapters


def validate_youtube_url(url):
    """Validate if the URL is a valid YouTube URL."""
    youtube_domains = ['youtube.com', 'www.youtube.com', 'youtu.be', 'www.youtu.be']
    parsed = urlparse(url)

    if not parsed.netloc:
        return False

    # Remove 'www.' prefix for comparison
    domain = parsed.netloc.replace('www.', '')

    if domain not in youtube_domains:
        return False

    return True


def progress_hook(d):
    """Progress hook for download progress."""
    if d['status'] == 'downloading':
        if 'total_bytes' in d and d['total_bytes']:
            percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
            click.echo(f"\r📥 Downloading... {percent:.1f}%", nl=False)
        elif 'downloaded_bytes' in d:
            click.echo(f"\r📥 Downloaded: {d['downloaded_bytes']} bytes", nl=False)
    elif d['status'] == 'finished':
        click.echo("\n🔄 Processing audio...")


def download_audio(url, output_dir="downloads", format_id=None, quality="best", bitrate="192", split_large_files=False, split_by_chapters=False):
    """Download audio from YouTube video."""
    if not validate_youtube_url(url):
        click.echo("❌ Invalid YouTube URL provided!")
        return False

    # Ensure output directory is always within the downloads folder
    if output_dir == "downloads":
        final_output_dir = "downloads"
    else:
        # Create a clean subfolder name and place it in downloads/
        clean_dir_name = clean_directory_name(output_dir)
        final_output_dir = Path("downloads") / clean_dir_name

    # Create output directory if it doesn't exist
    Path(final_output_dir).mkdir(parents=True, exist_ok=True)

    # Configure yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(final_output_dir, '%(title)s.%(ext)s'),
        'format': f'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio' if format_id is None else format_id,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': bitrate,
        }],
        'progress_hooks': [progress_hook],
        'quiet': False,
        'no_warnings': False,
    }

    try:
        click.echo(f"🎵 Starting audio extraction from: {url}")
        click.echo(f"📁 Output directory: {final_output_dir}")
        click.echo(f"🎚️  Audio quality: {bitrate} kbps")

        if split_large_files:
            click.echo(f"✂️  Large file splitting: Enabled (max 16MB per chunk)")

        if split_by_chapters:
            click.echo(f"📚  Chapter-based splitting: Enabled")
            # Check if video has chapters before downloading
            if not has_chapters(url):
                click.echo("⚠️  Warning: Video doesn't appear to have chapters. Chapter splitting may not work as expected.")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        click.echo("✅ Audio extraction completed successfully!")

        # Find the downloaded MP3 file
        mp3_files = list(Path(final_output_dir).glob("*.mp3"))
        if not mp3_files:
            click.echo("❌ No MP3 file found after download")
            return False

        downloaded_file = mp3_files[-1]  # Get the most recent MP3 file
        file_size_mb = downloaded_file.stat().st_size / (1024 * 1024)
        click.echo(f"📊 Downloaded file size: {file_size_mb:.1f} MB")

        # Handle chapter-based splitting first (if requested)
        if split_by_chapters:
            click.echo("🔧 Splitting audio by video chapters...")
            chapters, _ = get_video_chapters(url)

            if chapters:
                if split_audio_by_chapters(str(downloaded_file), final_output_dir, chapters, bitrate):
                    click.echo("✅ Chapter-based splitting completed successfully!")
                    # Optionally remove the original file after chapter splitting
                    if click.confirm("🗑️  Remove the original file after chapter splitting?"):
                        downloaded_file.unlink()
                        click.echo("✅ Original file removed")
                else:
                    click.echo("❌ Chapter-based splitting failed!")
            else:
                click.echo("ℹ️  No chapters found, skipping chapter splitting")

        # Handle size-based splitting (if requested and not already handled by chapters)
        elif split_large_files:
            if file_size_mb > 16:
                click.echo("🔧 File is larger than 16MB, splitting into chunks...")
                if split_audio_file(str(downloaded_file), final_output_dir, 16, bitrate):
                    click.echo("✅ Audio splitting completed successfully!")
                    # Optionally remove the original large file
                    if click.confirm("🗑️  Remove the original large file?"):
                        downloaded_file.unlink()
                        click.echo("✅ Original file removed")
                else:
                    click.echo("❌ Audio splitting failed!")
            else:
                click.echo("ℹ️  File is already under 16MB, no splitting needed")

        return True

    except Exception as e:
        click.echo(f"❌ Error during download: {e}")
        return False


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
