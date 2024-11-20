from typing import Optional, Dict, Union, List
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import get_backup, get_backups, convert_model_to_dict

@celery.task(bind=True)
def get_backups_task(
    self: Task, 
    backup_id: Optional[str] = None
) -> Dict[str, Union[str, Union[Dict, List[Dict], None]]]:
    """
    Celery task to retrieve one or all backups.

    This task can retrieve either a single backup (if backup_id is provided) or all backups.
    It updates its state during execution and returns the result of the retrieval operation.

    Args:
        self (Task): The Celery task instance (automatically injected by Celery).
        backup_id (Optional[str]): The ID of the specific backup to retrieve. If None, all backups will be retrieved.

    Returns:
        Dict[str, Union[str, Union[Dict, List[Dict], None]]]: A dictionary containing the status
        of the operation and its result. The structure is as follows:
        {
            "status": str,  # "SUCCESS", "NOT_FOUND", or "ERROR"
            "result": Union[Dict, List[Dict], None]  # Backup data, list of backup data, or error message
        }

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
        This exception is handled within the task.

    Note:
        - The task updates its state to 'PROGRESS' during execution.
        - For single backup retrieval, it returns the backup data if found.
        - For all backups retrieval, it returns a list of backup data.
        - The backup data is converted to a dictionary format using convert_model_to_dict.
    """

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
    except SQLAlchemyError as e:
        print(f"Database error in get_backups_task: {str(e)}")
        return {
            "status": "ERROR",
            "result": f"An error occurred while retrieving backup(s): {str(e)}"
        }