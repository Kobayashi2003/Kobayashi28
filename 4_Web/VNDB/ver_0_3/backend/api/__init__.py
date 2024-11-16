from flask import Flask, jsonify
from api.config import Config

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
    global scheduled_task
    global celery

    # ----------------------------------------
    # Cors Initialization
    # This section sets up the CORS (Cross-Origin Resource Sharing) mechanism for cross-domain communication
    # ----------------------------------------
    from flask_cors import CORS
    CORS(app)

    # ----------------------------------------
    # Database Initialization
    # This section sets up the SQLAlchemy database connection and creates all tables
    # ----------------------------------------
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)
    with app.app_context():
        db.create_all()

    # ----------------------------------------
    # Cache Initialization
    # This section sets up the caching system for improved performance
    # ----------------------------------------
    from flask_caching import Cache
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    # ----------------------------------------
    # Scheduler Initialization
    # This section sets up the APScheduler for running scheduled tasks
    # ----------------------------------------
    from flask_apscheduler import APScheduler
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    
    def scheduled_task(*args, **kwargs):
        def decorator(func):
            import functools
            @functools.wraps(func)
            @scheduler.task(*args, **kwargs)
            def wrapper(*a, **kw):
                with app.app_context():
                    return func(*a, **kw)
            return wrapper
        return decorator

    # Import scheduler tasks
    from .schedule import simple_task as scheduled_simple_task
    from .schedule import cleanup_task as scheduled_cleanup_task
    from .schedule import backup_task as scheduled_backup_task

    # ----------------------------------------
    # Celery Initialization
    # This section sets up Celery for asynchronous task processing
    # ----------------------------------------
    from celery import Celery
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery_config = {
        'broker_url': app.config['CELERY_BROKER_URL'],
        'result_backend': app.config['CELERY_RESULT_BACKEND'],
        'accept_content': app.config['CELERY_ACCEPT_CONTENT'],
        'task_serializer': app.config['CELERY_TASK_SERIALIZER'],
        'result_serializer': app.config['CELERY_RESULT_SERIALIZER'],
        'timezone': app.config['CELERY_TIMEZONE'],
        'broker_connection_retry_on_startup': app.config['CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP']
    }
    celery.conf.update(celery_config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    app.celery = celery

    # Import Celery tasks
    from .tasks import get_data_task
    from .tasks import search_task

    from .tasks import create_data_task
    from .tasks import read_data_task
    from .tasks import update_data_task
    from .tasks import delete_data_task
    from .tasks import cleanup_task
    from .tasks import backup_task 
    from .tasks import restore_task

    from .tasks import get_image_task
    from .tasks import get_images_task
    from .tasks import upload_images_task
    from .tasks import download_images_task
    from .tasks import update_images_task
    from .tasks import delete_image_task
    from .tasks import delete_images_task

    from .tasks import get_savedata_task
    from .tasks import get_savedatas_task
    from .tasks import upload_savedatas_task
    from .tasks import delete_savedata_task
    from .tasks import delete_savedatas_task

    # ----------------------------------------
    # Blueprint Registration
    # This section registers all the blueprints (modular components) of the application
    # ----------------------------------------

    from .routes_v1 import api_bp as api_v1_bp
    from .routes_v2 import api_bp as api_v2_bp
    from .routes_v3 import api_bp as api_v3_bp

    app.register_blueprint(api_v1_bp)
    app.register_blueprint(api_v2_bp)
    app.register_blueprint(api_v3_bp)


    # ----------------------------------------
    # CLI Command Registration
    # This section adds custom CLI commands for database operations
    # ----------------------------------------
    from .database.command import initdb
    from .database.command import forge
    from .database.command import clean_db
    from .database.command import backup_db 
    from .database.command import restore_db

    app.cli.add_command(initdb)
    app.cli.add_command(forge)
    app.cli.add_command(clean_db)
    app.cli.add_command(backup_db)
    app.cli.add_command(restore_db)

    return app