import os

class Config:
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']
    REDIS_HOST = os.environ['REDIS_HOST']
    REDIS_PORT = os.environ['REDIS_PORT']
    REDIS_CACHE_DB = os.environ['REDIS_CACHE_DB']
    REDIS_CELERY_BROKER_DB = os.environ['REDIS_CELERY_BROKER_DB']
    REDIS_CELERY_BACKEND_DB = os.environ['REDIS_CELERY_BACKEND_DB']

    # Flask configurations
    DEBUG = False
    USE_RELOADER = False
    SECRET_KEY = 'dev'
    APP_PORT = '5000'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cache configuration
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE_DB}'
    CACHE_DEFAULT_TIMEOUT = 300

    # Celery configuration
    CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_BROKER_DB}'
    CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_BACKEND_DB}'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

    # Scheduler configuration
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "UTC"