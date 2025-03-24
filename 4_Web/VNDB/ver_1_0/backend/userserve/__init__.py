from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from .config import Config
from .extensions import (
    ExtSQLAchemy, ExtJWT, ExtAPScheduler
)

import secrets
import string

def create_app(config_class=Config, enable_scheduler=True):
    app = Flask(__name__)

    # ---------------------------
    # Load configuration
    # ---------------------------
    app.url_map.strict_slashes = False
    app.config.from_object(config_class)

    # Global variable declarations
    global db
    global migrate
    global jwt
    global scheduler

    # ----------------------------------------
    # Cors Initialization
    # This section sets up the CORS (Cross-Origin Resource Sharing) mechanism for cross-domain communication
    # ----------------------------------------
    CORS(app, resources={r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "X-CSRFToken"],
        "max_age": 600
    }})

    db = ExtSQLAchemy(app)
    migrate = Migrate(app, db)
    jwt = ExtJWT(app)
    if enable_scheduler:
        scheduler = ExtAPScheduler(app)
    else:
        scheduler = None

    # ---------------------------
    # Generate random admin password
    alphabet = string.ascii_letters + string.digits
    admin_password = ''.join(secrets.choice(alphabet) for i in range(16))
    app.config['ADMIN_PASSWORD'] = admin_password
    print(f"Generated admin password: {admin_password}")

    # ---------------------------
    # Register routes
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify(error=str(e)), 500

    app.add_url_rule('/test', 'test', lambda: render_template('test.html'), methods=['GET'])

    from .routes import api_bp
    app.register_blueprint(api_bp)

    # ---------------------------
    # Register tasks
    from .schedule import backup_database_schedule

    # ---------------------------
    # Register CLI commands
    from .cli import register_commands
    register_commands(app)

    return app