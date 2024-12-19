import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/hospital'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost:5432/hospital'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/hospital_test'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Set the active configuration
active_config = config[os.environ.get('FLASK_ENV', 'default')]