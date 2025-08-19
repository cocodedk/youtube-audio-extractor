#!/usr/bin/env python3
"""
Setup script for YouTube Audio Extractor
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="youtube-audio-extractor",
    version="1.0.0",
    author="YouTube Audio Extractor",
    description="A command-line tool to extract audio from YouTube videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cocodedk/youtube-audio-extractor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "youtube-audio-extractor=youtube_audio_extractor.cli:cli",
            "yae=youtube_audio_extractor.cli:cli",
        ],
    },
    keywords="youtube, audio, download, extract, mp3, music",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/youtube-audio-extractor/issues",
        "Source": "https://github.com/yourusername/youtube-audio-extractor",
    },
)
