#!/usr/bin/env python3
"""
Flask web application for YouTube Audio Extractor
Provides a REST API for the web UI
"""

import os
from pathlib import Path
from flask import Flask, send_from_directory, send_file
from flask_cors import CORS

# Import all blueprint modules
from api.downloads import downloads_bp
from api.progress import progress_bp
from api.utils import utils_bp

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8080", "http://127.0.0.1:8080"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Register all blueprints
app.register_blueprint(downloads_bp)
app.register_blueprint(progress_bp)
app.register_blueprint(utils_bp)

# Serve static files from the built frontend
@app.route('/')
def serve_index():
    """Serve the main index.html file"""
    dist_dir = Path('web/dist')
    if dist_dir.exists():
        return send_file(dist_dir / 'index.html')
    else:
        return """
        <h1>YouTube Audio Extractor</h1>
        <p>Frontend not built yet. Please run:</p>
        <pre>cd web && npm run build</pre>
        <p>Or use development mode with: <code>./start_ui.sh</code></p>
        """, 200

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from the dist directory"""
    dist_dir = Path('web/dist')
    if dist_dir.exists():
        return send_from_directory(str(dist_dir), filename)
    else:
        # Fallback to index.html for client-side routing
        return serve_index()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)  # Disable auto-reload temporarily for debugging
