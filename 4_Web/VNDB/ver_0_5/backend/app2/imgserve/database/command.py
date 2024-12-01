import click
from flask.cli import with_appcontext
from imgserve import db
from .model import IMAGE_MODEL

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
