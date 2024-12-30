import click
from flask.cli import with_appcontext
from flask_migrate import upgrade 

@click.command('migrate')
@with_appcontext
def migrate_db():
    """Apply all pending migrations."""
    upgrade()
    click.echo('Applied all pending migrations.')