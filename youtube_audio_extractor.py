#!/usr/bin/env python3
"""
YouTube Audio Extractor
A command-line tool to extract audio from YouTube videos.
"""

import os
import click
import yt_dlp
from pathlib import Path
from urllib.parse import urlparse
import subprocess
import math


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


def split_audio_file(input_file, output_dir, max_size_mb=16, bitrate="192"):
    """Split audio file into chunks under specified size using FFmpeg."""
    try:
        # Get file info using FFprobe
        cmd = [
            'ffprobe', '-v', 'quiet', '-show_entries',
            'format=duration', '-of', 'csv=p=0', input_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            click.echo(f"❌ Error getting audio duration: {result.stderr}")
            return False

        duration = float(result.stdout.strip())

        # Calculate chunk duration based on bitrate and max size
        # Formula: duration = (size_in_bits) / (bitrate * 1000)
        # For MP3: size_in_bits = max_size_mb * 8 * 1024 * 1024
        max_size_bits = max_size_mb * 8 * 1024 * 1024
        bitrate_bps = int(bitrate) * 1000

        # Add some safety margin (90% of calculated size)
        safe_duration = (max_size_bits * 0.9) / bitrate_bps

        # Calculate number of chunks needed
        num_chunks = math.ceil(duration / safe_duration)
        chunk_duration = duration / num_chunks

        click.echo(f"📏 Audio duration: {duration:.1f} seconds")
        click.echo(f"✂️  Splitting into {num_chunks} chunks of ~{chunk_duration:.1f} seconds each")

        # Create output directory for split files
        split_dir = Path(output_dir) / "split_chunks"
        split_dir.mkdir(parents=True, exist_ok=True)

        # Split the audio file
        base_name = Path(input_file).stem
        for i in range(num_chunks):
            start_time = i * chunk_duration
            end_time = min((i + 1) * chunk_duration, duration)

            output_file = split_dir / f"{base_name}_part{i+1:02d}.mp3"

            cmd = [
                'ffmpeg', '-i', input_file, '-ss', str(start_time),
                '-t', str(end_time - start_time), '-c', 'copy',
                '-y', str(output_file)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                click.echo(f"❌ Error splitting chunk {i+1}: {result.stderr}")
                return False

            # Get the actual file size
            chunk_size = output_file.stat().st_size / (1024 * 1024)
            click.echo(f"✅ Chunk {i+1}: {output_file.name} ({chunk_size:.1f} MB)")

        click.echo(f"🎯 All chunks saved to: {split_dir}")
        return True

    except Exception as e:
        click.echo(f"❌ Error splitting audio file: {e}")
        return False


def download_audio(url, output_dir="downloads", format_id=None, quality="best", bitrate="192", split_large_files=False):
    """Download audio from YouTube video."""
    if not validate_youtube_url(url):
        click.echo("❌ Invalid YouTube URL provided!")
        return False

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Configure yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio' if format_id is None else format_id,
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
        click.echo(f"📁 Output directory: {output_dir}")
        click.echo(f"🎚️  Audio quality: {bitrate} kbps")
        if split_large_files:
            click.echo("✂️  Large file splitting: Enabled (max 16MB per chunk)")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        click.echo("✅ Audio extraction completed successfully!")

        # Check if splitting is requested and find the downloaded file
        if split_large_files:
            # Find the downloaded MP3 file
            mp3_files = list(Path(output_dir).glob("*.mp3"))
            if mp3_files:
                downloaded_file = mp3_files[-1]  # Get the most recent MP3 file
                file_size_mb = downloaded_file.stat().st_size / (1024 * 1024)

                click.echo(f"📊 Downloaded file size: {file_size_mb:.1f} MB")

                if file_size_mb > 16:
                    click.echo("🔧 File is larger than 16MB, splitting into chunks...")
                    if split_audio_file(str(downloaded_file), output_dir, 16, bitrate):
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


def list_formats(url):
    """List available audio formats for the video."""
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


def show_bitrate_info():
    """Show information about available bitrates and their file sizes."""
    click.echo("🎚️  Audio Quality Options:")
    click.echo("=" * 40)
    click.echo("Bitrate | Quality    | File Size (per 1 min)")
    click.echo("-" * 40)

    bitrates = [
        ("32", "Very Low", "0.24 MB"),
        ("64", "Low", "0.48 MB"),
        ("96", "Fair", "0.72 MB"),
        ("128", "Good", "0.96 MB"),
        ("160", "Better", "1.2 MB"),
        ("192", "High", "1.44 MB"),
        ("256", "Very High", "1.92 MB"),
        ("320", "Maximum", "2.4 MB"),
    ]

    for bitrate, quality, size in bitrates:
        click.echo(f"{bitrate:>6} | {quality:<11} | {size}")

    click.echo("\n💡 Tips:")
    click.echo("  • 32-64 kbps: Podcasts, voice recordings")
    click.echo("  • 96-128 kbps: Music, good balance of quality/size")
    click.echo("  • 160-192 kbps: High-quality music")
    click.echo("  • 256-320 kbps: Lossless-like quality, larger files")
    click.echo("\n✂️  Large File Splitting:")
    click.echo("  • Use --split-large-files to automatically split files >16MB")
    click.echo("  • Split files are saved in a 'split_chunks' subfolder")
    click.echo("  • Works with any bitrate setting")


@click.group()
def cli():
    """YouTube Audio Extractor - Download audio from YouTube videos."""
    pass


@cli.command()
@click.argument('url')
@click.option('--output-dir', '-o', default='downloads',
              help='Output directory for downloaded files (default: downloads)')
@click.option('--format-id', '-f',
              help='Specific format ID to download (use list-formats to see available formats)')
@click.option('--quality', '-q', default='best',
              help='Audio quality (default: best)')
@click.option('--bitrate', '-b', default='192', type=click.Choice(['32', '64', '96', '128', '160', '192', '256', '320']),
              help='Audio bitrate in kbps (default: 192)')
@click.option('--split-large-files', '-s', is_flag=True,
              help='Automatically split files larger than 16MB into smaller chunks')
def download(url, output_dir, format_id, quality, bitrate, split_large_files):
    """Download audio from a YouTube video."""
    download_audio(url, output_dir, format_id, quality, bitrate, split_large_files)


@cli.command()
@click.argument('url')
def list_formats_cmd(url):
    """List available audio formats for a YouTube video."""
    list_formats(url)


@cli.command()
def bitrates():
    """Show available audio bitrates and their file sizes."""
    show_bitrate_info()


@cli.command()
def info():
    """Show information about the YouTube Audio Extractor."""
    click.echo("🎵 YouTube Audio Extractor")
    click.echo("=" * 40)
    click.echo("A command-line tool to extract audio from YouTube videos.")
    click.echo("\nUsage examples:")
    click.echo("  python youtube_audio_extractor.py download <youtube_url>")
    click.echo("  python youtube_audio_extractor.py download <youtube_url> --output-dir music")
    click.echo("  python youtube_audio_extractor.py download <youtube_url> --bitrate 128")
    click.echo("  python youtube_audio_extractor.py download <youtube_url> --split-large-files")
    click.echo("  python youtube_audio_extractor.py list-formats <youtube_url>")
    click.echo("  python youtube_audio_extractor.py bitrates")
    click.echo("\nFor more help:")
    click.echo("  python youtube_audio_extractor.py --help")


if __name__ == '__main__':
    cli()
