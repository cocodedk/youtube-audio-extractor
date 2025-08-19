#!/usr/bin/env python3
"""
Example usage of YouTube Audio Extractor
This script demonstrates how to use the extractor programmatically
"""

import sys
import os

# Add the current directory to Python path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from youtube_audio_extractor import download_audio, list_formats, validate_youtube_url


def example_basic_download():
    """Example of basic audio download."""
    print("🎵 Example 1: Basic Audio Download")
    print("-" * 40)

    # Example YouTube URL (replace with a real one)
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    if validate_youtube_url(url):
        print(f"✅ Valid YouTube URL: {url}")

        # Download audio to default 'downloads' folder
        success = download_audio(url)

        if success:
            print("🎉 Download completed successfully!")
        else:
            print("❌ Download failed!")
    else:
        print("❌ Invalid YouTube URL!")

    print()


def example_custom_directory():
    """Example of downloading to a custom directory."""
    print("🎵 Example 2: Custom Output Directory")
    print("-" * 40)

    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    custom_dir = "my_music"

    if validate_youtube_url(url):
        print(f"✅ Valid YouTube URL: {url}")
        print(f"📁 Custom output directory: {custom_dir}")

        # Download audio to custom directory
        success = download_audio(url, output_dir=custom_dir)

        if success:
            print("🎉 Download completed successfully!")
        else:
            print("❌ Download failed!")
    else:
        print("❌ Invalid YouTube URL!")

    print()


def example_list_formats():
    """Example of listing available audio formats."""
    print("🎵 Example 3: List Available Formats")
    print("-" * 40)

    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    if validate_youtube_url(url):
        print(f"✅ Valid YouTube URL: {url}")
        print("🔍 Fetching available audio formats...")

        # List available formats
        list_formats(url)
    else:
        print("❌ Invalid YouTube URL!")

    print()


def example_url_validation():
    """Example of URL validation."""
    print("🎵 Example 4: URL Validation")
    print("-" * 40)

    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.google.com",
        "not_a_url",
        "https://www.youtube.com/invalid",
    ]

    for url in test_urls:
        is_valid = validate_youtube_url(url)
        status = "✅ Valid" if is_valid else "❌ Invalid"
        print(f"{status}: {url}")

    print()


def main():
    """Run all examples."""
    print("🚀 YouTube Audio Extractor - Example Usage")
    print("=" * 60)
    print("This script demonstrates various ways to use the extractor.")
    print("Note: Replace the example URLs with real YouTube URLs to test.")
    print()

    # Run examples
    example_url_validation()
    example_list_formats()
    example_basic_download()
    example_custom_directory()

    print("🎯 To use the command-line interface:")
    print("   python youtube_audio_extractor.py --help")
    print("   python youtube_audio_extractor.py download <youtube_url>")


if __name__ == "__main__":
    main()
