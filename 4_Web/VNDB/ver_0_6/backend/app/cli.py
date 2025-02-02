import click
from flask.cli import with_appcontext
from flask_migrate import migrate, upgrade 
from app import db
from .models import VisualNovel

def register_commands(app):
    app.cli.add_command(init_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(makemigrations)
    app.cli.add_command(migrate_db)
    app.cli.add_command(test)

@click.command('init-db')
@click.option('--drop', is_flag=True, help='Create after drop.')
@with_appcontext
def init_db(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Dropped all tables.')
    db.create_all()
    click.echo('Initialized the database.')

@click.command('drop-db')
@click.option('--force', is_flag=True, help='Drop without confirmation.')
@with_appcontext
def drop_db(force):
    """Drop all tables in the database."""
    if not force:
        click.confirm('This operation will drop all tables in the database, do you want to continue?', abort=True)
    
    db.drop_all()
    click.echo('All tables have been dropped.')

@click.command('makemigrations')
@click.option('--message', '-m', default=None, help='Migration message')
@with_appcontext
def makemigrations(message):
    """Create a new migration."""
    migrate(message=message)
    click.echo('Created a new migration.')

@click.command('migrate')
@with_appcontext
def migrate_db():
    """Apply all pending migrations."""
    upgrade()
    click.echo('Applied all pending migrations.')

@click.command('test')
@with_appcontext
def test():
    from .insert import insert_tag
    insert_tag('g1')