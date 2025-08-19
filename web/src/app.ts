import { Header } from './components/header';
import { TabManager } from './components/tab-manager';
import { DownloadForm } from './components/download-form';
import { DownloadsList } from './components/downloads-list';
import { About } from './components/about';

export class App {
  private container: HTMLElement;
  private header!: Header;
  private tabManager!: TabManager;
  private downloadForm!: DownloadForm;
  private downloadsList!: DownloadsList;
  private about!: About;
  private mainContainer!: HTMLElement;

  constructor(container: HTMLElement) {
    this.container = container;
    this.initializeApp();
  }

  private initializeApp(): void {
    // Create header
    this.header = new Header();
    this.container.appendChild(this.header.element);

    // Create main container
    this.mainContainer = document.createElement('main');
    this.mainContainer.className = 'container mx-auto px-4 py-8 max-w-6xl';

    // Create tab manager
    this.tabManager = new TabManager();
    this.mainContainer.appendChild(this.tabManager.element);

    // Create download form
    this.downloadForm = new DownloadForm();
    this.mainContainer.appendChild(this.downloadForm.element);

    // Create downloads list
    this.downloadsList = new DownloadsList();
    this.mainContainer.appendChild(this.downloadsList.element);

    // Create about page
    this.about = new About();
    this.mainContainer.appendChild(this.about.element);

    // Add main container to page
    this.container.appendChild(this.mainContainer);

    // Setup event listeners
    this.setupEventListeners();

    // Load initial data
    this.loadInitialData();
    this.updateTabVisibility();

    // Set initial form mode
    this.downloadForm.setMode('download');
  }

  private setupEventListeners(): void {
    // Listen for download completion
    this.downloadForm.onDownloadStarted(() => {
      // Refresh downloads list after a short delay
      setTimeout(() => {
        this.downloadsList.refreshDownloads();
      }, 2000);
    });

    // Listen for tab changes
    this.tabManager.onTabChange((activeTab: string) => {
      this.updateTabVisibility();

      // Update form mode based on active tab
      if (activeTab === 'download' || activeTab === 'playlist') {
        this.downloadForm.setMode(activeTab as 'download' | 'playlist');
      }

      if (activeTab === 'downloads') {
        this.downloadsList.refreshDownloads();
      }
    });
  }

  private loadInitialData(): void {
    // Load initial downloads
    this.downloadsList.refreshDownloads();
  }

  private updateTabVisibility(): void {
    const activeTab = this.tabManager.getActiveTab();

    // Show/hide components based on active tab
    if (activeTab === 'download' || activeTab === 'playlist') {
      this.downloadForm.element.style.display = 'block';
      this.downloadsList.element.style.display = 'none';
      this.about.element.style.display = 'none';
    } else if (activeTab === 'downloads') {
      this.downloadForm.element.style.display = 'none';
      this.downloadsList.element.style.display = 'block';
      this.about.element.style.display = 'none';
    } else if (activeTab === 'about') {
      this.downloadForm.element.style.display = 'none';
      this.downloadsList.element.style.display = 'none';
      this.about.element.style.display = 'block';
    }
  }
}
