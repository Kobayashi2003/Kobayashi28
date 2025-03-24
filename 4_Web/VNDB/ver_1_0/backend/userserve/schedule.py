import os
import subprocess
from functools import wraps
from urllib.parse import urlparse
from datetime import datetime, timezone

from flask import current_app
from userserve import scheduler

def test_task(func):
    @wraps(func)
    @scheduler.task(trigger='interval', id=f'test_{func.__name__}', seconds=10)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def daily_task(hour=0, minute=0):
    def decorator(func):
        @wraps(func)
        @scheduler.task(trigger='cron', id=f'daily_{func.__name__}', hour=hour, minute=minute)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def weekly_task(day_of_week=0, hour=0, minute=0):
    def decorator(func):
        @wraps(func)
        @scheduler.task(trigger='cron', id=f'weekly_{func.__name__}', day_of_week=day_of_week, hour=hour, minute=minute)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


@weekly_task(day_of_week=0, hour=0, minute=0)
def backup_database_schedule():
    filename = 'userserve_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S') + '.dump'
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
        print(f"[UserServe] Database backup created successfully")
    except Exception as e:
        print(f"[UserServe] Error creating database backup: {str(e)}", err=True)
