import { ApiService } from '../../services/api-service';
import { ProgressBar } from './progress-bar';
import { CompletionHandler } from './completion-handler';
import { TestUtils } from './test-utils';

export class DownloadForm {
  public element: HTMLElement;
  private apiService: ApiService;
  private onDownloadStartedCallback?: () => void;
  private isDownloading: boolean = false;
  private currentMode: 'download' | 'playlist' = 'download';

  // Component instances
  private progressBar: ProgressBar;
  private completionHandler: CompletionHandler;
  private testUtils: TestUtils;

  constructor() {
    this.apiService = new ApiService();
    this.element = this.createDownloadForm();

    // Initialize components
    this.progressBar = new ProgressBar(this.element);
    this.completionHandler = new CompletionHandler(this.element, this.apiService);
    this.testUtils = new TestUtils(this.element, this.apiService);

    this.setupEventListeners();
    this.setupTestEventListeners();
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
              <div class="flex items-center space-x-2">
                <span id="progressStatus" class="text-sm text-gray-400">Initializing...</span>
                <button id="closeProgressBtn" class="text-gray-400 hover:text-white p-1 rounded">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </div>
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
      this.testUtils.testProgressBar();
    });
  }

  private setupTestEventListeners(): void {
    // Listen for test events
    this.element.addEventListener('testDownloadStarted', ((event: CustomEvent) => {
      const { downloadId } = event.detail;
      this.progressBar.startProgressTracking(downloadId);
      this.completionHandler.setDownloadId(downloadId);
    }) as EventListener);

    this.element.addEventListener('testProgressUpdate', ((event: CustomEvent) => {
      const { data } = event.detail;
      this.progressBar.updateProgress(data);

      // Handle completion
      if (data.status === 'completed' || data.status === 'failed' || data.status === 'error') {
        this.completionHandler.handleDownloadComplete(data.status === 'completed');
      }
    }) as EventListener);

        // Listen for real download completion events from ProgressBar
    this.element.addEventListener('downloadCompleted', ((event: CustomEvent) => {
      const { success, data } = event.detail;

      // Don't call updateProgress again - it already handled the completion
      // Just handle the completion UI
      this.completionHandler.handleDownloadComplete(success);

      // Re-enable buttons after completion
      this.setDownloadingState(false);
    }) as EventListener);
  }

  private async handleDownload(): Promise<void> {
    if (this.isDownloading) return;

    const formData = this.getFormData();
    if (!formData.url) return;

    this.setDownloadingState(true);
    this.showStatus('Starting download...', 'info');

    try {
      const response = await this.apiService.downloadVideo(formData);
      this.showStatus('Download started successfully!', 'success');
      this.progressBar.show();
      this.progressBar.startProgressTracking(response.download_id);
      this.completionHandler.setDownloadId(response.download_id);

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
      this.showStatus('Playlist download started successfully!', 'success');
      this.progressBar.show();
      this.progressBar.startProgressTracking(response.download_id);
      this.progressBar.showPlaylistProgress();
      this.completionHandler.setDownloadId(response.download_id);

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
