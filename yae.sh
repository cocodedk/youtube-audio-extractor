#!/bin/bash
# YouTube Audio Extractor - Simple wrapper script

set -e  # Exit on any error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if virtual environment exists
if [[ ! -f "$SCRIPT_DIR/venv/bin/python" ]]; then
    echo "Error: Virtual environment not found at $SCRIPT_DIR/venv"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if main script exists
if [[ ! -f "$SCRIPT_DIR/youtube_audio_extractor_main.py" ]]; then
    echo "Error: Main script not found at $SCRIPT_DIR/youtube_audio_extractor_main.py"
    exit 1
fi

# Activate virtual environment and run the extractor
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/youtube_audio_extractor_main.py" "$@"
