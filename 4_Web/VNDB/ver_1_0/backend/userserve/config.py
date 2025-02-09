import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # Flask configurations
    DEBUG = False
    USE_RELOADER = False
    SECRET_KEY = os.environ['SECRET_KEY']
    APP_PORT = int(os.environ['USERSERVE_PORT'])

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ['USERSERVE_DB_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Scheduler configuration
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "UTC"

    # Data folder configuration
    DATA_FOLDER = os.environ['DATA_FOLDER']
    TEMP_FOLDER = os.path.join(DATA_FOLDER, 'tmp')
    BACKUP_FOLDER = os.path.join(DATA_FOLDER, 'backups')