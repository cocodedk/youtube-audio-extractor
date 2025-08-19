#!/usr/bin/env python3
"""
Flask web application for YouTube Audio Extractor
Provides a REST API for the web UI
"""

from flask import Flask
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

# Frontend is served by Webpack dev server in development
# No need to serve or redirect from Flask

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)  # Disable auto-reload temporarily for debugging
