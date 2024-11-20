from typing import Optional, Dict, Union, List
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import get_savedata, get_savedatas, convert_model_to_dict

@celery.task(bind=True)
def get_savedatas_task(
    self: Task, 
    resource_id: str, 
    savedata_id: Optional[str] = None
) -> Dict[str, Union[str, Union[Dict, List[Dict], None]]]:
    """
    Celery task to retrieve one or all savedatas associated with a resource.

    This task can retrieve either a single savedata (if savedata_id is provided) or all savedatas
    associated with a specific resource. It updates its state during execution and
    returns the result of the retrieval operation.

    Args:
        self (Task): The Celery task instance (automatically injected by Celery).
        resource_id (str): The ID of the resource (e.g., VN) associated with the savedata.
        savedata_id (Optional[str]): The ID of the specific savedata to retrieve.
            If None, all savedatas for the resource will be retrieved. Defaults to None.

    Returns:
        Dict[str, Union[str, Union[Dict, List[Dict], None]]]: A dictionary containing the status
        of the operation and its result. The structure is as follows:
        {
            "status": str,  # "SUCCESS", "NOT_FOUND", or "ERROR"
            "result": Union[Dict, List[Dict], None]  # Savedata data, list of savedata data, or error message
        }

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
        This exception is handled within the task.

    Note:
        - The task updates its state to 'PROGRESS' during execution.
        - For single savedata retrieval, it returns the savedata data if found.
        - For all savedatas retrieval, it returns a list of savedata data.
        - The savedata data is converted to a dictionary format using convert_model_to_dict.
    """
    self.update_state(state='PROGRESS', meta={'status': 'Retrieving savedata(s)...'})

    try:
        if savedata_id:
            # Retrieve a single savedata
            savedata = get_savedata(resource_id, savedata_id)
            return {
                "status": "SUCCESS" if savedata else "NOT_FOUND",
                "result": convert_model_to_dict(savedata) if savedata else None
            }
        else:
            # Retrieve all savedatas for the resource
            savedatas = get_savedatas(resource_id)
            return {
                "status": "SUCCESS" if savedatas else "NOT_FOUND",
                "result": [convert_model_to_dict(savedata) for savedata in savedatas if savedata is not None]
            }
    except SQLAlchemyError as e:
        print(f"Database error in get_savedatas_task: {str(e)}")
        return {
            "status": "ERROR",
            "result": f"An error occurred while retrieving savedata(s): {str(e)}"
        }