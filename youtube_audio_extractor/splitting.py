"""
Audio splitting functionality for YouTube Audio Extractor.
Contains functions for splitting large audio files into smaller chunks.
"""

import click
import subprocess
import math
from pathlib import Path


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
