from typing import Optional

from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import get_backup, get_backups

@celery.task(bind=True)
def get_backups_task(self, backup_id: Optional[str] = None):
    self.update_state(state='PROGRESS', meta={'status': 'Retrieving backup(s)...'})

    try:
        if backup_id:
            backup = get_backup(backup_id)
            return {
                "status": "SUCCESS" if backup else "NOT_FOUND",
                "result": backup
            }
        else:
            backups = get_backups()
            return {
                "status": "SUCCESS" if backups else "NOT_FOUND",
                "result": backups
            }
    except SQLAlchemyError as e:
        self.update_state(state='FAILURE', meta={'status': 'Database error occurred'})
        return {
            "status": "ERROR",
            "result": f"Database error: {str(e)}"
        }
    except Exception as e:
        self.update_state(state='FAILURE', meta={'status': 'Unexpected error occurred'})
        return {
            "status": "ERROR",
            "result": f"Unexpected error: {str(e)}"
        }