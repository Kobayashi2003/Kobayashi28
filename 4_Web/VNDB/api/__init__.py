from flask import Flask
from api.config import Config
from api.celery_app import celery, create_celery_app

from api.routes.search import search_bp
from api.routes.test import test_bp
from api.routes.hello import hello_bp
from api.db.operations import init_app as init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database
    init_db(app)

    # Register blueprints
    app.register_blueprint(search_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(hello_bp)

    # Initialize Celery
    celery.conf.update(app.config)

    return app