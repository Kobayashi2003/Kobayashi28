import os

class Config:
    # Database configuration
    DB_NAME = os.environ.get('DB_NAME', 'test2')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

    # Cache configuration
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/0')
    CACHE_DEFAULT_TIMEOUT = 300

    # Celery configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/1')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', f'redis://{REDIS_HOST}:{REDIS_PORT}/2')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

    # Scheduler configuration
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "UTC"

    # Flask configurations
    DEBUG = os.environ.get('DEBUG', False)
    USE_RELOADER = os.environ.get('USE_RELOADER', False)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    APP_PORT = int(os.environ.get('APP_PORT', 5000))