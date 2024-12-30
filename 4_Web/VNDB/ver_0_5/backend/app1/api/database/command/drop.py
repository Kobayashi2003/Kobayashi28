import click
from flask.cli import with_appcontext
from api import db

@click.command('drop-db')
@click.option('--force', is_flag=True, help='Drop without confirmation.')
@with_appcontext
def drop_db(force):
    """Drop all tables in the database."""
    if not force:
        click.confirm('This operation will drop all tables in the database, do you want to continue?', abort=True)
    
    db.drop_all()
    click.echo('All tables have been dropped.')