def create_app():
    from flask import Flask 
    app = Flask(__name__)
    
    # ---------------------------
    # Load configuration
    app.url_map.strict_slashes = False
    app.config.from_object('app.config.active_config')

    # ---------------------------
    # Initialize extensions
    from flask_migrate import Migrate
    from flask_cors import CORS
    from app.extentions import (
        ExtSQLAchemy, ExtRestx, ExtJWT, ExtAPScheduler
    )

    global db
    global migrate
    global api
    global jwt
    global scheduler

    CORS(app, resources={r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "X-CSRFToken"],
        "max_age": 600
    }})

    db = ExtSQLAchemy(app)
    migrate = Migrate(app, db)
    api = ExtRestx(app)
    jwt = ExtJWT(app)
    scheduler = ExtAPScheduler(app)
    
    # ---------------------------
    # Generate random admin password
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    admin_password = ''.join(secrets.choice(alphabet) for i in range(16))
    app.config['ADMIN_PASSWORD'] = admin_password
    print(f"Generated admin password: {admin_password}")

    # ---------------------------
    # Register routes
    # from app.routes import register_namespaces
    # register_namespaces(api)

    # ---------------------------
    # Register CLI commands
    from app.cli import register_commands
    register_commands(app)

    return app