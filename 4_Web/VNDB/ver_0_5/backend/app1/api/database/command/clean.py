import click
from flask.cli import with_appcontext
from api import db
from ..models import MODEL_MAP

@click.command('clean-db')
@click.option('--tables', '-t', multiple=True, help='Specify tables to clean. If none specified, all tables will be cleaned.')
@click.confirmation_option(prompt='Are you sure you want to clean the database?')
@with_appcontext
def clean_db(tables):
    """Clean specified tables or all tables in the database."""
    table_map = MODEL_MAP

    if not tables:
        tables = table_map.keys()

    for table in tables:
        if table in table_map:
            model = table_map[table]
            try:
                num_deleted = db.session.query(model).delete()
                db.session.commit()
                click.echo(f"Cleaned {num_deleted} entries from {table}")
            except Exception as e:
                db.session.rollback()
                click.echo(f"Error cleaning {table}: {str(e)}", err=True)
        else:
            click.echo(f"Unknown table: {table}", err=True)

    click.echo("Database cleaning completed.")