from celery import Celery
from api.config import Config

def create_celery_app(app=None):
    celery = Celery(__name__)
    celery.config_from_object(Config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

# Import tasks here to ensure they are registered with Celery
from api.tasks import search_task, download_server_task, download_client_task