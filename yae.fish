#!/usr/bin/env fish
# YouTube Audio Extractor - Fish shell wrapper script

# Get the directory where this script is located
set SCRIPT_DIR (dirname (status -f))

# Activate virtual environment and run the extractor
$SCRIPT_DIR/venv/bin/python $SCRIPT_DIR/youtube_audio_extractor_main.py $argv
