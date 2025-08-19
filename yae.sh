#!/bin/bash
# YouTube Audio Extractor - Simple wrapper script

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment and run the extractor
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/youtube_audio_extractor_main.py" "$@"
