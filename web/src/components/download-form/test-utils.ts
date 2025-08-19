import { ApiService } from '../../services/api-service';

export class TestUtils {
  private element: HTMLElement;
  private apiService: ApiService;

  constructor(container: HTMLElement, apiService: ApiService) {
    this.element = container;
    this.apiService = apiService;
  }

  public testProgressBar(): void {
    console.log('Testing progress bar with real YouTube URL...');

    // Set the URL input to the test URL
    const urlInput = this.element.querySelector('#url') as HTMLInputElement;
    urlInput.value = 'https://www.youtube.com/watch?v=xlgwFGdPRns';

    // Enable the download button
    const downloadBtn = this.element.querySelector('#downloadBtn') as HTMLButtonElement;
    downloadBtn.disabled = false;

    // Simulate the download process
    console.log('Starting simulated download process...');

    // Simulate starting
    setTimeout(() => {
      this.updateProgress({
        status: 'starting',
        message: 'Starting download of test video...',
        percent: 0
      });
    }, 500);

    // Simulate downloading
    setTimeout(() => {
      this.updateProgress({
        status: 'downloading',
        message: 'Downloading audio from YouTube...',
        percent: 25,
        downloaded_bytes: 1024 * 1024, // 1MB
        total_bytes: 4 * 1024 * 1024, // 4MB
        speed: 1024 * 1024 // 1MB/s
      });
    }, 1500);

    // Simulate more progress
    setTimeout(() => {
      this.updateProgress({
        status: 'downloading',
        message: 'Processing audio...',
        percent: 75,
        downloaded_bytes: 3 * 1024 * 1024, // 3MB
        total_bytes: 4 * 1024 * 1024, // 4MB
        speed: 1024 * 1024 // 1MB/s
      });
    }, 2500);

    // Simulate completion
    setTimeout(() => {
      this.updateProgress({
        status: 'completed',
        message: 'Test download completed successfully!',
        percent: 100,
        downloaded_bytes: 4 * 1024 * 1024, // 4MB
        total_bytes: 4 * 1024 * 1024, // 4MB
        speed: 0
      });
    }, 3500);

    // Test actual download after simulation
    setTimeout(() => {
      console.log('Testing actual download API call...');
      this.testActualDownload();
    }, 4000);
  }

  private async testActualDownload(): Promise<void> {
    try {
      console.log('Making actual API call to test download...');

      const testData = {
        url: 'https://www.youtube.com/watch?v=xlgwFGdPRns',
        output_dir: 'downloads',
        bitrate: '192',
        split_large_files: false,
        split_by_chapters: false
      };

      const response = await this.apiService.downloadVideo(testData);
      console.log('Download API response:', response);

      if (response.download_id) {
        console.log('Starting real progress tracking for download ID:', response.download_id);
        // Emit an event or callback to notify the main component
        this.element.dispatchEvent(new CustomEvent('testDownloadStarted', {
          detail: { downloadId: response.download_id }
        }));
      }

    } catch (error) {
      console.error('Test download failed:', error);
      this.updateProgress({
        status: 'error',
        message: `Test download failed: ${error}`,
        percent: 0
      });
    }
  }

  private updateProgress(data: any): void {
    // This is just for testing - dispatch an event to the main component
    this.element.dispatchEvent(new CustomEvent('testProgressUpdate', {
      detail: { data }
    }));
  }
}
