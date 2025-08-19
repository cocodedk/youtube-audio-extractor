export class About {
  public element: HTMLElement;

  constructor() {
    this.element = this.createAbout();
  }

  private createAbout(): HTMLElement {
    const container = document.createElement('div');
    container.className = 'card';

    container.innerHTML = `
      <div class="text-center mb-8">
        <div class="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2z"></path>
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-100 mb-2">YouTube Audio Extractor</h1>
        <p class="text-xl text-gray-400">Professional Audio Extraction Tool</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <!-- Project Description -->
        <div class="space-y-4">
          <h2 class="text-xl font-semibold text-gray-100">About This Project</h2>
          <p class="text-gray-300 leading-relaxed">
            YouTube Audio Extractor is a powerful, open-source tool designed for extracting high-quality audio from YouTube videos and playlists. Built with modern web technologies and a focus on user experience.
          </p>
          <p class="text-gray-300 leading-relaxed">
            Whether you're a content creator, music enthusiast, or educator, this tool provides professional-grade audio extraction with advanced features like chapter splitting, bitrate control, and playlist management.
          </p>
        </div>

        <!-- Key Features -->
        <div class="space-y-4">
          <h2 class="text-xl font-semibold text-gray-100">Key Features</h2>
          <ul class="space-y-2 text-gray-300">
            <li class="flex items-center">
              <svg class="w-5 h-5 text-primary-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
              High-quality audio extraction (32-320 kbps)
            </li>
            <li class="flex items-center">
              <svg class="w-5 h-5 text-primary-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
              Playlist support with range selection
            </li>
            <li class="flex items-center">
              <svg class="w-5 h-5 text-primary-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
              Chapter-based audio splitting
            </li>
            <li class="flex items-center">
              <svg class="w-5 h-5 text-primary-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
              Modern dark-themed web interface
            </li>
            <li class="flex items-center">
              <svg class="w-5 h-5 text-primary-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
              Cross-platform file browser integration
            </li>
          </ul>
        </div>
      </div>

      <!-- Technology Stack -->
      <div class="mb-8">
        <h2 class="text-xl font-semibold text-gray-100 mb-4">Technology Stack</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-dark-700 rounded-lg p-4 text-center border border-dark-600">
            <div class="text-primary-400 font-semibold">Backend</div>
            <div class="text-gray-300 text-sm">Python + Flask</div>
          </div>
          <div class="bg-dark-700 rounded-lg p-4 text-center border border-dark-600">
            <div class="text-primary-400 font-semibold">Frontend</div>
            <div class="text-gray-300 text-sm">TypeScript + Tailwind</div>
          </div>
          <div class="bg-dark-700 rounded-lg p-4 text-center border border-dark-600">
            <div class="text-primary-400 font-semibold">Audio</div>
            <div class="text-gray-300 text-sm">yt-dlp + FFmpeg</div>
          </div>
          <div class="bg-dark-700 rounded-lg p-4 text-center border border-dark-600">
            <div class="text-primary-400 font-semibold">Build</div>
            <div class="text-gray-300 text-sm">Webpack + PostCSS</div>
          </div>
        </div>
      </div>

      <!-- Links and Credits -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Project Links -->
        <div class="space-y-4">
          <h2 class="text-xl font-semibold text-gray-100">Project Links</h2>
          <div class="space-y-3">
            <a href="https://github.com/your-repo/youtube-audio-extractor"
               target="_blank"
               rel="noopener noreferrer"
               class="flex items-center text-primary-400 hover:text-primary-300 transition-colors">
              <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 4.624-5.479 4.833.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              GitHub Repository
            </a>
            <a href="https://pypi.org/project/youtube-audio-extractor/"
               target="_blank"
               rel="noopener noreferrer"
               class="flex items-center text-primary-400 hover:text-primary-300 transition-colors">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
              </svg>
              PyPI Package
            </a>
            <a href="https://github.com/your-repo/youtube-audio-extractor/issues"
               target="_blank"
               rel="noopener noreferrer"
               class="flex items-center text-primary-400 hover:text-primary-300 transition-colors">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Report Issues
            </a>
          </div>
        </div>

        <!-- Credits and Support -->
        <div class="space-y-4">
          <h2 class="text-xl font-semibold text-gray-100">Credits & Support</h2>
          <div class="space-y-3">
            <div class="flex items-center text-gray-300">
              <svg class="w-5 h-5 mr-2 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
              <span>Developed with ❤️ by the community</span>
            </div>
            <div class="flex items-center text-gray-300">
              <svg class="w-5 h-5 mr-2 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
              <span>Powered by yt-dlp & FFmpeg</span>
            </div>
            <div class="flex items-center text-gray-300">
              <svg class="w-5 h-5 mr-2 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>MIT License with Attribution</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Special Thanks -->
      <div class="mt-8 p-6 bg-gradient-to-r from-primary-900/20 to-blue-900/20 rounded-lg border border-primary-700/30">
        <h2 class="text-xl font-semibold text-gray-100 mb-4 text-center">Special Thanks</h2>
        <div class="text-center">
          <p class="text-gray-300 mb-4">
            This project is proudly supported and developed in collaboration with
          </p>
          <a href="https://cocode.dk"
             target="_blank"
             rel="noopener noreferrer"
             class="inline-flex items-center text-2xl font-bold text-primary-400 hover:text-primary-300 transition-colors">
            <svg class="w-8 h-8 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path>
            </svg>
            cocode.dk
          </a>
          <p class="text-gray-400 text-sm mt-2">
            Empowering developers with innovative solutions
          </p>
        </div>
      </div>

      <!-- Version Info -->
      <div class="mt-8 text-center text-gray-500 text-sm">
        <p>Version 1.0.0 • Built with modern web technologies</p>
        <p class="mt-1">© 2025 YouTube Audio Extractor Project</p>
      </div>
    `;

    return container;
  }
}
