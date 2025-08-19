"""
Chapter handling for YouTube Audio Extractor.
Contains functions for detecting and using YouTube video chapters for audio splitting.
"""

import click
import yt_dlp
from pathlib import Path
import subprocess
import re


def get_video_chapters(url):
    """Extract chapter information from a YouTube video."""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Check for chapters in video info
            chapters = info.get('chapters', [])

            if not chapters:
                click.echo("ℹ️  No chapters found in this video")
                return None, info

            click.echo(f"📚 Found {len(chapters)} chapters in the video")

            # Extract chapter information
            chapter_info = []
            for i, chapter in enumerate(chapters):
                start_time = chapter.get('start_time', 0)
                end_time = chapter.get('end_time', 0)
                title = chapter.get('title', f'Chapter {i+1}')

                # Clean chapter title for filename
                clean_title = clean_chapter_title(title)

                chapter_info.append({
                    'index': i + 1,
                    'start_time': start_time,
                    'end_time': end_time,
                    'title': title,
                    'clean_title': clean_title,
                    'duration': end_time - start_time if end_time > start_time else 0
                })

                click.echo(f"  📖 Chapter {i+1}: {title} ({start_time:.0f}s - {end_time:.0f}s)")

            return chapter_info, info

    except Exception as e:
        click.echo(f"❌ Error extracting chapter info: {e}")
        return None, None


def clean_chapter_title(title):
    """Clean chapter title for use in filenames."""
    # Remove or replace characters that are problematic in filenames
    clean = re.sub(r'[<>:"/\\|?*]', '_', title)
    clean = re.sub(r'\s+', ' ', clean)  # Replace multiple spaces with single space
    clean = clean.strip()

    # Limit length to avoid extremely long filenames
    if len(clean) > 100:
        clean = clean[:97] + "..."

    return clean


def split_audio_by_chapters(input_file, output_dir, chapters, bitrate="192"):
    """Split audio file according to YouTube video chapters."""
    try:
        if not chapters:
            click.echo("❌ No chapters provided for splitting")
            return False

        # Create output directory for chapter files
        chapters_dir = Path(output_dir) / "chapters"
        chapters_dir.mkdir(parents=True, exist_ok=True)

        click.echo(f"✂️  Splitting audio into {len(chapters)} chapter files...")

        # Split the audio file by chapters
        base_name = Path(input_file).stem

        for chapter in chapters:
            start_time = chapter['start_time']
            duration = chapter['duration']
            clean_title = chapter['clean_title']
            index = chapter['index']

            # Create filename: base_name_chapter01_chapter_title.mp3
            output_file = chapters_dir / f"{base_name}_chapter{index:02d}_{clean_title}.mp3"

            # Use FFmpeg to extract the chapter segment
            cmd = [
                'ffmpeg', '-i', input_file, '-ss', str(start_time),
                '-t', str(duration), '-c', 'copy', '-y', str(output_file)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                click.echo(f"❌ Error splitting chapter {index}: {result.stderr}")
                return False

            # Get the actual file size
            chapter_size = output_file.stat().st_size / (1024 * 1024)
            click.echo(f"✅ Chapter {index}: {output_file.name} ({chapter_size:.1f} MB)")

        click.echo(f"🎯 All chapter files saved to: {chapters_dir}")
        return True

    except Exception as e:
        click.echo(f"❌ Error splitting audio by chapters: {e}")
        return False


def list_chapters(url):
    """List available chapters for a YouTube video."""
    chapters, info = get_video_chapters(url)

    if not chapters:
        return

    click.echo(f"\n📺 Video: {info.get('title', 'Unknown')}")
    click.echo(f"⏱️  Total Duration: {info.get('duration', 'Unknown')} seconds")
    click.echo(f"📚 Chapters: {len(chapters)}")
    click.echo("\n📖 Chapter Details:")
    click.echo("-" * 80)

    for chapter in chapters:
        start_min = int(chapter['start_time'] // 60)
        start_sec = int(chapter['start_time'] % 60)
        end_min = int(chapter['end_time'] // 60)
        end_sec = int(chapter['end_time'] % 60)

        click.echo(f"Chapter {chapter['index']:2d}: {start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d} | {chapter['title']}")
        click.echo(f"         Duration: {chapter['duration']:.0f}s | Clean Title: {chapter['clean_title']}")
        click.echo()


def has_chapters(url):
    """Check if a YouTube video has chapters."""
    chapters, _ = get_video_chapters(url)
    return chapters is not None and len(chapters) > 0
