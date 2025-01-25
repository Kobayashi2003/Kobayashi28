from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler

from abc import ABC, abstractmethod
from functools import wraps

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

class Extention(ABC):
    def __init__(self, app):
        self.app = app
        self.instance = self.create(app)

    @error_handler
    def __getattr__(self, name):
        return getattr(self.instance, name)

    @abstractmethod
    def create(self, app):
        pass

class ExtSQLAchemy(Extention):
    def create(self, app):
        db = SQLAlchemy(app)
        with app.app_context():
            db.create_all()
        return db

class ExtRestx(Extention):
    def create(self, app):
        api = Api(app)
        return api

class ExtJWT(Extention):
    def create(self, app):
        jwt = JWTManager(app)
        return jwt

class ExtAPScheduler(Extention):
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
            @self.instance.task(*args, **kwargs)
            def wrapper(*a, **kw):
                with self.app.app_context():
                    return func(*a, **kw)
            return wrapper
        return decorator
