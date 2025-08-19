# YouTube Audio Extractor - Web Frontend

This is the web frontend for the YouTube Audio Extractor application, built with TypeScript, Tailwind CSS, and Webpack.

## Features

- **Modern UI**: Clean, responsive design with Tailwind CSS
- **TypeScript**: Full type safety and modern JavaScript features
- **Component-based**: Modular architecture for easy maintenance
- **Real-time updates**: Live status updates and progress tracking
- **Mobile responsive**: Works on all device sizes

## Development

### Prerequisites

- Node.js 16+ and npm
- Python 3.7+ with Flask dependencies

### Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

   This will start Webpack dev server on port 3000 with hot reloading.

3. **Build for production:**
   ```bash
   npm run build
   ```

4. **Clean build artifacts:**
   ```bash
   npm run clean
   ```

## Project Structure

```
web/
├── src/
│   ├── components/          # UI components
│   │   ├── header.ts       # Application header
│   │   ├── tab-manager.ts  # Tab navigation
│   │   ├── download-form.ts # Download form
│   │   └── downloads-list.ts # Downloads display
│   ├── services/           # API services
│   │   └── api-service.ts  # HTTP client
│   ├── app.ts             # Main application class
│   ├── index.ts           # Entry point
│   ├── index.html         # HTML template
│   └── styles.css         # Global styles with Tailwind
├── dist/                  # Built files (generated)
├── package.json           # Dependencies and scripts
├── webpack.config.js      # Webpack configuration
├── tsconfig.json          # TypeScript configuration
├── tailwind.config.js     # Tailwind CSS configuration
└── postcss.config.js      # PostCSS configuration
```

## Development Workflow

1. **Start Flask backend** (from project root):
   ```bash
   python web_app.py
   ```

2. **Start frontend dev server** (in web/ directory):
   ```bash
   npm run dev
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000/api/

## Building for Production

The production build process:

1. **Build frontend:**
   ```bash
   npm run build
   ```

2. **Start Flask server:**
   ```bash
   python web_app.py
   ```

3. **Access production app:**
   - Web UI: http://localhost:5000
   - API: http://localhost:5000/api/

## Architecture

### Components

- **Header**: Application branding and navigation
- **TabManager**: Tab-based navigation between views
- **DownloadForm**: Form for video/playlist downloads
- **DownloadsList**: Display of downloaded files

### Services

- **ApiService**: HTTP client for backend communication
- Handles all API calls with proper error handling
- Supports both development and production environments

### Styling

- **Tailwind CSS**: Utility-first CSS framework
- **Custom components**: Reusable UI components
- **Responsive design**: Mobile-first approach
- **Dark mode ready**: CSS variables for theming

## API Integration

The frontend communicates with the Flask backend through:

- **REST API**: Standard HTTP endpoints
- **JSON**: Data exchange format
- **Error handling**: Graceful fallbacks and user feedback
- **Real-time updates**: Status messages and progress indicators

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development Tips

1. **Hot reloading**: Changes to TypeScript files automatically refresh the browser
2. **Type safety**: Use TypeScript interfaces for API responses
3. **Component isolation**: Each component manages its own state and events
4. **Error boundaries**: Graceful error handling throughout the application
5. **Accessibility**: ARIA labels and keyboard navigation support

## Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 3000 and 5000 are available
2. **Build errors**: Check TypeScript compilation and Webpack configuration
3. **API errors**: Verify Flask backend is running and accessible
4. **Styling issues**: Ensure Tailwind CSS is properly configured

### Debug Mode

Enable debug logging in the browser console for detailed error information and API call tracking.
