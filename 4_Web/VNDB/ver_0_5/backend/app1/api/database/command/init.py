import click
from flask.cli import with_appcontext
from api import db

@click.command('init-db')
@click.option('--drop', is_flag=True, help='Create after drop.')
@with_appcontext
def init_db(drop):
    """Clear the existing data and create new tables."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized the database.')