import os

class Config:
    # Database configuration
    DB_NAME = os.environ.get('DB_NAME', 'vndb')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')

    # Celery configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'

    # Download configuration
    TEMP_FOLDER = os.environ.get('TEMP_FOLDER', '/tmp')
    IMAGES_FOLDER = os.environ.get('IMAGES_FOLDER', '/images/vn')
    IMAGES_URL_PREFIX = os.environ.get('IMAGES_URL_PREFIX', '/images')

    # Other configurations
    DEBUG = os.environ.get('DEBUG', True)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
