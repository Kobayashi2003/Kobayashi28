from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
api = Api()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name.capitalize()}Config')

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Enable CORS for all routes with specific options
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

    # Import and register blueprints/routes here
    from app.routes import user_routes, image_routes, tag_routes, comment_routes, collection_routes

    api.add_namespace(user_routes.ns)
    api.add_namespace(image_routes.ns)
    api.add_namespace(tag_routes.ns)
    api.add_namespace(comment_routes.ns)
    api.add_namespace(collection_routes.ns)

    from app.cli import register_commands
    register_commands(app, db)

    return app
