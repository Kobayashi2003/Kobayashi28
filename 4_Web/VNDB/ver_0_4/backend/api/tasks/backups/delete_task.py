from typing import Optional, List

from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import delete_backup, delete_backups

@celery.task(bind=True)
def delete_backups_task(self, backup_id: Optional[str] = None):
    self.update_state(state='PROGRESS', meta={'status': 'Deleting backup(s)...'})
    
    try:
        if backup_id:
            result = delete_backup(backup_id)
        else:
            result = delete_backups()

        return {
            "status": "SUCCESS",
            "result": result
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

