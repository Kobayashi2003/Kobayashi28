from api import create_app
from api.config import Config

def run_celery_worker(config):
    app = create_app(config)
    celery = app.celery
    print("Starting Celery worker")
    worker = celery.Worker(
        pool='solo',
        loglevel='info',
        quiet=False
    )
    worker.start()

if __name__ == '__main__':
    config = Config()
    run_celery_worker(config)