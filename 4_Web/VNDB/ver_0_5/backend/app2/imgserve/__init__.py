from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_migrate import Migrate

from .config import Config
from .proxy import (
    DatabaseProxy, CacheProxy, CeleryProxy, SchedulerProxy
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify(error=str(e)), 500

    # Global variable declarations
    global db
    global cache
    global scheduler
    global celery

    # ----------------------------------------
    # Cors Initialization
    # This section sets up the CORS (Cross-Origin Resource Sharing) mechanism for cross-domain communication
    # ----------------------------------------
    CORS(app)

    # ----------------------------------------
    # Database Initialization
    # This section sets up the SQLAlchemy database connection and creates all tables
    # ----------------------------------------
    db = DatabaseProxy(app)
    migrate = Migrate(app, db.instance)

    # ----------------------------------------
    # Cache Initialization
    # This section sets up the caching system for improved performance
    # ----------------------------------------
    cache = CacheProxy(app)

    # ----------------------------------------
    # Celery Initialization
    # This section sets up Celery for asynchronous task processing
    # ----------------------------------------
    celery = CeleryProxy(app)

    # ----------------------------------------
    # Scheduler Initialization
    # This section sets up the APScheduler for running scheduled tasks
    # ----------------------------------------
    scheduler = SchedulerProxy(app)

    # ----------------------------------------
    # Blueprint Registration
    # This section registers all the blueprints (modular components) of the application
    # ----------------------------------------
    from .routes.images import image_bp
    app.register_blueprint(image_bp)

    # ----------------------------------------
    # CLI Command Registration
    # This section adds custom CLI commands for database operations
    # ----------------------------------------
    from .database.command import register_commands

    register_commands(app)

    return app