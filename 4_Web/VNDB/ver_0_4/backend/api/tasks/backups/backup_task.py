from typing import Dict, Union
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from api import celery
from api.database import create_backup 

@celery.task(bind=True)
def backup_task(self: Task) -> Dict[str, Union[str, None]]:
    """
    Celery task to create a database backup.

    This task attempts to create a backup of the database. It updates its state
    during execution and returns the result of the backup operation.

    Args:
        self (Task): The Celery task instance (automatically injected by Celery).

    Returns:
        Dict[str, Union[str, None]]: A dictionary containing the status
        of the operation and its result. The structure is as follows:
        {
            "status": str,  # "SUCCESS" or "ERROR"
            "result": str  # Backup ID or error message
        }

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
        Exception: For any other unexpected errors.
        Both exceptions are caught and handled within the task.

    Note:
        - The task updates its state to 'PROGRESS' at the start and after successful completion.
        - If an error occurs, the task state is updated to 'FAILURE'.
        - The backup_id is returned on successful backup creation.
    """

    self.update_state(state='PROGRESS', meta={'status': 'Starting database backup...'})

    try:
        backup_id = create_backup()
        self.update_state(state='PROGRESS', meta={'status': 'Backup completed successfully.'})
        return {"status": "SUCCESS", "result": f"Database backup created successfully: {backup_id}"}
    except SQLAlchemyError as e:
        self.update_state(state='FAILURE', meta={'status': 'Database error occurred'})
        return {
            "status": "ERROR",
            "result": f"Database error during backup: {str(e)}"
        }
    except Exception as e:
        self.update_state(state='FAILURE', meta={'status': 'Unexpected error occurred'})
        return {
            "status": "ERROR",
            "result": f"Unexpected error during backup: {str(e)}"
        }