from typing import Dict 
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import restore_database_pg_dump 
from api.utils import get_backup_path

@celery.task(bind=True)
def restore_task(
    self: Task, 
    backup_id: str
) -> Dict[str, str]:
    """
    Celery task to restore a database from a backup.

    This task attempts to restore the database from a specified backup. It updates its state
    during execution and returns the result of the restore operation.

    Args:
        self (Task): The Celery task instance (automatically injected by Celery).
        backup_id (str): The ID of the backup to restore from.

    Returns:
        Dict[str, str]: A dictionary containing the status of the operation and its result.
        The structure is as follows:
        {
            "status": str,  # "SUCCESS" or "ERROR"
            "result": str   # Success message or error description
        }

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
        Exception: For any other unexpected errors.
        Both exceptions are caught and handled within the task.

    Note:
        - The task updates its state to 'PROGRESS' at the start of the operation.
        - If an error occurs, the task state is updated to 'FAILURE'.
        - The task uses get_backup_path to locate the backup file and restore_database_pg_dump
          to perform the actual restore operation.
    """

    self.update_state(state='PROGRESS', meta={'status': 'Restoring backup...'})
    try:
        backup_path = get_backup_path(backup_id)
        restore_database_pg_dump(backup_path)
        return {"status": "SUCCESS", "result": f"Database restored from backup {backup_id}"}
    except SQLAlchemyError as e:
        self.update_state(state='FAILURE', meta={'status': 'Database error occurred'})
        return {
            "status": "ERROR",
            "result": f"Database error during restore: {str(e)}"
        }
    except Exception as e:
        self.update_state(state='FAILURE', meta={'status': 'Unexpected error occurred'})
        return {
            "status": "ERROR",
            "result": f"Unexpected error during restore: {str(e)}"
        }