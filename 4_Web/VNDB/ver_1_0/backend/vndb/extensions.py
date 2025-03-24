from abc import ABC, abstractmethod
from functools import wraps

from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_apscheduler import APScheduler
from celery import Celery

from .logger import logger


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error: {str(e)}")
            logger.error(str(e))
            return None
    return wrapper

class Extension(ABC):
    def __init__(self, app):
        self._app= app
        self._instance = self.create(app)

    @error_handler
    def __getattr__(self, name):
        if not self._instance:
            raise AttributeError(f"{self.__class__.__name__} has not been initialized")
        return getattr(self._instance, name)

    @abstractmethod
    def create(self, app):
        pass

class ExtSQLAchemy(Extension):
    def create(self, app):
        db = SQLAlchemy(app)
        with app.app_context():
            db.create_all()
        return db

class ExtCache(Extension):
    def create(self, app):
        cache = Cache(app, config={
            'CACHE_TYPE': app.config['CACHE_TYPE'],
            'CACHE_REDIS_URL': app.config['CACHE_REDIS_URL'],
            'CACHE_DEFAULT_TIMEOUT': app.config['CACHE_DEFAULT_TIMEOUT']
        })
        return cache

class ExtCelery(Extension):
    def create(self, app):
        celery = Celery(
            app.import_name,
            broker=app.config['CELERY_BROKER_URL'],
            backend=app.config['CELERY_RESULT_BACKEND']
        )
        celery.conf.update({
            'task_default_queue': app.config['CELERY_DEFAULT_QUEUE'],
            'broker_url': app.config['CELERY_BROKER_URL'],
            'result_backend': app.config['CELERY_RESULT_BACKEND'],
            'accept_content': app.config['CELERY_ACCEPT_CONTENT'],
            'task_serializer': app.config['CELERY_TASK_SERIALIZER'],
            'result_serializer': app.config['CELERY_RESULT_SERIALIZER'],
            # 'timezone': app.config['CELERY_TIMEZONE'],
            'broker_connection_retry_on_startup': app.config['CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP']
        })
        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        celery.Task = ContextTask
        app.celery = celery
        return celery

class ExtAPScheduler(Extension):
    def __getattr__(self, name):
        if name == 'task':
            return self.scheduled_task
        return super().__getattr__(name)

    def create(self, app):
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
        return scheduler

    def scheduled_task(self, *args, **kwargs):
        def decorator(func):
            @wraps(func)
            @self._instance.task(*args, **kwargs)
            def wrapper(*a, **kw):
                with self._app.app_context():
                    return func(*a, **kw)
            return wrapper
        return decorator