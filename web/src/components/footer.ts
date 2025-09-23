export class Footer {
  public element: HTMLElement;

  constructor() {
    this.element = this.createFooter();
  }

  private createFooter(): HTMLElement {
    const footer = document.createElement('footer');
    footer.className = 'bg-dark-800 border-t border-dark-700 mt-auto';

    const container = document.createElement('div');
    container.className = 'container mx-auto px-4 py-6 max-w-6xl';

    const content = document.createElement('div');
    content.className = 'flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0';

    // Left side - App info
    const appInfo = document.createElement('div');
    appInfo.className = 'text-center sm:text-left';

    const appName = document.createElement('h3');
    appName.className = 'text-lg font-semibold text-gray-200 mb-1';
    appName.textContent = 'YouTube Audio Extractor';

    const appDescription = document.createElement('p');
    appDescription.className = 'text-sm text-gray-400';
    appDescription.textContent = 'Extract audio from YouTube videos and playlists';

    appInfo.appendChild(appName);
    appInfo.appendChild(appDescription);

    // Right side - Cocode link
    const cocodeLink = document.createElement('a');
    cocodeLink.href = 'https://cocode.dk';
    cocodeLink.target = '_blank';
    cocodeLink.rel = 'noopener noreferrer';
    cocodeLink.className = 'inline-flex items-center space-x-2 text-primary-400 hover:text-primary-300 transition-colors duration-200 group';

    const linkIcon = document.createElement('svg');
    linkIcon.className = 'w-4 h-4 group-hover:scale-110 transition-transform duration-200';
    linkIcon.setAttribute('fill', 'none');
    linkIcon.setAttribute('stroke', 'currentColor');
    linkIcon.setAttribute('viewBox', '0 0 24 24');
    linkIcon.innerHTML = `
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
    `;

    const linkText = document.createElement('span');
    linkText.className = 'text-sm font-medium';
    linkText.textContent = 'cocode.dk';

    cocodeLink.appendChild(linkIcon);
    cocodeLink.appendChild(linkText);

    // Copyright
    const copyright = document.createElement('div');
    copyright.className = 'text-xs text-gray-500 text-center sm:text-right mt-2 sm:mt-0';
    copyright.innerHTML = '© 2025 YouTube Audio Extractor. Made with ❤️ by <a href="https://cocode.dk" target="_blank" rel="noopener noreferrer" class="text-primary-400 hover:text-primary-300 transition-colors duration-200">Cocode</a>';

    content.appendChild(appInfo);
    content.appendChild(cocodeLink);

    container.appendChild(content);
    container.appendChild(copyright);
    footer.appendChild(container);

    return footer;
  }
}
