from typing import Dict, Union
from celery import Task

from api import celery
from api.database import delete_savedata, delete_savedatas, convert_model_to_dict

@celery.task(bind=True)
def delete_savedatas_task(self: Task, resource_id: str, savedata_id: str = None) -> Dict[str, Union[str, Union[Dict, int, None]]]:
    self.update_state(state='PROGRESS', meta={'status': 'Deleting savedata(s)...'})
    
    try:
        if savedata_id:
            result = delete_savedata(resource_id, savedata_id)
            if not result:
                return {"status": "NOT_FOUND", "result": None}
            return {"status": "SUCCESS", "result": convert_model_to_dict(result)}
        else:
            deleted_count = delete_savedatas(resource_id)
            if not deleted_count:
                return {"status": "NOT_FOUND", "result": None}
            return {"status": "SUCCESS", "result": deleted_count}
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}