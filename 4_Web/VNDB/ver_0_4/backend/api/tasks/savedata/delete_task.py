from typing import Optional, Dict, Union
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import delete_savedata, delete_savedatas, convert_model_to_dict

@celery.task(bind=True)
def delete_savedatas_task(
    self: Task,
    resource_type: str,
    resource_id: str,
    savedata_id: Optional[str] = None
) -> Dict[str, Union[str, Union[Dict, int, None]]]:
    """
    Celery task to delete one or all savedatas associated with a resource.

    This task can delete either a single savedata (if savedata_id is provided) or all savedatas
    associated with a specific resource. It updates its state during execution and
    returns the result of the deletion operation.

    Args:
        self (Task): The Celery task instance (automatically injected by Celery).
        resource_type (str): The type of resource (e.g., 'vn').
        resource_id (str): The ID of the resource.
        savedata_id (Optional[str], optional): The ID of the specific savedata to delete.
            If None, all savedatas for the resource will be deleted. Defaults to None.

    Returns:
        Dict[str, Union[str, Union[Dict, int, None]]]: A dictionary containing the status
        of the operation and its result. The structure is as follows:
        {
            "status": str,  # "SUCCESS", "NOT_FOUND", or "ERROR"
            "result": Union[Dict, int, str, None]  # Deleted savedata data, count of deleted savedatas, or error message
        }

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
        This exception is handled by Celery's error handling mechanisms.

    Note:
        - The task updates its state to 'PROGRESS' during execution.
        - For single savedata deletion, it returns the deleted savedata data if successful.
        - For bulk deletion, it returns the count of deleted savedatas.
        - The savedata data is converted to a dictionary format using convert_model_to_dict.
    """

    self.update_state(state='PROGRESS', meta={'status': 'Deleting savedata(s)...'})
    
    try:
        if savedata_id:
            result = delete_savedata(resource_id, savedata_id)
            if not result:
                return {"status": "NOT_FOUND", "result": f"Savedata with id {savedata_id} not found for {resource_type} {resource_id}"}
            return {"status": "SUCCESS", "result": convert_model_to_dict(result)}
        else:
            deleted_count = delete_savedatas(resource_id)
            if not deleted_count:
                return {"status": "NOT_FOUND", "result": f"No savedatas found for {resource_type} {resource_id}"}
            return {"status": "SUCCESS", "result": deleted_count}
    except SQLAlchemyError as e:
        self.update_state(state='FAILURE', meta={'status': 'Database error occurred'})
        return {
            "status": "ERROR",
            "result": f"Database error during savedata deletion: {str(e)}"
        }
    except Exception as e:
        self.update_state(state='FAILURE', meta={'status': 'Unexpected error occurred'})
        return {
            "status": "ERROR",
            "result": f"Unexpected error during savedata deletion: {str(e)}"
        }