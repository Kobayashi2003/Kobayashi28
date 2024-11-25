from typing import List, Dict, Any, Optional

import os
import subprocess
import uuid
from datetime import datetime, timezone 

from flask import current_app

from .common import db_transaction
from .base import (
    _get, _get_all, _get_inactive_type,
    _create, _delete
)
from ..models import Backup

def get_next_backup_id() -> str:
    return str(uuid.uuid4()) 

def backup_database_pg_dump() -> str:
    """Create a database backup and return the filename."""
    backup_folder = current_app.config['BACKUP_FOLDER']
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    backup_id = get_next_backup_id()
    backup_filename = f"{backup_id}.dump"
    backup_path = os.path.join(backup_folder, backup_filename)
    
    # Get database connection information from config
    db_name = current_app.config['DB_NAME']
    db_user = current_app.config['DB_USER']
    db_password = current_app.config['DB_PASSWORD']
    db_host = current_app.config['DB_HOST']
    db_port = current_app.config['DB_PORT']

    # Set environment variable to avoid exposing password in command line
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password

    # Build pg_dump command
    command = [
        'pg_dump',
        '-h', db_host,
        '-p', db_port,
        '-U', db_user,
        '-F', 'c',  # custom format
        '-f', backup_path,
        db_name
    ]

    try:
        # Execute pg_dump command
        result = subprocess.run(command, env=env, check=True, capture_output=True, text=True)
        print(f"Database backup created: {backup_filename}")
        return backup_id 
    except subprocess.CalledProcessError as e:
        print(f"Error during database backup: {e}")
        print(f"Error output: {e.stderr}")
        if os.path.exists(backup_path):
            os.remove(backup_path)
        raise
    finally:
        # Clear password from environment variable
        env.pop('PGPASSWORD', None)

def restore_database_pg_dump(filename) -> bool:

    # Check if the backup file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Backup file not found: {filename}")

    # Get database connection information from config
    db_name = current_app.config['DB_NAME']
    db_user = current_app.config['DB_USER']
    db_password = current_app.config['DB_PASSWORD']
    db_host = current_app.config['DB_HOST']
    db_port = current_app.config['DB_PORT']

    # Set environment variable to avoid exposing password in command line
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password

    # Build psql command for restoration
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
        # Execute psql command to restore the database
        result = subprocess.run(command, env=env, check=True, capture_output=True, text=True)
        print(f"Database restored from: {filename}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during database restore: {e}")
        print(f"Error output: {e.stderr}")
        raise
    except Exception as e:
        print(f"Unexpected error during database restore: {str(e)}")
        raise
    finally:
        # Clear password from environment variable
        env.pop('PGPASSWORD', None)

@db_transaction
def create_backup() -> Optional[str]:
    try:
        # Perform the actual backup
        backup_id = backup_database_pg_dump()

        # Create a new backup entry in the database
        backup_data = {
            'time': datetime.now(timezone.utc),
        }
        
        new_backup = _create('backup', backup_id, backup_data)
        if new_backup is None:
            raise ValueError("Failed to create backup entry in database")

        return backup_id

    except Exception as e:
        print(f"Error during backup creation: {str(e)}")
        # If the backup file was created but database entry failed, remove the file
        backup_folder = current_app.config['BACKUP_FOLDER']
        backup_path = os.path.join(backup_folder, f'{backup_id}.dump')
        if os.path.exists(backup_path):
            os.remove(backup_path)
        raise

@db_transaction
def get_backup(backup_id: str) -> Optional[Backup]:
    return _get('backup', backup_id)

@db_transaction
def get_backups(page: Optional[int] = None, limit: Optional[int] = None) -> List[Backup]:
    return _get_all('backup', page=page, limit=limit, sort='time', order='desc')

@db_transaction
def delete_backup(backup_id: str) -> Optional[Backup]:
    deleted_backup = _delete('backup', backup_id)
    if deleted_backup is None:
        print(f"No backup found with ID: {backup_id}")
        return None

    print(f"Backup with ID {backup_id} successfully deleted")
    return deleted_backup

@db_transaction
def delete_backups() -> int:
    backups = _get_all('backup') + _get_inactive_type('backup')
    
    deleted_count = 0
    for backup in backups:
        deleted_backup = _delete('backup', backup.id)
        deleted_count += 1 if deleted_backup else 0

    return deleted_count

