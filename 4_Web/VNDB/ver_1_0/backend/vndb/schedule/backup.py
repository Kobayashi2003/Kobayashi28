import os
import subprocess
from urllib.parse import urlparse
from datetime import datetime, timezone
from flask import current_app
from .common import weekly_task

@weekly_task(day_of_week=0, hour=0, minute=0)
def backup_database_schedule():
    filename = 'vndb_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S') + '.dump'
    backup_folder = current_app.config['BACKUP_FOLDER']
    backup_path = os.path.join(backup_folder, filename)
    os.makedirs(backup_folder, exist_ok=True)

    db_url = urlparse(current_app.config['SQLALCHEMY_DATABASE_URI'])

    db_name = db_url.path[1:]  # remove leading '/'
    db_user = db_url.username
    db_password = db_url.password
    db_host = db_url.hostname
    db_port = str(db_url.port)

    env = os.environ.copy()
    env['PGPASSWORD'] = db_password

    command = [
        'pg_dump',
        '-h', db_host,
        '-p', db_port,
        '-U', db_user,
        '-F', 'c',
        '-f', backup_path,
        db_name
    ]

    try:
        subprocess.run(command, env=env, check=True, capture_output=True, text=True)
        print(f"[VNDB] Database backup created successfully")
    except Exception as e:
        print(f"[VNDB] Error creating database backup: {str(e)}", err=True)

