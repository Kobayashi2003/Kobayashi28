from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import restore_database_pg_dump, get_backup_path

@celery.task(bind=True)
def restore_task(self, backup_id: str):
    self.update_state(state='PROGRESS', meta={'status': 'Restoring backup...'})
    try:
        backup_path = get_backup_path(backup_id)
        restore_database_pg_dump(backup_path)
        return {"status": "SUCCESS", "result": f"Database restored from backup {backup_id}"}
    except SQLAlchemyError as e:
        self.update_state(state='FAILURE', meta={'status': 'Database error occurred'})
        return {
            "status": "ERROR",
            "result": f"Database error during restore: {str(e)}"
        }
    except Exception as e:
        self.update_state(state='FAILURE', meta={'status': 'Unexpected error occurred'})
        return {
            "status": "ERROR",
            "result": f"Unexpected error during restore: {str(e)}"
        }