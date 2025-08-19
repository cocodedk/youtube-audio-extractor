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


def download_audio_with_progress(url, output_dir="downloads", format_id=None, quality="best", bitrate="192",
                                split_large_files=False, split_by_chapters=False, progress_hook=None, download_id=None):
    """Download audio from YouTube video with custom progress tracking."""
    if not validate_youtube_url(url):
        if progress_hook:
            progress_hook({'status': 'error', 'message': 'Invalid YouTube URL provided!'})
        else:
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
        'quiet': False,
        'no_warnings': False,
    }

    # Add progress hook if provided
    if progress_hook:
        ydl_opts['progress_hooks'] = [progress_hook]

    try:
        if progress_hook:
            progress_hook({'status': 'starting', 'message': f'Starting audio extraction from: {url}'})
        else:
            click.echo(f"🎵 Starting audio extraction from: {url}")

        if progress_hook:
            progress_hook({'status': 'info', 'message': f'Output directory: {final_output_dir}'})
        else:
            click.echo(f"📁 Output directory: {final_output_dir}")

        if progress_hook:
            progress_hook({'status': 'info', 'message': f'Audio quality: {bitrate} kbps'})
        else:
            click.echo(f"🎚️  Audio quality: {bitrate} kbps")

        if split_large_files:
            if progress_hook:
                progress_hook({'status': 'info', 'message': 'Large file splitting: Enabled (max 16MB per chunk)'})
            else:
                click.echo(f"✂️  Large file splitting: Enabled (max 16MB per chunk)")

        if split_by_chapters:
            if progress_hook:
                progress_hook({'status': 'info', 'message': 'Chapter-based splitting: Enabled'})
            else:
                click.echo(f"📚  Chapter-based splitting: Enabled")
            # Check if video has chapters before downloading
            if not has_chapters(url):
                if progress_hook:
                    progress_hook({'status': 'warning', 'message': "Video doesn't appear to have chapters. Chapter splitting may not work as expected."})
                else:
                    click.echo("⚠️  Warning: Video doesn't appear to have chapters. Chapter splitting may not work as expected.")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if progress_hook:
            progress_hook({'status': 'finished', 'message': 'Audio extraction completed successfully!'})
        else:
            click.echo("✅ Audio extraction completed successfully!")

        # Find the downloaded audio file (MP3, M4A, or other audio formats)
        audio_files = list(Path(final_output_dir).glob("*.mp3")) + list(Path(final_output_dir).glob("*.m4a")) + list(Path(final_output_dir).glob("*.webm"))
        if not audio_files:
            if progress_hook:
                progress_hook({'status': 'error', 'message': 'No audio file found after download'})
            else:
                click.echo("❌ No audio file found after download")
            return False

        downloaded_file = audio_files[-1]  # Get the most recent audio file
        file_size_mb = downloaded_file.stat().st_size / (1024 * 1024)

        if progress_hook:
            progress_hook({'status': 'info', 'message': f'Downloaded file: {downloaded_file.name} ({file_size_mb:.1f} MB)'})
        else:
            click.echo(f"📊 Downloaded file: {downloaded_file.name} ({file_size_mb:.1f} MB)")

        # Handle chapter-based splitting first (if requested)
        if split_by_chapters:
            if progress_hook:
                progress_hook({'status': 'processing', 'message': 'Splitting audio by video chapters...'})
            else:
                click.echo("🔧 Splitting audio by video chapters...")

            chapters, _ = get_video_chapters(url)

            if chapters:
                if split_audio_by_chapters(str(downloaded_file), final_output_dir, chapters, bitrate):
                    if progress_hook:
                        progress_hook({'status': 'success', 'message': 'Chapter-based splitting completed successfully!'})
                    else:
                        click.echo("✅ Chapter-based splitting completed successfully!")
                    # In web mode, don't prompt for confirmation - just remove the original file
                    if progress_hook:
                        downloaded_file.unlink()
                        progress_hook({'status': 'info', 'message': 'Original file removed'})
                    else:
                        # In CLI mode, ask for confirmation
                        if click.confirm("🗑️  Remove the original file after chapter splitting?"):
                            downloaded_file.unlink()
                            click.echo("✅ Original file removed")
                else:
                    if progress_hook:
                        progress_hook({'status': 'error', 'message': 'Chapter-based splitting failed!'})
                    else:
                        click.echo("❌ Chapter-based splitting failed!")
            else:
                if progress_hook:
                    progress_hook({'status': 'info', 'message': 'No chapters found, skipping chapter splitting'})
                else:
                    click.echo("ℹ️  No chapters found, skipping chapter splitting")

        # Handle size-based splitting (if requested and not already handled by chapters)
        elif split_large_files:
            if file_size_mb > 16:
                if progress_hook:
                    progress_hook({'status': 'processing', 'message': 'File is larger than 16MB, splitting into chunks...'})
                else:
                    click.echo("🔧 File is larger than 16MB, splitting into chunks...")

                if split_audio_file(str(downloaded_file), final_output_dir, 16, bitrate):
                    if progress_hook:
                        progress_hook({'status': 'success', 'message': 'Audio splitting completed successfully!'})
                    else:
                        click.echo("✅ Audio splitting completed successfully!")
                    # In web mode, don't prompt for confirmation - just remove the original file
                    if progress_hook:
                        downloaded_file.unlink()
                        progress_hook({'status': 'info', 'message': 'Original file removed'})
                    else:
                        # In CLI mode, ask for confirmation
                        if click.confirm("🗑️  Remove the original large file?"):
                            downloaded_file.unlink()
                            click.echo("✅ Original file removed")
                else:
                    if progress_hook:
                        progress_hook({'status': 'error', 'message': 'Audio splitting failed!'})
                    else:
                        click.echo("❌ Audio splitting failed!")
            else:
                if progress_hook:
                    progress_hook({'status': 'info', 'message': 'File is already under 16MB, no splitting needed'})
                else:
                    click.echo("ℹ️  File is already under 16MB, no splitting needed")

        # Send final completion message
        if progress_hook:
            progress_hook({'status': 'completed', 'message': 'Download and processing completed successfully!', 'percent': 100})

        return True

    except Exception as e:
        if progress_hook:
            progress_hook({'status': 'error', 'message': f'Error during download: {e}'})
        else:
            click.echo(f"❌ Error during download: {e}")
        return False


def download_audio(url, output_dir="downloads", format_id=None, quality="best", bitrate="192", split_large_files=False, split_by_chapters=False):
    """Download audio from YouTube video."""
    return download_audio_with_progress(url, output_dir, format_id, quality, bitrate, split_large_files, split_by_chapters)


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
