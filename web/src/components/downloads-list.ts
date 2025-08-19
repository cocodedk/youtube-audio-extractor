import { ApiService } from '../services/api-service';

export class DownloadsList {
  public element: HTMLElement;
  private apiService: ApiService;
  private allDownloads: any[] = [];
  private filteredDownloads: any[] = [];

  constructor() {
    this.apiService = new ApiService();
    this.element = this.createDownloadsList();
    this.setupEventListeners();
  }

  private createDownloadsList(): HTMLElement {
    const container = document.createElement('div');
    container.className = 'card';

    container.innerHTML = `
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-xl font-semibold text-gray-100">Downloads</h2>
          <p class="text-gray-400">View and manage your downloaded audio files</p>
        </div>
        <button id="refreshBtn" class="btn-secondary">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          Refresh
        </button>
      </div>

      <!-- Search Filter -->
      <div class="mb-6">
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          <input
            type="text"
            id="searchInput"
            class="input pl-10 pr-4"
            placeholder="Search downloads by name, type, or date..."
          >
        </div>
        <div class="mt-2 flex items-center justify-between text-sm">
          <span id="searchResults" class="text-gray-400">
            Showing all downloads
          </span>
          <button id="clearSearchBtn" class="text-primary-400 hover:text-primary-300 hidden">
            Clear search
          </button>
        </div>
      </div>

      <div id="downloadsContent" class="space-y-4">
        <!-- Downloads will be populated here -->
        <div class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2z"></path>
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-300">No downloads yet</h3>
          <p class="mt-1 text-sm text-gray-500">Start downloading audio files to see them here</p>
        </div>
      </div>
    `;

    return container;
  }

  private setupEventListeners(): void {
    const refreshBtn = this.element.querySelector('#refreshBtn') as HTMLButtonElement;
    const searchInput = this.element.querySelector('#searchInput') as HTMLInputElement;
    const clearSearchBtn = this.element.querySelector('#clearSearchBtn') as HTMLButtonElement;

    refreshBtn.addEventListener('click', () => {
      this.refreshDownloads();
    });

    // Search input event listener
    searchInput.addEventListener('input', (e) => {
      const query = (e.target as HTMLInputElement).value.trim();
      this.filterDownloads(query);
    });

    // Clear search button
    clearSearchBtn.addEventListener('click', () => {
      searchInput.value = '';
      this.filterDownloads('');
    });
  }

  public async refreshDownloads(): Promise<void> {
    try {
      const response = await this.apiService.getDownloads();
      // Extract the downloads array from the response
      this.allDownloads = response.downloads || [];
      this.filteredDownloads = [...this.allDownloads];
      this.renderDownloads();
    } catch (error) {
      this.showError(`Failed to load downloads: ${error}`);
    }
  }

  private filterDownloads(query: string): void {
    if (!query) {
      this.filteredDownloads = [...this.allDownloads];
      this.updateSearchResults();
      this.renderDownloads();
      return;
    }

    const lowerQuery = query.toLowerCase();
    this.filteredDownloads = this.allDownloads.filter(item => {
      // Search in name
      if (item.name.toLowerCase().includes(lowerQuery)) {
        return true;
      }

      // Search in type
      if (item.type.toLowerCase().includes(lowerQuery)) {
        return true;
      }

      // Search in file count (for folders)
      if (item.type === 'folder' && item.mp3_count !== undefined) {
        if (item.mp3_count.toString().includes(lowerQuery)) {
          return true;
        }
      }

      // Search in file size (for files)
      if (item.type === 'file' && item.size !== undefined) {
        const sizeText = this.formatFileSize(item.size).toLowerCase();
        if (sizeText.includes(lowerQuery)) {
          return true;
        }
      }

      // Search in date
      const date = new Date(item.modified * 1000).toLocaleDateString().toLowerCase();
      if (date.includes(lowerQuery)) {
        return true;
      }

      return false;
    });

    this.updateSearchResults();
    this.renderDownloads();
  }

  private updateSearchResults(): void {
    const searchResults = this.element.querySelector('#searchResults') as HTMLElement;
    const clearSearchBtn = this.element.querySelector('#clearSearchBtn') as HTMLButtonElement;
    const searchInput = this.element.querySelector('#searchInput') as HTMLInputElement;

    if (searchInput.value.trim()) {
      searchResults.textContent = `Showing ${this.filteredDownloads.length} of ${this.allDownloads.length} downloads`;
      clearSearchBtn.classList.remove('hidden');
    } else {
      searchResults.textContent = `Showing all downloads`;
      clearSearchBtn.classList.add('hidden');
    }
  }

