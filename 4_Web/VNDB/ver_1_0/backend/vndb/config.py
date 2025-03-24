import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # Flask configurations
    DEBUG = os.environ['DEBUG']
    USE_RELOADER = os.environ['USE_RELOADER']
    SECRET_KEY = os.environ['SECRET_KEY']
    APP_HOST = os.environ['VNDB_HOST']
    APP_PORT = int(os.environ['VNDB_PORT'])

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ['VNDB_DB_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cache configuration
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ['VNDB_CACHE_REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = 300

    # Celery configuration
    CELERY_DEFAULT_QUEUE = os.environ['VNDB_CELERY_DEFAULT_QUEUE']
    CELERY_BROKER_URL = os.environ['VNDB_CELERY_BROKER_URL']
    CELERY_RESULT_BACKEND = os.environ['VNDB_CELERY_RESULT_BACKEND']
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    # CELERY_TIMEZONE = 'UTC'
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
    FLOWER_PORT = os.environ['VNDB_FLOWER_PORT']

    # Scheduler configuration
    SCHEDULER_API_ENABLED = True
    # SCHEDULER_TIMEZONE = "UTC"

    # Data folder configuration
    DATA_FOLDER = os.environ['DATA_FOLDER']
    TEMP_FOLDER = os.path.join(DATA_FOLDER, 'tmp')
    BACKUP_FOLDER = os.path.join(DATA_FOLDER, 'backups')