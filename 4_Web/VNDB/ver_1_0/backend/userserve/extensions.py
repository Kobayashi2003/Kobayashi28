from abc import ABC, abstractmethod
from functools import wraps

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler

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
        self._app = app
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

class ExtJWT(Extension):
    def create(self, app):
        jwt = JWTManager(app)
        return jwt

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