export class ApiService {
  private baseUrl: string = 'http://localhost:5000/api';

  async downloadVideo(data: any): Promise<any> {
    const response = await fetch(`${this.baseUrl}/download`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Download failed');
    }

    return response.json();
  }

  async downloadPlaylist(data: any): Promise<any> {
    const response = await fetch(`${this.baseUrl}/playlist`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Playlist download failed');
    }

    return response.json();
  }

  async getDownloads(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/downloads`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to fetch downloads');
    }

    return response.json();
  }

  async getDownloadsStatus(): Promise<any> {
    const response = await fetch('/api/downloads/status');
    return response.json();
  }

  async getDownloadLocation(downloadId: string): Promise<any> {
    const response = await fetch(`/api/downloads/${downloadId}/location`);
    return response.json();
  }

  async getChapters(url: string): Promise<any> {
    const encodedUrl = encodeURIComponent(url);
    const response = await fetch(`${this.baseUrl}/chapters/${encodedUrl}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to fetch chapters');
    }

    return response.json();
  }

  async getFormats(url: string): Promise<any> {
    const encodedUrl = encodeURIComponent(url);
    const response = await fetch(`${this.baseUrl}/formats/${encodedUrl}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to fetch formats');
    }

    return response.json();
  }

  async getBitrates(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/bitrates`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to fetch bitrates');
    }

    return response.json();
  }

  async openFolder(path: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/open-folder`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ path }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to open folder');
    }

    return response.json();
  }
}
