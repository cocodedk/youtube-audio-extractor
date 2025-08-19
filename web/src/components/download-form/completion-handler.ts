import { ApiService } from '../../services/api-service';

export class CompletionHandler {
  private element: HTMLElement;
  private apiService: ApiService;
  private currentDownloadId: string | null = null;

  constructor(container: HTMLElement, apiService: ApiService) {
    this.element = container;
    this.apiService = apiService;
  }

  public setDownloadId(downloadId: string): void {
    this.currentDownloadId = downloadId;
  }

  public handleDownloadComplete(success: boolean): void {

    if (success) {
      // Show success message with option to open file location
      this.showSuccessMessage();
    } else {
      // Show error message
      this.showErrorMessage();
    }
  }

  private showSuccessMessage(): void {
    const progressContainer = this.element.querySelector('#progressContainer') as HTMLElement;

    // Remove any existing success message
    const existingMessage = progressContainer.querySelector('.bg-green-100');
    if (existingMessage) {
      existingMessage.remove();
    }

    // Create success message with open folder button
    const successMessage = document.createElement('div');
    successMessage.className = 'bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4';
    successMessage.innerHTML = `
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          <span class="font-medium">Download completed successfully!</span>
        </div>
        <div class="flex items-center space-x-2">
          <button id="openFolderBtn" class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm">
            📁 Open Folder
          </button>
          <button id="closeSuccessBtn" class="bg-gray-500 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm">
            ✕ Close
          </button>
        </div>
      </div>
    `;

    // Insert success message at the top of progress container
    progressContainer.insertBefore(successMessage, progressContainer.firstChild);

    // Add event listener for open folder button
    const openFolderBtn = successMessage.querySelector('#openFolderBtn') as HTMLButtonElement;
    openFolderBtn.addEventListener('click', () => this.openDownloadsFolder());

    // Add event listener for close button
    const closeBtn = successMessage.querySelector('#closeSuccessBtn') as HTMLButtonElement;
    closeBtn.addEventListener('click', () => {
      this.hideProgressBar();
      this.currentDownloadId = null; // Reset ID only when user closes
    });
  }

  private showErrorMessage(): void {
    const progressContainer = this.element.querySelector('#progressContainer') as HTMLElement;

    // Remove any existing error message
    const existingMessage = progressContainer.querySelector('.bg-red-100');
    if (existingMessage) {
      existingMessage.remove();
    }

    // Create error message with close button
    const errorMessage = document.createElement('div');
    errorMessage.className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4';
    errorMessage.innerHTML = `
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
          </svg>
          <span class="font-medium">Download failed. Check the console for details.</span>
        </div>
        <button id="closeErrorBtn" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm">
          ✕ Close
        </button>
      </div>
    `;

    // Insert error message at the top of progress container
    progressContainer.insertBefore(errorMessage, progressContainer.firstChild);

    // Add event listener for close button
    const closeBtn = errorMessage.querySelector('#closeErrorBtn') as HTMLButtonElement;
    closeBtn.addEventListener('click', () => {
      this.hideProgressBar();
      this.currentDownloadId = null; // Reset ID only when user closes
    });
  }

  private async openDownloadsFolder(): Promise<void> {
    if (!this.currentDownloadId) {
      console.error('No download ID available');
      return;
    }

    try {
      // Get download location from backend
      const locationInfo = await this.apiService.getDownloadLocation(this.currentDownloadId);

      if (locationInfo.downloads_dir) {
        // Open file browser to downloads folder
        this.openFolderInSystem(locationInfo.downloads_dir);
      } else {
        console.error('Could not get download location');
      }
    } catch (error) {
      console.error('Error getting download location:', error);
      // Fallback: try to open the downloads folder directly
      this.openFolderInSystem('downloads');
    }
  }

  private openFolderInSystem(folderPath: string): void {
    // Try to open folder using system-specific commands
    if (navigator.platform.includes('Win')) {
      // Windows - try to open with file explorer
      try {
        window.open(`file:///${folderPath.replace(/\\/g, '/')}`);
      } catch (e) {
        this.showFolderPathDialog(folderPath);
      }
    } else if (navigator.platform.includes('Mac')) {
      // macOS - try to open with Finder
      try {
        window.open(`file://${folderPath}`);
      } catch (e) {
        this.showFolderPathDialog(folderPath);
      }
    } else {
      // Linux and other Unix-like systems
      // Browsers can't directly open file managers due to security restrictions
      this.showFolderPathDialog(folderPath);
    }
  }

  private showFolderPathDialog(folderPath: string): void {
    // Create a better dialog than alert() for showing the folder path
    const dialog = document.createElement('div');
    dialog.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    dialog.innerHTML = `
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md mx-4 shadow-xl">
        <div class="flex items-center mb-4">
          <svg class="w-6 h-6 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Download Complete!</h3>
        </div>
        <p class="text-gray-600 dark:text-gray-300 mb-4">Your file has been saved to:</p>
        <div class="bg-gray-100 dark:bg-gray-700 p-3 rounded border mb-4">
          <code class="text-sm text-gray-800 dark:text-gray-200 break-all" id="folderPath">${folderPath}</code>
        </div>
        <div class="flex space-x-3">
          <button id="copyPathBtn" class="flex-1 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium">
            📋 Copy Path
          </button>
          <button id="closeDialogBtn" class="flex-1 bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded text-sm font-medium">
            Close
          </button>
        </div>
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-3">
          💡 Tip: Open your file manager and paste this path in the address bar
        </p>
      </div>
    `;

    document.body.appendChild(dialog);

    // Add event listeners
    const copyBtn = dialog.querySelector('#copyPathBtn') as HTMLButtonElement;
    const closeBtn = dialog.querySelector('#closeDialogBtn') as HTMLButtonElement;
    const pathElement = dialog.querySelector('#folderPath') as HTMLElement;

    copyBtn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(folderPath);
        copyBtn.innerHTML = '✅ Copied!';
        copyBtn.classList.remove('bg-blue-500', 'hover:bg-blue-600');
        copyBtn.classList.add('bg-green-500', 'hover:bg-green-600');
        setTimeout(() => {
          copyBtn.innerHTML = '📋 Copy Path';
          copyBtn.classList.remove('bg-green-500', 'hover:bg-green-600');
          copyBtn.classList.add('bg-blue-500', 'hover:bg-blue-600');
        }, 2000);
      } catch (err) {
        // Fallback for older browsers
        pathElement.style.userSelect = 'all';
        const range = document.createRange();
        range.selectNode(pathElement);
        window.getSelection()?.removeAllRanges();
        window.getSelection()?.addRange(range);
        copyBtn.innerHTML = '📝 Selected - Press Ctrl+C';
      }
    });

    closeBtn.addEventListener('click', () => {
      document.body.removeChild(dialog);
    });

    // Close on background click
    dialog.addEventListener('click', (e) => {
      if (e.target === dialog) {
        document.body.removeChild(dialog);
      }
    });

    // Close on Escape key
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        document.body.removeChild(dialog);
        document.removeEventListener('keydown', handleEscape);
      }
    };
    document.addEventListener('keydown', handleEscape);
  }

  private hideProgressBar(): void {
    const progressContainer = this.element.querySelector('#progressContainer') as HTMLElement;
    if (progressContainer) {
      progressContainer.classList.add('hidden');
    }
  }
}
