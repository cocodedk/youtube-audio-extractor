#!/usr/bin/env python3
"""
Test script to verify YouTube Audio Extractor installation
"""

def test_imports():
    """Test if all required packages can be imported."""
    try:
        import yt_dlp  # noqa: F401
        print("✅ yt-dlp imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import yt-dlp: {e}")
        return False

    try:
        import click  # noqa: F401
        print("✅ click imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import click: {e}")
        return False

    try:
        import requests  # noqa: F401
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False

    try:
        import tqdm  # noqa: F401
        print("✅ tqdm imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import tqdm: {e}")
        return False

    return True


def test_ffmpeg():
    """Test if FFmpeg is available in the system."""
    import shutil

    if shutil.which('ffmpeg'):
        print("✅ FFmpeg found in system PATH")
        return True
    else:
        print("❌ FFmpeg not found in system PATH")
        print("   Please install FFmpeg to use audio conversion features")
        return False


def test_main_script():
    """Test if the main script can be imported."""
    try:
        import youtube_audio_extractor  # noqa: F401
        print("✅ youtube_audio_extractor module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import youtube_audio_extractor: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Testing YouTube Audio Extractor Installation")
    print("=" * 50)

    tests = [
        ("Package Imports", test_imports),
        ("FFmpeg Availability", test_ffmpeg),
        ("Main Script Import", test_main_script),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"   ⚠️  {test_name} test failed")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your installation is ready.")
        print("\n🚀 You can now use the YouTube Audio Extractor:")
        print("   python youtube_audio_extractor.py --help")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n💡 Common solutions:")
        print("   1. Install missing packages: pip install -r requirements.txt")
        print("   2. Install FFmpeg for audio conversion")
        print("   3. Check Python version (requires Python 3.7+)")

    return passed == total


if __name__ == "__main__":
    main()
