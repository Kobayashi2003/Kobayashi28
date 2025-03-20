import os
import subprocess
from datetime import datetime, timezone
from urllib.parse import urlparse

import click
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy import inspect

from vndb import db
from .models import MODEL_MAP

def register_commands(app):
    app.cli.add_command(init_db)
    app.cli.add_command(clean_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(inspect_db)
    app.cli.add_command(backup_db)
    app.cli.add_command(restore_db)

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

@click.command('inspect-db')
@with_appcontext
def inspect_db():
    """Inspect the database schema."""
    inspector = inspect(db.engine)
    for model_name, model_class in MODEL_MAP.items():
        columns = inspector.get_columns(model_class.__tablename__)
        foreign_keys = inspector.get_foreign_keys(model_class.__tablename__)

        print(f"Table: {model_class.__tablename__}")
        print("Columns:")
        for column in columns:
            print(f"  - {column['name']} ({column['type']})")
        print("Foreign Keys:")
        for fk in foreign_keys:
            print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        print("\n")

@click.command('backup-db')
@click.option('-f', '--filename', default=None, help='Specify a filename for the backup file.')
@with_appcontext
def backup_db(filename):
    """Backup the database using pg_dump."""

    if not filename:
        filename = 'vndb_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S') + '.dump'

    db_url = urlparse(current_app.config['SQLALCHEMY_DATABASE_URI'])

    db_name = db_url.path[1:]  # remove leading '/'
    db_user = db_url.username
    db_password = db_url.password
    db_host = db_url.hostname
    db_port = str(db_url.port)

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

    db_url = urlparse(current_app.config['SQLALCHEMY_DATABASE_URI'])

    db_name = db_url.path[1:]  # remove leading '/'
    db_user = db_url.username
    db_password = db_url.password
    db_host = db_url.hostname
    db_port = str(db_url.port)

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