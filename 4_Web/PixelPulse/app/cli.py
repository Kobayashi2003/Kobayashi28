import click
from flask.cli import with_appcontext
from flask_migrate import Migrate

def register_commands(app, db):
    migrate = Migrate(app, db)

    @app.cli.command("makemigrations")
    @click.option("--message", default=None, help="Migration message")
    @with_appcontext
    def make_migrations(message):
        """Create a new migration."""
        if message:
            from flask_migrate import migrate as _migrate
            _migrate(message=message)
        else:
            from flask_migrate import migrate as _migrate
            _migrate()
        click.echo("Created new migration.")

    @app.cli.command("migrate")
    @with_appcontext
    def run_migrations():
        """Apply all pending migrations."""
        from flask_migrate import upgrade
        upgrade()
        click.echo("Applied all pending migrations.")
