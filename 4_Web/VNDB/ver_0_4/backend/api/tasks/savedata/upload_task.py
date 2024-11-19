from typing import List, Dict, Any, Union

from datetime import datetime, timezone
import os

from celery import Task
from api import celery
from api.database import create_savedata, delete_savedata
from api.utils import get_savedata_folder
from api.database.models import SaveData

@celery.task(bind=True)
def upload_savedatas_task(self: Task, resource_id: str, files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Celery task to upload and process multiple savedata files for a given resource.

    Args:
        self (Task): The Celery task instance.
        resource_id (str): The ID of the resource (e.g., VN) associated with the savedata.
        files (List[Dict[str, Any]]): List of dictionaries containing file information.

    Returns:
        Dict[str, Any]: A dictionary containing the task status and upload results.
    """
    self.update_state(state='PROGRESS', meta={'status': 'Processing savedata files...'})

    upload_results: Dict[str, Union[bool, str]] = {}
    upload_folder: str = get_savedata_folder()
    os.makedirs(upload_folder, exist_ok=True)

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