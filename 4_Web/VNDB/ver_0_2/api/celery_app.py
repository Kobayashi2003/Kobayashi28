from celery import Celery
from flask import Flask
from api.config import Config

def create_celery_app(app=None):
    if app is None:
        app = Flask(__name__)
        app.config.from_object(Config)

    celery = Celery(app.import_name,
                    broker=app.config['CELERY_BROKER_URL'],
                    backend=app.config['CELERY_RESULT_BACKEND'])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = create_celery_app()

# Import tasks here to ensure they are registered with Celery
from api.tasks import search_task