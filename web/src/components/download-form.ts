import { ApiService } from '../services/api-service';

export class DownloadForm {
  public element: HTMLElement;
  private apiService: ApiService;
  private onDownloadStartedCallback?: () => void;
  private isDownloading: boolean = false;
  private currentMode: 'download' | 'playlist' = 'download';
  private currentDownloadId: string | null = null;
  private progressEventSource: EventSource | null = null;

  constructor() {
    this.apiService = new ApiService();
    this.element = this.createDownloadForm();
    this.setupEventListeners();
  }

  public setMode(mode: 'download' | 'playlist'): void {
    this.currentMode = mode;
    this.updateFormDisplay();
  }

  private updateFormDisplay(): void {
    const titleElement = this.element.querySelector('#formTitle') as HTMLElement;
    const descriptionElement = this.element.querySelector('#formDescription') as HTMLElement;
    const playlistOptionsElement = this.element.querySelector('#playlistOptions') as HTMLElement;
    const playlistBtn = this.element.querySelector('#playlistBtn') as HTMLButtonElement;
    const downloadBtn = this.element.querySelector('#downloadBtn') as HTMLButtonElement;

    if (this.currentMode === 'playlist') {
      titleElement.textContent = 'Download Playlist';
      descriptionElement.textContent = 'Enter a YouTube playlist URL to download all videos';
      playlistOptionsElement.classList.remove('hidden');
      playlistBtn.classList.add('btn-primary');
      playlistBtn.classList.remove('btn-secondary');
      downloadBtn.classList.add('btn-secondary');
      downloadBtn.classList.remove('btn-primary');
    } else {
      titleElement.textContent = 'Download Audio';
      descriptionElement.textContent = 'Enter a YouTube URL to extract audio';
      playlistOptionsElement.classList.add('hidden');
      downloadBtn.classList.add('btn-primary');
      downloadBtn.classList.remove('btn-secondary');
      playlistBtn.classList.add('btn-secondary');
      playlistBtn.classList.remove('btn-primary');
    }
  }

