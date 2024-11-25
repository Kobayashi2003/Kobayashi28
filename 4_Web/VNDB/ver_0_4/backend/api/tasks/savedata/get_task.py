from typing import Dict, Union
from celery import Task

from api import celery
from api.database import get_savedata, get_savedatas, convert_model_to_dict

@celery.task(bind=True)
def get_savedatas_task(self: Task, resource_id: str, savedata_id: str = None) -> Dict[str, Union[str, Union[Dict, list, None]]]:
    self.update_state(state='PROGRESS', meta={'status': 'Retrieving savedata(s)...'})

    try:
        if savedata_id:
            savedata = get_savedata(resource_id, savedata_id)
            return {
                "status": "SUCCESS" if savedata else "NOT_FOUND",
                "result": convert_model_to_dict(savedata) if savedata else None
            }
        else:
            savedatas = get_savedatas(resource_id)
            return {
                "status": "SUCCESS" if savedatas else "NOT_FOUND",
                "result": [convert_model_to_dict(savedata) for savedata in savedatas if savedata is not None]
            }
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}