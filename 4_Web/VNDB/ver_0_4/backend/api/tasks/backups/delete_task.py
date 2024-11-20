from typing import Optional, Dict, Union 
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import delete_backup, delete_backups, convert_model_to_dict

@celery.task(bind=True)
def delete_backups_task(
    self: Task,
    backup_id: Optional[str] = None
) -> Dict[str, Union[str, Union[Dict, int, None]]]:
    """
    Celery task to delete one or all backups.

    This task can delete either a single backup (if backup_id is provided) or all backups.
    It updates its state during execution and returns the result of the deletion operation.

    Args:
        self (Task): The Celery task instance (automatically injected by Celery).
        backup_id (Optional[str], optional): The ID of the specific backup to delete.
            If None, all backups will be deleted. Defaults to None.

    Returns:
        Dict[str, Union[str, Union[Dict, int, None]]]: A dictionary containing the status
        of the operation and its result. The structure is as follows:
        {
            "status": str,  # "SUCCESS", "NOT_FOUND", or "ERROR"
            "result": Union[Dict, int, str, None]  # Deleted backup data, count of deleted backups, or error message
        }

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
        This exception is handled by Celery's error handling mechanisms.

    Note:
        - The task updates its state to 'PROGRESS' during execution.
        - For single backup deletion, it returns the deleted backup data if found.
        - For all backups deletion, it returns the count of deleted backups.
        - The backup data is converted to a dictionary format using convert_model_to_dict.
    """

    self.update_state(state='PROGRESS', meta={'status': 'Deleting backup(s)...'})

    try:
        if backup_id:
            result = delete_backup(backup_id)
            if not result:
                return {"status": "NOT_FOUND", "result": f"Backup with id {backup_id} not found"}
            return {"status": "SUCCESS", "result": convert_model_to_dict(result)}
        else:
            deleted_count = delete_backups()
            if not deleted_count:
                return {"status": "NOT_FOUND", "result": "No backups found"}
            return {"status": "SUCCESS", "result": deleted_count}
    except SQLAlchemyError as e:
        # Log the error or handle it as appropriate for your application
        print(f"Database error in delete_backups_task: {str(e)}")
        return {
            "status": "ERROR",
            "result": f"An error occurred while deleting backup(s): {str(e)}"
        }