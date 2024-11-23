import click
from flask.cli import with_appcontext
from ..crud import restore_database_pg_dump

@click.command('restore-db')
@click.argument('filename', type=click.Path(exists=True))
@with_appcontext
def restore_db(filename):
    """Restore the database from a backup file."""
    try:
        restore_database_pg_dump(filename)
        click.echo(f"Database restored successfully from: {filename}")
    except Exception as e:
        click.echo(f"Error restoring database: {str(e)}", err=True)

