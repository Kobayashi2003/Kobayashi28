from typing import List, Dict, Any, Union
from celery import Task
from sqlalchemy.exc import SQLAlchemyError

import os
from datetime import datetime, timezone

from api import celery
from api.database import create_savedata, delete_savedata
from api.utils import get_savedata_folder
from api.database.models import SaveData

@celery.task(bind=True)
def upload_savedatas_task(
    self: Task, 
    resource_id: str, 
    files: List[Dict[str, Any]]
) -> Dict[str, Union[str, Dict[str, Union[bool, str]]]]:
    """
    Celery task to upload and process multiple savedata files for a given resource.

    This task processes multiple savedata files, creates database records, and saves the files.
    It updates its state during execution and returns the result of the upload operation.

    Args:
        self (Task): The Celery task instance (automatically injected by Celery).
        resource_id (str): The ID of the resource (e.g., VN) associated with the savedata.
        files (List[Dict[str, Any]]): List of dictionaries containing file information.

    Returns:
        Dict[str, Union[str, Dict[str, Union[bool, str]]]]: A dictionary containing the status
        of the operation and its result. The structure is as follows:
        {
            "status": str,  # "SUCCESS" or "ERROR"
            "result": Dict[str, Union[bool, str]]  # Upload results for each file
        }

    Raises:
        SQLAlchemyError: If there's an issue with the database operation.
        OSError: If there's an issue with file operations.
        These exceptions are handled within the task.

    Note:
        - The task updates its state to 'PROGRESS' during execution.
        - For each file, it creates a savedata record and saves the file content.
        - In case of failure for a specific file, it cleans up by deleting the record and file.
    """

    self.update_state(state='PROGRESS', meta={'status': 'Processing savedata files...'})

    upload_results: Dict[str, Union[bool, str]] = {}
    upload_folder: str = get_savedata_folder()
    os.makedirs(upload_folder, exist_ok=True)

    try:
        for file_data in files:
            savedata_id: Union[str, None] = None
            savedata_path: Union[str, None] = None
            try:
                filename: str = file_data.get('filename', '')
                time: datetime = file_data.get('last_modified', datetime.now(timezone.utc))
                file_content: bytes = file_data.get('content', b'')
                if not file_content:
                    raise ValueError(f"Failed to read content of {filename}")

                # Create savedata record in database
                savedata: SaveData = create_savedata(resource_id, {'filename': filename, 'time': time})

                savedata_id = savedata.id
                savedata_path = os.path.join(upload_folder, f"{savedata_id}")

                # Save the savedata file
                with open(savedata_path, 'wb') as f:
                    f.write(file_content)

                upload_results[filename] = True
            except Exception as exc:
                # Clean up in case of failure
                if savedata_id is not None:
                    delete_savedata(resource_id, savedata_id)
                if savedata_path is not None and os.path.exists(savedata_path):
                    os.remove(savedata_path)
                upload_results[filename] = str(exc)

        return {"status": "SUCCESS", "result": upload_results}
    except (SQLAlchemyError, OSError) as e:
        print(f"Error in upload_savedatas_task: {str(e)}")
        return {"status": "ERROR", "result": f"An error occurred during savedata upload: {str(e)}"}