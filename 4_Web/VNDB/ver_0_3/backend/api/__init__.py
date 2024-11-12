from flask import Flask 
from api.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Global variable declarations
    global db
    global cache
    global scheduler
    global scheduled_task
    global celery

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
    from .tasks import crud_task
    from .tasks import search_task
    from .tasks import get_data_task
    from .tasks import update_data_task
    from .tasks import delete_data_task
    from .tasks import cleanup_task
    from .tasks import backup_task 
    from .tasks import restore_task

    # ----------------------------------------
    # Blueprint Registration
    # This section registers all the blueprints (modular components) of the application
    # ----------------------------------------
    from .routes import hello_bp
    from .routes import test_bp
    from .routes import search_bp
    from .routes import crud_bp
    from .routes import data_bp
    from .routes import update_bp
    from .routes import delete_bp
    from .routes import cleanup_bp
    from .routes import backup_restore_bp

    app.register_blueprint(hello_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(crud_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(update_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(cleanup_bp)
    app.register_blueprint(backup_restore_bp)

    # ----------------------------------------
    # CLI Command Registration
    # This section adds custom CLI commands for database operations
    # ----------------------------------------
    from api.database.command import initdb
    from api.database.command import forge
    from api.database.command import backup_db 
    from api.database.command import restore_db

    app.cli.add_command(initdb)
    app.cli.add_command(forge)
    app.cli.add_command(backup_db)
    app.cli.add_command(restore_db)

    return app