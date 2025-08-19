"""
Command-line interface for YouTube Audio Extractor.
Contains all CLI commands and user interface logic.
"""

import click
from .core import download_audio, validate_youtube_url
from .formats import list_formats
from .chapters import list_chapters, has_chapters
from .playlists import download_playlist, list_playlist_videos, validate_playlist_url


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
    click.echo("\n📚  Chapter-Based Splitting:")
    click.echo("  • Use --split-by-chapters to split by video chapters")
    click.echo("  • Chapter files are saved in a 'chapters' subfolder")
    click.echo("  • Perfect for albums, podcasts, and educational content")
    click.echo("\n📚  Playlist Downloads:")
    click.echo("  • Use playlist <url> to download entire playlists")
    click.echo("  • Videos are organized in numbered subfolders")
    click.echo("  • Supports all splitting options for individual videos")


@click.group()
def cli():
    """YouTube Audio Extractor - Download audio from YouTube videos and playlists."""
    pass


@cli.command()
@click.argument('url')
@click.option('--output-dir', '-o', default='downloads',
              help='Output directory name (will be created within downloads/ folder)')
@click.option('--format-id', '-f',
              help='Specific format ID to download (use list-formats to see available formats)')
@click.option('--quality', '-q', default='best',
              help='Audio quality (default: best)')
@click.option('--bitrate', '-b', default='192', type=click.Choice(['32', '64', '96', '128', '160', '192', '256', '320']),
              help='Audio bitrate in kbps (default: 192)')
@click.option('--split-large-files', '-s', is_flag=True,
              help='Automatically split files larger than 16MB into smaller chunks')
@click.option('--split-by-chapters', '-c', is_flag=True,
              help='Split audio according to YouTube video chapters')
def download(url, output_dir, format_id, quality, bitrate, split_large_files, split_by_chapters):
    """Download audio from a YouTube video."""
    # Validate that only one splitting method is selected
    if split_large_files and split_by_chapters:
        click.echo("❌ Error: Cannot use both --split-large-files and --split-by-chapters at the same time")
        click.echo("   Choose one splitting method:")
        click.echo("   • --split-large-files: Split by file size (16MB chunks)")
        click.echo("   • --split-by-chapters: Split by video chapters")
        return

    download_audio(url, output_dir, format_id, quality, bitrate, split_large_files, split_by_chapters)


@cli.command()
@click.argument('url')
@click.option('--output-dir', '-o', default='downloads',
              help='Output directory name (will be created within downloads/ folder)')
@click.option('--quality', '-q', default='best',
              help='Audio quality (default: best)')
@click.option('--bitrate', '-b', default='192', type=click.Choice(['32', '64', '96', '128', '160', '192', '256', '320']),
              help='Audio bitrate in kbps (default: 192)')
@click.option('--split-large-files', '-s', is_flag=True,
              help='Automatically split files larger than 16MB into smaller chunks')
@click.option('--split-by-chapters', '-c', is_flag=True,
              help='Split audio according to YouTube video chapters')
@click.option('--start-index', '-start', default=1, type=int,
              help='Start downloading from this video index (default: 1)')
@click.option('--end-index', '-end', type=int,
              help='Stop downloading at this video index (default: all remaining videos)')
def playlist(url, output_dir, quality, bitrate, split_large_files, split_by_chapters, start_index, end_index):
    """Download entire YouTube playlist."""
    # Validate that only one splitting method is selected
    if split_large_files and split_by_chapters:
        click.echo("❌ Error: Cannot use both --split-large-files and --split-by-chapters at the same time")
        click.echo("   Choose one splitting method:")
        click.echo("   • --split-large-files: Split by file size (16MB chunks)")
        click.echo("   • --split-by-chapters: Split by video chapters")
        return

    # Validate playlist URL
    if not validate_playlist_url(url):
        click.echo("❌ Error: Invalid YouTube playlist URL provided!")
        click.echo("   Playlist URLs should contain 'playlist' or 'list=' parameter")
        return

    download_playlist(url, output_dir, quality, bitrate, split_large_files, split_by_chapters, start_index, end_index)


@cli.command()
@click.argument('url')
def list_playlist_cmd(url):
    """List all videos in a YouTube playlist."""
    if not validate_playlist_url(url):
        click.echo("❌ Error: Invalid YouTube playlist URL provided!")
        click.echo("   Playlist URLs should contain 'playlist' or 'list=' parameter")
        return

    list_playlist_videos(url)


@cli.command()
@click.argument('url')
def list_formats_cmd(url):
    """List available audio formats for a YouTube video."""
    list_formats(url)


@cli.command()
@click.argument('url')
def list_chapters_cmd(url):
    """List available chapters for a YouTube video."""
    list_chapters(url)


@cli.command()
@click.argument('url')
def check_chapters_cmd(url):
    """Check if a YouTube video has chapters."""
    if not validate_youtube_url(url):
        click.echo("❌ Invalid YouTube URL provided!")
        return

    if has_chapters(url):
        click.echo("✅ This video has chapters!")
        click.echo("💡 Use --split-by-chapters to split audio by chapters")
    else:
        click.echo("❌ This video doesn't have chapters")
        click.echo("💡 Use --split-large-files to split by file size instead")


@cli.command()
def bitrates():
    """Show available audio bitrates and their file sizes."""
    show_bitrate_info()


@cli.command()
def info():
    """Show information about the YouTube Audio Extractor."""
    click.echo("🎵 YouTube Audio Extractor")
    click.echo("=" * 40)
    click.echo("A command-line tool to extract audio from YouTube videos and playlists.")
    click.echo("\nUsage examples:")
    click.echo("  # Single video downloads:")
    click.echo("  python youtube_audio_extractor.py download <youtube_url>")
    click.echo("  python youtube_audio_extractor.py download <youtube_url> --output-dir music")
    click.echo("  python youtube_audio_extractor.py download <youtube_url> --bitrate 128")
    click.echo("  python youtube_audio_extractor.py download <youtube_url> --split-large-files")
    click.echo("  python youtube_audio_extractor.py download <youtube_url> --split-by-chapters")
    click.echo("\n  # Playlist downloads:")
    click.echo("  python youtube_audio_extractor.py playlist <playlist_url>")
    click.echo("  python youtube_audio_extractor.py playlist <playlist_url> --bitrate 320")
    click.echo("  python youtube_audio_extractor.py playlist <playlist_url> --start-index 5 --end-index 10")
    click.echo("  python youtube_audio_extractor.py playlist <playlist_url> --split-by-chapters")
    click.echo("\n  # Information commands:")
    click.echo("  python youtube_audio_extractor.py list-formats <youtube_url>")
    click.echo("  python youtube_audio_extractor.py list-chapters <youtube_url>")
    click.echo("  python youtube_audio_extractor.py list-playlist <playlist_url>")
    click.echo("  python youtube_audio_extractor.py check-chapters <youtube_url>")
    click.echo("  python youtube_audio_extractor.py bitrates")
    click.echo("\nFor more help:")
    click.echo("  python youtube_audio_extractor.py --help")
