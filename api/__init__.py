from flask import Flask
from api.routes import api

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/api')
    return app
