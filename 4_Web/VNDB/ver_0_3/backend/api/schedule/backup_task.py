from datetime import datetime
from flask import current_app

from api import scheduled_task
from ..database import backup_database_pg_dump

@scheduled_task(trigger='cron', id='weekly_backup_task', day_of_week='sun', hour=0, minute=0)
def backup_task():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_app.logger.info(f"Starting database backup at {current_time}")

    try:
        backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.dump"
        result = backup_database_pg_dump(backup_filename)

        success_message = f"Database backup completed successfully. Backup file: {result}"
        current_app.logger.info(success_message)
        print(success_message)

        return {
            'status': 'SUCCESS',
            'result': result,
            'backup_file': backup_filename
        }
    except Exception as e:
        error_message = f"Database backup failed: {str(e)}"
        current_app.logger.error(error_message)
        print(error_message)
        raise