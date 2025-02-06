import os
from dotenv import load_dotenv

load_dotenv()

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
    DEBUG = os.environ['DEBUG'].lower() == 'true'
    USE_RELOADER = os.environ['USE_RELOADER'].lower() == 'true'
    SECRET_KEY = os.environ['SECRET_KEY']
    APP_PORT = int(os.environ['APP_PORT'])

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

    # Data folder configuration
    DATA_FOLDER = os.environ['DATA_FOLDER']
    TEMP_FOLDER = os.path.join(DATA_FOLDER, 'tmp')
    BACKUP_FOLDER = os.path.join(DATA_FOLDER, 'backups')