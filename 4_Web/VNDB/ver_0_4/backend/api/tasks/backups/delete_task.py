from typing import Optional, Dict, Any 
from celery import Task

from api import celery
from api.database import delete_backup, delete_backups, convert_model_to_dict

@celery.task(bind=True)
def delete_backups_task(self: Task, backup_id: Optional[str] = None) -> Dict[str, Any]:

    self.update_state(state='PROGRESS', meta={'status': 'Deleting backup(s)...'})

    try:
        if backup_id:
            result = delete_backup(backup_id)
            return {
                "status": "SUCCESS" if result else "NOT_FOUND",
                "result": convert_model_to_dict(result) if result else None
            }
        else:
            deleted_count = delete_backups()
            return {
                "status": "SUCCESS" if deleted_count else "NOT_FOUND",
                "result": deleted_count
            }
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}