  private createDownloadForm(): HTMLElement {
    const container = document.createElement('div');
    container.className = 'card mb-8';

    container.innerHTML = `
      <div class="mb-6">
        <h2 id="formTitle" class="text-xl font-semibold text-gray-100 mb-2">Download Audio</h2>
        <p id="formDescription" class="text-gray-400">Enter a YouTube URL to extract audio</p>
      </div>

      <form id="downloadForm" class="space-y-6">
        <!-- URL Input -->
        <div>
          <label for="url" class="block text-sm font-medium text-gray-300 mb-2">
            YouTube URL
          </label>
          <input
            type="url"
            id="url"
            name="url"
            required
            placeholder="https://www.youtube.com/watch?v=... or https://youtube.com/playlist?list=..."
            class="input"
          >
        </div>

        <!-- Playlist-specific Options -->
        <div id="playlistOptions" class="hidden space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="startIndex" class="block text-sm font-medium text-gray-300 mb-2">
                Start Video Number
              </label>
              <input
                type="number"
                id="startIndex"
                name="startIndex"
                min="1"
                value="1"
                class="input"
              >
            </div>
            <div>
              <label for="endIndex" class="block text-sm font-medium text-gray-300 mb-2">
                End Video Number (optional)
              </label>
              <input
                type="number"
                id="endIndex"
                name="endIndex"
                min="1"
                placeholder="Leave empty for all videos"
                class="input"
              >
            </div>
          </div>
          <div class="bg-blue-900/20 border border-blue-700/50 rounded-md p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-blue-300">Playlist Download Tips</h3>
                <div class="mt-2 text-sm text-blue-200">
                  <p>• Use range selection to download specific videos (e.g., videos 5-10)</p>
                  <p>• Leave end number empty to download from start to end</p>
                  <p>• Large playlists may take significant time to download</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Output Directory -->
        <div>
          <label for="outputDir" class="block text-sm font-medium text-gray-300 mb-2">
            Output Directory (optional)
          </label>
          <input
            type="text"
            id="outputDir"
            name="outputDir"
            placeholder="music, podcasts, etc."
            class="input"
          >
          <p class="mt-1 text-sm text-gray-500">
            Leave empty to save in downloads/ folder
          </p>
        </div>

        <!-- Bitrate Selection -->
        <div>
          <label for="bitrate" class="block text-sm font-medium text-gray-300 mb-2">
            Audio Quality
          </label>
          <select id="bitrate" name="bitrate" class="input">
            <option value="32">32 kbps - Very Low (Podcasts, voice)</option>
            <option value="64">64 kbps - Low (Basic audio)</option>
            <option value="96">96 kbps - Fair (Good balance)</option>
            <option value="128">128 kbps - Good (Music, general use)</option>
            <option value="160">160 kbps - Better (High-quality music)</option>
            <option value="192" selected>192 kbps - High (Default - Best balance)</option>
            <option value="256">256 kbps - Very High (Lossless-like)</option>
            <option value="320">320 kbps - Maximum (Studio quality)</option>
          </select>
        </div>

        <!-- Splitting Options -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="flex items-center">
            <input
              type="checkbox"
              id="splitLargeFiles"
              name="splitLargeFiles"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-dark-600 rounded bg-dark-700"
            >
            <label for="splitLargeFiles" class="ml-2 block text-sm text-gray-300">
              Split large files (>16MB)
            </label>
          </div>
          <div class="flex items-center">
            <input
              type="checkbox"
              id="splitByChapters"
              name="splitByChapters"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-dark-600 rounded bg-dark-700"
            >
            <label for="splitByChapters" class="ml-2 block text-sm text-gray-300">
              Split by video chapters
            </label>
          </div>
        </div>

        <!-- Download Buttons -->
        <div class="flex flex-col sm:flex-row gap-3">
          <button
            type="submit"
            id="downloadBtn"
            class="btn-primary flex-1"
            disabled
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            Download Audio
          </button>
          <button
            type="button"
            id="playlistBtn"
            class="btn-secondary flex-1"
            disabled
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path>
            </svg>
            Download Playlist
          </button>
          <button
            type="button"
            id="testProgressBtn"
            class="btn-secondary"
          >
            Test Progress Bar
          </button>
        </div>

        <!-- Progress Bar -->
        <div id="progressContainer" class="hidden space-y-4">
          <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-sm font-medium text-gray-200">Download Progress</h3>
              <span id="progressStatus" class="text-sm text-gray-400">Initializing...</span>
            </div>

            <!-- Overall Progress Bar -->
            <div class="mb-3">
              <div class="flex justify-between text-sm text-gray-400 mb-1">
                <span id="progressText">0%</span>
                <span id="progressDetails">0 B / 0 B</span>
              </div>
              <div class="w-full bg-gray-700 rounded-full h-2">
                <div id="progressBar" class="bg-primary-600 h-2 rounded-full transition-all duration-300" style="width: 0%"></div>
              </div>
            </div>

            <!-- Current Step -->
            <div id="currentStep" class="text-sm text-gray-300 mb-3">
              <div class="flex items-center">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-primary-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span id="stepText">Initializing download...</span>
              </div>
            </div>

            <!-- Playlist Progress (for playlist downloads) -->
            <div id="playlistProgress" class="hidden">
              <div class="flex justify-between text-sm text-gray-400 mb-1">
                <span>Video Progress</span>
                <span id="videoProgress">0 / 0</span>
              </div>
              <div class="w-full bg-gray-700 rounded-full h-1.5">
                <div id="videoProgressBar" class="bg-blue-500 h-1.5 rounded-full transition-all duration-300" style="width: 0%"></div>
              </div>
            </div>

            <!-- Speed and ETA -->
            <div id="speedInfo" class="hidden text-sm text-gray-400">
              <div class="flex justify-between">
                <span id="downloadSpeed">Speed: 0 B/s</span>
                <span id="downloadEta">ETA: --</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Status Messages -->
        <div id="statusMessage" class="hidden"></div>
      </form>
    `;

    return container;
  }

