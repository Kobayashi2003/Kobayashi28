from typing import Optional

from api import celery
from api.database import delete_savedatas, delete_savedata, exists

@celery.task(bind=True)
def delete_savedatas_task(self, resource_type: str, resource_id: str, savedata_id: Optional[str] = None):
    self.update_state(state='PROGRESS', meta={'status': 'Checking resource existence...'})
    if not exists(resource_type, resource_id):
        return {"status": "NOT_FOUND", "result": None}

    self.update_state(state='PROGRESS', meta={'status': 'Deleting savedata(s)...'})
    
    if savedata_id:
        result = delete_savedata(resource_id, savedata_id)
        return {
            "status": "SUCCESS" if result else "NOT_FOUND",
            "result": result
        }
    else:
        deleted_count = delete_savedatas(resource_id)
        return {
            "status": "SUCCESS",
            "result": deleted_count
        }