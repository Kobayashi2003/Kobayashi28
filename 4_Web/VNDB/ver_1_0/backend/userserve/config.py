import os
from dotenv import load_dotenv
from datetime import timedelta 

load_dotenv()

class Config:

    # Flask configurations
    DEBUG = os.environ['DEBUG']
    USE_RELOADER = os.environ['USE_RELOADER']
    SECRET_KEY = os.environ['SECRET_KEY']
    APP_HOST = os.environ['USERSERVE_HOST']
    APP_PORT = int(os.environ['USERSERVE_PORT'])

    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    JWT_VERIFY_SUB = False
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7) 

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ['USERSERVE_DB_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Scheduler configuration
    SCHEDULER_API_ENABLED = True
    # SCHEDULER_TIMEZONE = "UTC"

    # Data folder configuration
    DATA_FOLDER = os.environ['DATA_FOLDER']
    TEMP_FOLDER = os.path.join(DATA_FOLDER, 'tmp')
    BACKUP_FOLDER = os.path.join(DATA_FOLDER, 'backups')