import click
from flask.cli import with_appcontext
from flask_migrate import migrate

@click.command('makemigrations')
@click.option('--message', '-m', default=None, help='Migration message')
@with_appcontext
def makemigrations(message):
    """Create a new migration."""
    migrate(message=message)
    click.echo('Created a new migration.')