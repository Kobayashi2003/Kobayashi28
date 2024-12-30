import click
from flask.cli import with_appcontext
from flask_migrate import downgrade

@click.command('downgrade')
@click.option('--revision', '-r', default='-1', help='Revision to downgrade to (default: -1, which means downgrade one step)')
@with_appcontext
def downgrade_db(revision):
    """Revert to a previous database migration."""
    downgrade(revision)
    click.echo(f'Downgraded database to revision: {revision}')