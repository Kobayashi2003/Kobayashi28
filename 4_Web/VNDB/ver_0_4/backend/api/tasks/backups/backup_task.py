from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import backup_database_pg_dump

@celery.task(bind=True)
def backup_task(self):
    self.update_state(state='PROGRESS', meta={'status': 'Starting database backup...'})

    try:
        backup_id = backup_database_pg_dump()
        self.update_state(state='PROGRESS', meta={'status': 'Backup completed successfully.'})
        return {"status": "SUCCESS", "result": f"Database backup created successfully: {backup_id}"}
    except SQLAlchemyError as e:
        self.update_state(state='FAILURE', meta={'status': 'Database error occurred'})
        return {
            "status": "ERROR",
            "result": f"Database error during backup: {str(e)}"
        }
    except Exception as e:
        self.update_state(state='FAILURE', meta={'status': 'Unexpected error occurred'})
        return {
            "status": "ERROR",
            "result": f"Unexpected error during backup: {str(e)}"
        }