#!/usr/bin/env fish
# YouTube Audio Extractor - Fish shell wrapper script

# Get the directory where this script is located
set SCRIPT_DIR (dirname (status -f))

# Check if virtual environment exists
if not test -f "$SCRIPT_DIR/venv/bin/python"
    echo "Error: Virtual environment not found at $SCRIPT_DIR/venv"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
end

# Check if main script exists
if not test -f "$SCRIPT_DIR/youtube_audio_extractor_main.py"
    echo "Error: Main script not found at $SCRIPT_DIR/youtube_audio_extractor_main.py"
    exit 1
end

# Activate virtual environment and run the extractor
$SCRIPT_DIR/venv/bin/python $SCRIPT_DIR/youtube_audio_extractor_main.py $argv
