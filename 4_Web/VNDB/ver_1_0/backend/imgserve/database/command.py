import os
import subprocess
from datetime import datetime, timezone

import click
from flask import current_app
from flask.cli import with_appcontext
from imgserve import db
from .model import IMAGE_MODEL

def register_commands(app):
    app.cli.add_command(init_db)
    app.cli.add_command(clean_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(backup_db)
    app.cli.add_command(restore_db)

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

@click.command('restore-db')
@click.argument('filename', type=click.Path(exists=True))
@with_appcontext
def restore_db(filename):
    """Restore the database from a backup file."""

    db_name = current_app.config['DB_NAME']
    db_user = current_app.config['DB_USER']
    db_password = current_app.config['DB_PASSWORD']
    db_host = current_app.config['DB_HOST']
    db_port = current_app.config['DB_PORT']

    env = os.environ.copy()
    env['PGPASSWORD'] = db_password

    command = [
        'pg_restore',
        '-h', db_host,
        '-p', db_port,
        '-U', db_user,
        '-d', db_name,
        '--clean',  # drop existing objects before restoring
        '--if-exists',  # skip objects that don't exist
        '--no-owner', # skip restoration of object ownership
        '--no-privileges',  # skip restoration of access privileges
        filename
    ]

    try:
        subprocess.run(command, env=env, check=True, capture_output=True, text=True)
        click.echo(f"Database restored successfully from: {filename}")
    except Exception as e:
        click.echo(f"Error restoring database: {str(e)}", err=True)