export class ProgressBar {
  private element: HTMLElement;
  private currentDownloadId: string | null = null;
  private progressEventSource: EventSource | null = null;
  private completionEmitted: boolean = false;
  private lastProgressData: any = null;

  constructor(container: HTMLElement) {
    this.element = container;
    this.setupEventListeners();
  }

  public show(): void {
    const progressContainer = this.element.querySelector('#progressContainer') as HTMLElement;
    if (progressContainer) {
      progressContainer.classList.remove('hidden');
    }
  }

  public hide(): void {
    const progressContainer = this.element.querySelector('#progressContainer') as HTMLElement;
    if (progressContainer) {
      progressContainer.classList.add('hidden');
    }
  }

  public showPlaylistProgress(): void {
    const playlistProgress = this.element.querySelector('#playlistProgress') as HTMLElement;
    playlistProgress.classList.remove('hidden');
  }

  public startProgressTracking(downloadId: string): void {
    this.currentDownloadId = downloadId;
    this.completionEmitted = false; // Reset completion flag for new download

    // Close existing connection
    if (this.progressEventSource) {
      this.progressEventSource.close();
    }

    // Create new EventSource connection
    const progressUrl = `http://localhost:5000/api/progress/${downloadId}`;


    try {
      this.progressEventSource = new EventSource(progressUrl);

      this.progressEventSource.onopen = (event) => {
        // Connection established successfully
      };

            this.progressEventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.updateProgress(data);
        } catch (error) {
          console.error('Error parsing progress data:', error);
        }
      };

      this.progressEventSource.onerror = (error) => {
        console.error('Progress tracking error:', error);

        // If the connection is closed and we get an error, it might mean the download is complete
        // and the backend has cleaned up the download ID
        if (this.progressEventSource && this.progressEventSource.readyState === EventSource.CLOSED) {
          // Check if we should treat this as completion (download ID no longer exists)
          // This prevents infinite reconnection attempts for completed downloads
          if (this.currentDownloadId) {
            this.stopSpinners();

            // Emit completion event (treat as success since the download likely completed)
            this.element.dispatchEvent(new CustomEvent('downloadCompleted', {
              detail: {
                success: true,
                data: { status: 'completed', message: 'Download completed (connection closed)' }
              }
            }));
          }
        }
      };
    } catch (error) {
      console.error('Error creating EventSource:', error);
    }
  }

  public updateProgress(data: any): void {
    // Store the latest progress data for status checking
    this.lastProgressData = data;

    // Handle heartbeat
    if (data.heartbeat) {
      return;
    }



    // Check for error responses from backend (like "Download not found")
    if (data.error) {
      this.stopSpinners();

      // Emit completion event with error status
      this.element.dispatchEvent(new CustomEvent('downloadCompleted', {
        detail: {
          success: false,
          data: { status: 'error', message: data.error }
        }
      }));
      return;
    }

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
        stepText.className = 'text-sm text-gray-300';
      } else if (data.status === 'failed') {
        progressStatus.className = 'text-sm text-red-400';
        stepText.className = 'text-sm text-gray-300';
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

        // Handle completion or failure - stop spinners and emit event
    if (data.status === 'completed' || data.status === 'failed' || data.status === 'error') {
      this.stopSpinners();
      this.completionEmitted = true;

      // Close EventSource connection to prevent reconnection
      if (this.progressEventSource) {
        this.progressEventSource.close();
        this.progressEventSource = null;
      }

      // Emit completion event to parent component
      this.element.dispatchEvent(new CustomEvent('downloadCompleted', {
        detail: {
          success: data.status === 'completed',
          data: data
        }
      }));
    }

    // Handle stream end signal - close connection gracefully
    if (data.status === 'end') {
      // If we haven't emitted completion yet, emit it now
      // This handles the case where "end" comes before "completed"
      if (!this.completionEmitted) {
        this.completionEmitted = true;
        this.stopSpinners();

        // Emit completion event to parent component
        this.element.dispatchEvent(new CustomEvent('downloadCompleted', {
          detail: {
            success: true, // Assume success if we got to end
            data: { status: 'completed', message: 'Download completed' }
          }
        }));
      }

      this.closeConnection();
    }
  }

    private stopSpinners(): void {
    // Stop ALL spinning animations in the progress container
    const allSpinners = this.element.querySelectorAll('svg.animate-spin');

    allSpinners.forEach((spinner) => {
      // Replace spinner with appropriate icon based on status
      const status = this.element.querySelector('#progressStatus')?.textContent;

      // Check both the DOM status and the data passed to updateProgress
      const isSuccess = status?.includes('completed') || status?.includes('success') ||
                       (this.lastProgressData && this.lastProgressData.status === 'completed');

      if (isSuccess) {
        spinner.outerHTML = `
          <svg class="w-4 h-4 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
        `;
      } else {
        spinner.outerHTML = `
          <svg class="w-4 h-4 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
          </svg>
        `;
      }
    });

    // Also remove animate-spin class from any remaining elements
    const animatedElements = this.element.querySelectorAll('.animate-spin');
    animatedElements.forEach((element) => {
      element.classList.remove('animate-spin');
    });
  }

  private updatePlaylistProgress(currentVideo: number, totalVideos: number): void {
    const videoProgress = this.element.querySelector('#videoProgress') as HTMLElement;
    const videoProgressBar = this.element.querySelector('#videoProgressBar') as HTMLElement;

    videoProgress.textContent = `${currentVideo} / ${totalVideos}`;
    const percent = (currentVideo / totalVideos) * 100;
    videoProgressBar.style.width = `${percent}%`;
  }

  public closeConnection(): void {
    if (this.progressEventSource) {
      this.progressEventSource.close();
      this.progressEventSource = null;
    }
    this.currentDownloadId = null;
  }

  public getCurrentDownloadId(): string | null {
    return this.currentDownloadId;
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

  private setupEventListeners(): void {
    // Close progress button
    const closeProgressBtn = this.element.querySelector('#closeProgressBtn') as HTMLButtonElement;
    if (closeProgressBtn) {
      closeProgressBtn.addEventListener('click', () => {
        this.hide();
        this.closeConnection();
      });
    }
  }
}
