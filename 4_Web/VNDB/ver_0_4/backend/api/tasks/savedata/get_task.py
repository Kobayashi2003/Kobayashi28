from typing import Optional

from api import celery
from api.database import get_savedata, get_savedatas, exists

@celery.task(bind=True)
def get_savedatas_task(self, resource_type: str, resource_id: str, savedata_id: Optional[str] = None):
    self.update_state(state='PROGRESS', meta={'status': 'Checking resource existence...'})
    if not exists(resource_type, resource_id):
        return {"status": "NOT_FOUND", "result": None}

    self.update_state(state='PROGRESS', meta={'status': 'Retrieving savedata(s)...'})

    if savedata_id:
        savedata = get_savedata(resource_id, savedata_id)
        return {
            "status": "SUCCESS" if savedata else "NOT_FOUND",
            "result": savedata
        }
    else:
        savedatas = get_savedatas(resource_id)
        return {
            "status": "SUCCESS" if savedatas else "NOT_FOUND",
            "result": savedatas
        }