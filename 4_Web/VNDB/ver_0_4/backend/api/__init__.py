from flask import Flask, jsonify, render_template
from flask_cors import CORS

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

    from .tasks.simple import simple_task
    # from .tasks.backups import scheduled_backup_task

    # ----------------------------------------
    # Blueprint Registration
    # This section registers all the blueprints (modular components) of the application
    # ----------------------------------------
    from .routes import api_bp
    app.register_blueprint(api_bp)
    app.add_url_rule('/', 'index', lambda: render_template('test.html'), methods=['GET'])

    # ----------------------------------------
    # CLI Command Registration
    # This section adds custom CLI commands for database operations
    # ----------------------------------------
    from .database.command import init_db
    from .database.command import forge
    from .database.command import clean_db
    from .database.command import backup_db 
    from .database.command import restore_db

    app.cli.add_command(init_db)
    app.cli.add_command(forge)
    app.cli.add_command(clean_db)
    app.cli.add_command(backup_db)
    app.cli.add_command(restore_db)

    return app