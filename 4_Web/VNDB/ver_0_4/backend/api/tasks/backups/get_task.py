from typing import Optional, Dict, Any 
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import get_backup, get_backups, convert_model_to_dict

@celery.task(bind=True)
def get_backups_task(self: Task, backup_id: Optional[str] = None) -> Dict[str, Any]:

    self.update_state(state='PROGRESS', meta={'status': 'Retrieving backup(s)...'})

    try:
        if backup_id:
            backup = get_backup(backup_id)
            return {
                "status": "SUCCESS" if backup else "NOT_FOUND",
                "result": convert_model_to_dict(backup) if backup else None
            }
        else:
            backups = get_backups()
            return {
                "status": "SUCCESS" if backups else "NOT_FOUND",
                "result": [convert_model_to_dict(backup) for backup in backups] if backups else []
            }
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}