export class TabManager {
  public element: HTMLElement;
  private activeTab: string = 'download';
  private onTabChangeCallback?: (tab: string) => void;

  constructor() {
    this.element = this.createTabManager();
    this.setupEventListeners();
  }

  private createTabManager(): HTMLElement {
    const container = document.createElement('div');
    container.className = 'mb-8';

    container.innerHTML = `
      <div class="border-b border-dark-700">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
          <button class="tab-button active" data-tab="download">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            Download
          </button>
          <button class="tab-button" data-tab="playlist">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path>
            </svg>
            Playlist
          </button>
          <button class="tab-button" data-tab="downloads">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z"></path>
            </svg>
            Downloads
          </button>
          <button class="tab-button" data-tab="about">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            About
          </button>
        </nav>
      </div>
    `;

    return container;
  }

  private setupEventListeners(): void {
    const tabButtons = this.element.querySelectorAll('.tab-button');

    tabButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        const target = e.target as HTMLElement;
        const tabButton = target.closest('.tab-button') as HTMLElement;
        if (tabButton) {
          const tab = tabButton.dataset.tab;
          if (tab) {
            this.setActiveTab(tab);
          }
        }
      });
    });
  }

  private setActiveTab(tab: string): void {
    // Remove active class from all tabs
    const tabButtons = this.element.querySelectorAll('.tab-button');
    tabButtons.forEach(btn => btn.classList.remove('active'));

    // Add active class to selected tab
    const activeButton = this.element.querySelector(`[data-tab="${tab}"]`);
    if (activeButton) {
      activeButton.classList.add('active');
    }

    this.activeTab = tab;

    // Notify listeners
    if (this.onTabChangeCallback) {
      this.onTabChangeCallback(tab);
    }
  }

  public onTabChange(callback: (tab: string) => void): void {
    this.onTabChangeCallback = callback;
  }

  public getActiveTab(): string {
    return this.activeTab;
  }
}
