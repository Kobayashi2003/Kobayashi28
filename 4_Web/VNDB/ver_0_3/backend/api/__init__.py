from flask import Flask
from flask_caching import Cache

from api.config import Config
from api.celery_app import celery, create_celery_app
from api.cache_app import cache, init_cache
from api.db.database import db, init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database
    init_db(app)

    # Initialize cache
    init_cache(app)

    # Initialize Celery
    celery.conf.update(app.config)

    # Register blueprints
    from api.routes.hello import hello_bp
    from api.routes.test import test_bp
    from api.routes.search import search_bp
    from api.routes.crud import crud_bp
    from api.routes.data import data_bp
    from api.routes.update import update_bp

    app.register_blueprint(hello_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(crud_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(update_bp)

    # Register CLI commands
    from api.db.command import initdb, forge
    app.cli.add_command(initdb)
    app.cli.add_command(forge)

    return app
