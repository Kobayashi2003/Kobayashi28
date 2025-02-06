from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from .config import Config
from .extensions import (
    ExtSQLAchemy, ExtCache, ExtCelery, ExtAPScheduler
)

def create_app(config_class=Config):
    app = Flask(__name__)

    # ---------------------------
    # Load configuration
    # ---------------------------
    app.url_map.strict_slashes = False
    app.config.from_object(config_class)

    # Global variable declarations
    global db
    global migrate
    global cache
    global scheduler
    global celery

    # ----------------------------------------
    # Cors Initialization
    # This section sets up the CORS (Cross-Origin Resource Sharing) mechanism for cross-domain communication
    # ----------------------------------------
    CORS(app, resources={r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "X-CSRFToken"],
        "max_age": 600
    }})

    # ----------------------------------------
    # Database Initialization
    # This section sets up the SQLAlchemy database connection and creates all tables
    # ----------------------------------------
    db = ExtSQLAchemy(app)

    # ----------------------------------------
    # Migrate Initialization
    # This section sets up the Flask-Migrate extension for database migration management
    # ----------------------------------------
    migrate = Migrate(app, db)

    # ----------------------------------------
    # Cache Initialization
    # This section sets up the caching system for improved performance
    # ----------------------------------------
    cache = ExtCache(app)

    # ----------------------------------------
    # Celery Initialization
    # This section sets up Celery for asynchronous task processing
    # ----------------------------------------
    celery = ExtCelery(app)

    # ----------------------------------------
    # Scheduler Initialization
    # This section sets up the APScheduler for running scheduled tasks
    # ----------------------------------------
    scheduler = ExtAPScheduler(app)

    from .tasks.simple import simple_task

    # ----------------------------------------
    # Blueprint Registration
    # This section registers all the blueprints (modular components) of the application
    # ----------------------------------------

    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify(error=str(e)), 500

    from .routes import api_bp
    app.register_blueprint(api_bp)
    app.add_url_rule('/test', 'test', lambda: render_template('test.html'), methods=['GET'])

    # ----------------------------------------
    # CLI Command Registration
    # This section adds custom CLI commands for database operations
    # ----------------------------------------
    from .database.command import register_commands

    register_commands(app)

    return app