  private setupEventListeners(): void {
    const form = this.element.querySelector('#downloadForm') as HTMLFormElement;
    const urlInput = this.element.querySelector('#url') as HTMLInputElement;
    const downloadBtn = this.element.querySelector('#downloadBtn') as HTMLButtonElement;
    const playlistBtn = this.element.querySelector('#playlistBtn') as HTMLButtonElement;
    const splitLargeFiles = this.element.querySelector('#splitLargeFiles') as HTMLInputElement;
    const splitByChapters = this.element.querySelector('#splitByChapters') as HTMLInputElement;

    // Enable/disable buttons based on URL input
    urlInput.addEventListener('input', () => {
      const hasUrl = urlInput.value.trim().length > 0;
      downloadBtn.disabled = !hasUrl || this.isDownloading;
      playlistBtn.disabled = !hasUrl || this.isDownloading;
    });

    // Prevent using both splitting options
    splitLargeFiles.addEventListener('change', () => {
      if (splitLargeFiles.checked && splitByChapters.checked) {
        splitByChapters.checked = false;
      }
    });

    splitByChapters.addEventListener('change', () => {
      if (splitByChapters.checked && splitLargeFiles.checked) {
        splitLargeFiles.checked = false;
      }
    });

    // Form submission
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      this.handleDownload();
    });

    // Playlist download
    playlistBtn.addEventListener('click', () => {
      this.handlePlaylistDownload();
    });

    // Test progress bar button
    const testProgressBtn = this.element.querySelector('#testProgressBtn') as HTMLButtonElement;
    testProgressBtn.addEventListener('click', () => {
      this.testProgressBar();
    });
  }

  private async handleDownload(): Promise<void> {
    if (this.isDownloading) return;

    const formData = this.getFormData();
    if (!formData.url) return;

    this.setDownloadingState(true);
    this.showStatus('Starting download...', 'info');

    try {
      const response = await this.apiService.downloadVideo(formData);
      this.currentDownloadId = response.download_id;
      this.showStatus('Download started successfully!', 'success');
      this.showProgressBar();
      this.startProgressTracking(response.download_id);

      if (this.onDownloadStartedCallback) {
        this.onDownloadStartedCallback();
      }
    } catch (error) {
      this.showStatus(`Download failed: ${error}`, 'error');
      this.setDownloadingState(false);
    }
  }

  private async handlePlaylistDownload(): Promise<void> {
    if (this.isDownloading) return;

    const formData = this.getFormData();
    if (!formData.url) return;

    this.setDownloadingState(true);
    this.showStatus('Starting playlist download...', 'info');

    try {
      const response = await this.apiService.downloadPlaylist(formData);
      this.currentDownloadId = response.download_id;
      this.showStatus('Playlist download started successfully!', 'success');
      this.showProgressBar();
      this.startProgressTracking(response.download_id);
      this.showPlaylistProgress();

      if (this.onDownloadStartedCallback) {
        this.onDownloadStartedCallback();
      }
    } catch (error) {
      this.showStatus(`Playlist download failed: ${error}`, 'error');
      this.setDownloadingState(false);
    }
  }

  private getFormData(): any {
    const form = this.element.querySelector('#downloadForm') as HTMLFormElement;
    const formData = new FormData(form);

    return {
      url: formData.get('url'),
      output_dir: formData.get('outputDir') || 'downloads',
      bitrate: formData.get('bitrate'),
      split_large_files: formData.get('splitLargeFiles') === 'on',
      split_by_chapters: formData.get('splitByChapters') === 'on',
      start_index: formData.get('startIndex') ? parseInt(formData.get('startIndex') as string) : 1,
      end_index: formData.get('endIndex') ? parseInt(formData.get('endIndex') as string) : undefined
    };
  }

  private setDownloadingState(downloading: boolean): void {
    this.isDownloading = downloading;
    const downloadBtn = this.element.querySelector('#downloadBtn') as HTMLButtonElement;
    const playlistBtn = this.element.querySelector('#playlistBtn') as HTMLButtonElement;
    const urlInput = this.element.querySelector('#url') as HTMLInputElement;

    downloadBtn.disabled = downloading || !urlInput.value.trim();
    playlistBtn.disabled = downloading || !urlInput.value.trim();

    if (downloading) {
      downloadBtn.innerHTML = `
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Downloading...
      `;
      playlistBtn.innerHTML = `
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-200" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Downloading...
      `;
    } else {
      downloadBtn.innerHTML = `
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        Download Audio
      `;
      playlistBtn.innerHTML = `
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path>
        </svg>
        Download Playlist
      `;
    }
  }

  private showProgressBar(): void {
    console.log('showProgressBar called');
    const progressContainer = this.element.querySelector('#progressContainer') as HTMLElement;
    console.log('Progress container found:', progressContainer);
    console.log('Progress container classes before:', progressContainer.className);
    progressContainer.classList.remove('hidden');
    console.log('Progress container classes after:', progressContainer.className);
    console.log('Progress container hidden:', progressContainer.classList.contains('hidden'));
  }

  private showPlaylistProgress(): void {
    const playlistProgress = this.element.querySelector('#playlistProgress') as HTMLElement;
    playlistProgress.classList.remove('hidden');
  }

  private testProgressBar(): void {
    console.log('Testing progress bar with real YouTube URL...');

    // Set the URL input to the test URL
    const urlInput = this.element.querySelector('#url') as HTMLInputElement;
    urlInput.value = 'https://www.youtube.com/watch?v=xlgwFGdPRns';

    // Enable the download button
    const downloadBtn = this.element.querySelector('#downloadBtn') as HTMLButtonElement;
    downloadBtn.disabled = false;

    // Show the progress bar
    this.showProgressBar();

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
        this.currentDownloadId = response.download_id;
        this.startProgressTracking(response.download_id);
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

  private startProgressTracking(downloadId: string): void {
    console.log('startProgressTracking called with ID:', downloadId);

    // Close existing connection
    if (this.progressEventSource) {
      console.log('Closing existing EventSource connection');
      this.progressEventSource.close();
    }

    // Create new EventSource connection
    const progressUrl = `http://localhost:5000/api/progress/${downloadId}`;
    console.log('Creating EventSource connection to:', progressUrl);

    try {
      this.progressEventSource = new EventSource(progressUrl);

      this.progressEventSource.onopen = (event) => {
        console.log('EventSource connection opened:', event);
        console.log('EventSource readyState:', this.progressEventSource?.readyState);
      };

      this.progressEventSource.onmessage = (event) => {
        console.log('Progress message received:', event.data);
        try {
          const data = JSON.parse(event.data);
          console.log('Parsed progress data:', data);
          this.updateProgress(data);
        } catch (error) {
          console.error('Error parsing progress data:', error);
        }
      };

      this.progressEventSource.onerror = (error) => {
        console.error('Progress tracking error:', error);
        console.error('EventSource readyState:', this.progressEventSource?.readyState);
        console.error('EventSource URL:', this.progressEventSource?.url);

        // Try to reconnect if the connection was closed unexpectedly
        if (this.progressEventSource && this.progressEventSource.readyState === EventSource.CLOSED) {
          console.log('Attempting to reconnect...');
          setTimeout(() => {
            if (this.currentDownloadId) {
              this.startProgressTracking(this.currentDownloadId);
            }
          }, 1000);
        }
      };
    } catch (error) {
      console.error('Error creating EventSource:', error);
    }
  }

  private updateProgress(data: any): void {
    // Handle heartbeat
    if (data.heartbeat) {
      return;
    }

    console.log('Updating progress with data:', data);

    // Update progress status
    const progressStatus = this.element.querySelector('#progressStatus') as HTMLElement;
    const stepText = this.element.querySelector('#stepText') as HTMLElement;
    const progressText = this.element.querySelector('#progressText') as HTMLElement;
    const progressBar = this.element.querySelector('#progressBar') as HTMLElement;
    const progressDetails = this.element.querySelector('#progressDetails') as HTMLElement;
    const speedInfo = this.element.querySelector('#speedInfo') as HTMLElement;
    const downloadSpeed = this.element.querySelector('#downloadSpeed') as HTMLElement;
    const downloadEta = this.element.querySelector('#downloadEta') as HTMLElement;

    // Update status
    if (data.status) {
      progressStatus.textContent = this.getStatusText(data.status);

      // Handle error status
      if (data.status === 'error') {
        progressStatus.className = 'text-sm text-red-400';
        stepText.className = 'text-sm text-red-300';
      } else if (data.status === 'failed') {
        progressStatus.className = 'text-sm text-red-400';
        stepText.className = 'text-sm text-red-300';
      } else {
        progressStatus.className = 'text-sm text-gray-400';
        stepText.className = 'text-sm text-gray-300';
      }
    }

    // Update step text
    if (data.message) {
      stepText.textContent = data.message;
    }

    // Update progress bar
    if (data.percent !== undefined) {
      const percent = Math.round(data.percent);
      progressText.textContent = `${percent}%`;
      progressBar.style.width = `${percent}%`;
    }

    // Update progress details
    if (data.downloaded_bytes !== undefined && data.total_bytes !== undefined) {
      const downloaded = this.formatBytes(data.downloaded_bytes);
      const total = this.formatBytes(data.total_bytes);
      progressDetails.textContent = `${downloaded} / ${total}`;
    }

    // Update speed and ETA
    if (data.speed !== undefined) {
      speedInfo.classList.remove('hidden');
      downloadSpeed.textContent = `Speed: ${this.formatBytes(data.speed)}/s`;
    }

    if (data.eta !== undefined && data.eta > 0) {
      downloadEta.textContent = `ETA: ${this.formatTime(data.eta)}`;
    }

    // Handle playlist-specific progress
    if (data.current_video !== undefined && data.total_videos !== undefined) {
      this.updatePlaylistProgress(data.current_video, data.total_videos);
    }

    // Handle completion or failure
    if (data.status === 'completed' || data.status === 'failed' || data.status === 'error') {
      this.handleDownloadComplete(data.status === 'completed');
    }
  }

  private updatePlaylistProgress(currentVideo: number, totalVideos: number): void {
    const videoProgress = this.element.querySelector('#videoProgress') as HTMLElement;
    const videoProgressBar = this.element.querySelector('#videoProgressBar') as HTMLElement;

    videoProgress.textContent = `${currentVideo} / ${totalVideos}`;
    const percent = (currentVideo / totalVideos) * 100;
    videoProgressBar.style.width = `${percent}%`;
  }

  private handleDownloadComplete(success: boolean): void {
    // Close progress tracking
    if (this.progressEventSource) {
      this.progressEventSource.close();
      this.progressEventSource = null;
    }

    // Reset state
    this.setDownloadingState(false);
    this.currentDownloadId = null;

    // Hide progress bar after a delay
    setTimeout(() => {
      const progressContainer = this.element.querySelector('#progressContainer') as HTMLElement;
      progressContainer.classList.add('hidden');
    }, 5000);

    // Show final status
    if (success) {
      this.showStatus('Download completed successfully!', 'success');
    } else {
      this.showStatus('Download failed. Check the console for details.', 'error');
    }
  }

  private getStatusText(status: string): string {
    const statusMap: { [key: string]: string } = {
      'starting': 'Starting...',
      'downloading': 'Downloading...',
      'processing': 'Processing...',
      'completed': 'Completed',
      'failed': 'Failed',
      'error': 'Error',
      'downloading_video': 'Downloading Video...',
      'video_completed': 'Video Completed',
      'video_failed': 'Video Failed',
      'playlist_completed': 'Playlist Completed'
    };
    return statusMap[status] || status;
  }

  private formatBytes(bytes: number): string {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

  private formatTime(seconds: number): string {
    if (seconds < 60) return `${Math.round(seconds)}s`;
    if (seconds < 3600) return `${Math.round(seconds / 60)}m`;
    return `${Math.round(seconds / 3600)}h`;
  }

  private showStatus(message: string, type: 'info' | 'success' | 'error' | 'warning'): void {
    const statusElement = this.element.querySelector('#statusMessage') as HTMLElement;

    const typeClasses = {
      info: 'bg-blue-900/20 text-blue-200 border-blue-700/50',
      success: 'bg-success-900/20 text-success-200 border-success-700/50',
      error: 'bg-error-900/20 text-error-200 border-error-700/50',
      warning: 'bg-warning-900/20 text-warning-200 border-warning-700/50'
    };

    statusElement.className = `p-4 rounded-md border ${typeClasses[type]} animate-fade-in`;
    statusElement.textContent = message;
    statusElement.classList.remove('hidden');

    // Auto-hide after 5 seconds
    setTimeout(() => {
      statusElement.classList.add('hidden');
    }, 5000);
  }

  public onDownloadStarted(callback: () => void): void {
    this.onDownloadStartedCallback = callback;
  }
}
