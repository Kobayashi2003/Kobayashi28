import click
from flask.cli import with_appcontext
from ..crud import backup_database_pg_dump

@click.command('backup-db')
@with_appcontext
def backup_db():
    """Backup the database using pg_dump."""
    try:
        backup_file = backup_database_pg_dump()
        click.echo(f"Database backup created successfully: {backup_file}")
    except Exception as e:
        click.echo(f"Error creating database backup: {str(e)}", err=True)
