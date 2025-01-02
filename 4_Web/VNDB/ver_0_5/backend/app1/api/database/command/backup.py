import os 
import subprocess
from datetime import datetime, timezone

import click
from flask.cli import with_appcontext
from flask import current_app

@click.command('backup-db')
@click.option('-f', '--filename', default=None, help='Specify a filename for the backup file.')
@with_appcontext
def backup_db(filename):
    """Backup the database using pg_dump."""

    if not filename:
        filename = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S') + '.dump'

    db_name = current_app.config['DB_NAME']
    db_user = current_app.config['DB_USER']
    db_password = current_app.config['DB_PASSWORD']
    db_host = current_app.config['DB_HOST']
    db_port = current_app.config['DB_PORT']

    backup_folder = current_app.config['BACKUP_FOLDER']
    backup_path = os.path.join(backup_folder, filename)
    os.makedirs(backup_folder, exist_ok=True)

    env = os.environ.copy()
    env['PGPASSWORD'] = db_password

    command = [
        'pg_dump',
        '-h', db_host,
        '-p', db_port,
        '-U', db_user,
        '-F', 'c',  # plain text format
        '-f', backup_path,
        db_name
    ]

    try:
        subprocess.run(command, env=env, check=True, capture_output=True, text=True)
        click.echo(f"Database backup created successfully")
    except Exception as e:
        click.echo(f"Error creating database backup: {str(e)}", err=True)