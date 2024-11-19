from typing import Optional, Dict, Any, List
from celery import Task

from api import celery
from api.database import get_savedata, get_savedatas, convert_model_to_dict
from api.database.models import SaveData

@celery.task(bind=True)
def get_savedatas_task(self: Task, resource_id: str, savedata_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Celery task to retrieve savedata(s) for a given resource.

    Args:
        self (Task): The Celery task instance.
        resource_id (str): The ID of the resource (e.g., VN) associated with the savedata.
        savedata_id (Optional[str]): The specific savedata ID to retrieve, if any.

    Returns:
        Dict[str, Any]: A dictionary containing the task status and retrieved savedata(s) information.
    """
    self.update_state(state='PROGRESS', meta={'status': 'Retrieving savedata(s)...'})

    if savedata_id:
        # Retrieve a single savedata
        savedata: Optional[SaveData] = get_savedata(resource_id, savedata_id)
        return {
            "status": "SUCCESS" if savedata else "NOT_FOUND",
            "result": convert_model_to_dict(savedata) if savedata else None
        }
    else:
        # Retrieve all savedatas for the resource
        savedatas: List[SaveData] = get_savedatas(resource_id)
        return {
            "status": "SUCCESS" if savedatas else "NOT_FOUND",
            "result": [convert_model_to_dict(savedata) for savedata in savedatas if savedata is not None]
        }