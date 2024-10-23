import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    STATIC_FOLDER = 'static'
    PG_USER = os.environ.get('PG_USER') or 'postgres'
    PG_PASSWORD = os.environ.get('PG_PASSWORD') or 'root'
    PG_DB = os.environ.get('PG_DB') or 'vndb'
    PG_HOST = os.environ.get('PG_HOST') or 'localhost'
    PG_PORT = os.environ.get('PG_PORT') or '5432'