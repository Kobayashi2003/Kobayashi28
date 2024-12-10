from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
api = Api()
jwt = JWTManager()

def configure_cors(app):
    """Configure CORS for the application."""
    CORS(app, resources={r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    
    # ---------------------------
    # Load configuration
    app.config.from_object('app.config.active_config')

    # ---------------------------
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)
    configure_cors(app)

    # ---------------------------
    # Register routes
    from .routes import user_routes, image_routes
    api.add_namespace(user_routes.ns)
    api.add_namespace(image_routes.ns)

    # ---------------------------
    # Register CLI commands
    from .cli import register_commands
    register_commands(app)

    return app