import click
from flask.cli import with_appcontext
from flask_migrate import migrate, upgrade
from imgserve import db
from .model import IMAGE_MODEL

def register_commands(app):
    app.cli.add_command(init_db)
    app.cli.add_command(clean_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(makemigration)
    app.cli.add_command(migrate_db)

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

@click.command('clean-db')
@click.option('--force', is_flag=True, help='Clean without confirmation.')
@with_appcontext
def clean_db(force):
    """Remove all data from the database tables without dropping the tables."""
    if not force:
        click.confirm('This operation will delete all data in the database, do you want to continue?', abort=True)
    
    for model_name, model_class in IMAGE_MODEL.items():
        try:
            num_rows_deleted = db.session.query(model_class).delete()
            db.session.commit()
            click.echo(f'Deleted {num_rows_deleted} rows from {model_name}.')
        except Exception as e:
            db.session.rollback()
            click.echo(f'Error cleaning {model_name}: {str(e)}')
    
    click.echo('Database cleaned successfully.')

@click.command('makemigration')
@click.option('--message', '-m', default=None, help='Migration message')
@with_appcontext
def makemigration(message):
    """Create a new migration."""
    migrate(message=message)
    click.echo('Created a new migration.')

@click.command('migrate')
@with_appcontext
def migrate_db():
    """Apply all pending migrations."""
    upgrade()
    click.echo('Applied all pending migrations.')