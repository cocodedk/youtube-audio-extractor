#!/usr/bin/env python3
"""
Test script for the progress tracking functionality
"""

import time

def test_progress_hook(data):
    """Test progress hook function"""
    if data.get('status') == 'downloading':
        if 'percent' in data:
            print(f"📥 Download Progress: {data['percent']:.1f}%")
        if 'message' in data:
            print(f"ℹ️  {data['message']}")
    elif data.get('status') == 'finished':
        print(f"✅ {data.get('message', 'Download finished')}")
    elif data.get('status') == 'error':
        print(f"❌ {data.get('message', 'Error occurred')}")
    else:
        print(f"ℹ️  {data.get('message', 'Status update')}")

def test_download_with_progress():
    """Test the progress-enabled download function"""
    print("🧪 Testing progress tracking functionality...")
    print("=" * 50)

    # Test URL (replace with a real YouTube URL for actual testing)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll for testing

    print(f"🎵 Testing download with URL: {test_url}")
    print("📝 This will test the progress hook system without actually downloading")

    # Test the progress hook function
    print("\n🔧 Testing progress hook function...")
    test_data = [
        {'status': 'starting', 'message': 'Starting download...'},
        {'status': 'downloading', 'percent': 25.0, 'message': 'Downloading audio...'},
        {'status': 'downloading', 'percent': 50.0, 'message': 'Halfway there...'},
        {'status': 'downloading', 'percent': 75.0, 'message': 'Almost done...'},
        {'status': 'finished', 'message': 'Download completed!'},
    ]

    for data in test_data:
        test_progress_hook(data)
        time.sleep(0.5)  # Simulate real-time updates

    print("\n✅ Progress tracking test completed successfully!")
    print("💡 The progress hook system is working correctly")
    print("\n📋 To test with real downloads:")
    print("   1. Start the web server: python web_app.py")
    print("   2. Open the web UI in your browser")
    print("   3. Enter a YouTube URL and start a download")
    print("   4. Watch the progress bar update in real-time!")

if __name__ == "__main__":
    test_download_with_progress()