  private renderDownloads(): void {
    const contentElement = this.element.querySelector('#downloadsContent') as HTMLElement;

    if (!this.filteredDownloads || this.filteredDownloads.length === 0) {
      const searchInput = this.element.querySelector('#searchInput') as HTMLInputElement;
      const hasSearchQuery = searchInput.value.trim().length > 0;

      if (hasSearchQuery) {
        contentElement.innerHTML = `
          <div class="text-center py-8">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-300">No results found</h3>
            <p class="mt-1 text-sm text-gray-500">Try adjusting your search terms</p>
          </div>
        `;
      } else {
        contentElement.innerHTML = `
          <div class="text-center py-8">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2z"></path>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-300">No downloads yet</h3>
            <p class="mt-1 text-sm text-gray-500">Start downloading audio files to see them here</p>
          </div>
        `;
      }
      return;
    }

    const downloadsHtml = this.filteredDownloads.map(item => {
      if (item.type === 'folder') {
        return this.renderFolderItem(item);
      } else {
        return this.renderFileItem(item);
      }
    }).join('');

    contentElement.innerHTML = downloadsHtml;

    // Add event listeners to the newly created open folder buttons
    this.setupOpenFolderListeners();
  }

  private renderFileItem(file: any): string {
    const size = this.formatFileSize(file.size);
    const date = new Date(file.modified * 1000).toLocaleDateString();

    return `
      <div class="flex items-center justify-between p-4 bg-dark-700 rounded-lg border border-dark-600 hover:bg-dark-600 transition-colors">
        <div class="flex items-center space-x-3">
          <div class="flex-shrink-0">
            <svg class="w-8 h-8 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2z"></path>
            </svg>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-200">${this.escapeHtml(file.name)}</h3>
            <p class="text-xs text-gray-400">${size} • ${date}</p>
          </div>
        </div>
        <div class="flex items-center space-x-2">
          <span class="badge badge-info">MP3</span>
          <button class="open-folder-btn btn-secondary text-xs px-3 py-1" data-path="downloads" title="Open downloads folder">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z"></path>
            </svg>
            Open
          </button>
        </div>
      </div>
    `;
  }

  private renderFolderItem(folder: any): string {
    const date = new Date(folder.modified * 1000).toLocaleDateString();
    const fileCount = folder.mp3_count || 0;

    return `
      <div class="flex items-center justify-between p-4 bg-dark-700 rounded-lg border border-dark-600 hover:bg-dark-600 transition-colors">
        <div class="flex items-center space-x-3">
          <div class="flex-shrink-0">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z"></path>
            </svg>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-200">${this.escapeHtml(folder.name)}</h3>
            <p class="text-xs text-gray-400">${fileCount} MP3 file${fileCount !== 1 ? 's' : ''} • ${date}</p>
          </div>
        </div>
        <div class="flex items-center space-x-2">
          <span class="badge badge-info">Folder</span>
          <button class="open-folder-btn btn-secondary text-xs px-3 py-1" data-path="downloads/${folder.name}" title="Open folder in file browser">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 00-2-2H9a2 2 0 00-2-2z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z"></path>
            </svg>
            Open
          </button>
        </div>
      </div>
    `;
  }

  private setupOpenFolderListeners(): void {
    const openFolderButtons = this.element.querySelectorAll('.open-folder-btn');

    openFolderButtons.forEach(button => {
      button.addEventListener('click', async (e) => {
        const target = e.target as HTMLElement;
        const buttonElement = target.closest('.open-folder-btn') as HTMLButtonElement;
        if (buttonElement) {
          const path = buttonElement.dataset.path;
          if (path) {
            await this.openFolder(path);
          }
        }
      });
    });
  }

  private async openFolder(path: string): Promise<void> {
    try {
      const button = this.element.querySelector(`[data-path="${path}"]`) as HTMLButtonElement;
      if (button) {
        button.disabled = true;
        button.innerHTML = `
          <svg class="w-4 h-4 mr-1 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          Opening...
        `;
      }

      await this.apiService.openFolder(path);

      // Show success message
      this.showSuccess(`Opened folder: ${path}`);

    } catch (error) {
      this.showError(`Failed to open folder: ${error}`);
    } finally {
      // Reset button state
      const button = this.element.querySelector(`[data-path="${path}"]`) as HTMLButtonElement;
      if (button) {
        button.disabled = false;
        button.innerHTML = `
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 00-2-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z"></path>
          </svg>
          Open
        `;
      }
    }
  }

  private formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

  private escapeHtml(text: string): string {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  private showSuccess(message: string): void {
    // Show a temporary success message
    const successElement = document.createElement('div');
    successElement.className = 'fixed top-4 right-4 bg-success-900/90 text-success-200 px-4 py-2 rounded-md shadow-lg z-50 animate-fade-in';
    successElement.textContent = message;

    document.body.appendChild(successElement);

    setTimeout(() => {
      successElement.remove();
    }, 3000);
  }

  private showError(message: string): void {
    const contentElement = this.element.querySelector('#downloadsContent') as HTMLElement;
    contentElement.innerHTML = `
      <div class="text-center py-8">
        <svg class="mx-auto h-12 w-12 text-error-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h3 class="mt-2 text-sm font-medium text-error-300">Error loading downloads</h3>
        <p class="mt-1 text-sm text-error-200">${message}</p>
        <button class="mt-4 btn-secondary" onclick="this.parentElement.parentElement.parentElement.querySelector('#refreshBtn').click()">
          Try Again
        </button>
      </div>
    `;
  }
}
