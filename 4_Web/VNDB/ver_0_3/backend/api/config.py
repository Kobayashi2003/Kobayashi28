import os

class Config:
    # Cache configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300

    # Scheduler configuration
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "UTC"

    # Database configuration
    DB_NAME = os.environ.get('DB_NAME', 'flask_db')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

    # Download configuration
    TEMP_FOLDER = os.environ.get('TEMP_FOLDER', '/tmp')
    IMAGE_VN_FOLDER = os.environ.get('IMAGE_VN_FOLDER', os.path.join(os.path.dirname(__file__), '/DATA/images', 'vn'))
    IMAGE_CHARACTER_FOLDER = os.environ.get('IMAGE_CHARACTER_FOLDER', os.path.join(os.path.dirname(__file__), '/DATA/images', 'character'))
    SAVEDATA_FOLDER = os.environ.get('SAVEDATA_FOLDER', os.path.join(os.path.dirname(__file__), '/DATA/savedatas'))

    # Other configurations
    SERVER_NAME = os.environ.get('SERVER_NAME', 'localhost:5000')
    APPLICATION_ROOT = '/'
    PREFERRED_URL_SCHEME = 'http'

    DEBUG = os.environ.get('DEBUG', False)
    USE_RELOADER = os.environ.get('USE_RELOADER', False)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    APP_PORT = int(os.environ.get('APP_PORT', 5000))