from typing import Dict 
from celery import Task

from api import celery
from api.database import restore_database_pg_dump 
from api.utils import get_backup_path

@celery.task(bind=True)
def restore_task(self: Task, backup_id: str) -> Dict[str, str]:

    self.update_state(state='PROGRESS', meta={'status': 'Restoring backup...'})
    try:
        backup_path = get_backup_path(backup_id)
        return {
            "status": "SUCCESS" if backup_path else "NOT_FOUND",
            "result": restore_database_pg_dump(backup_path) if backup_path else False 
        }
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}