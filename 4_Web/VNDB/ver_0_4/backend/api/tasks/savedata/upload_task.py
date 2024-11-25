from typing import List, Dict, Any
from celery import Task

import os
from datetime import datetime, timezone

from api import celery
from api.database import create_savedata, delete_savedata
from api.utils import get_savedata_folder

@celery.task(bind=True)
def upload_savedatas_task(self: Task, resource_id: str, files: List[Dict[str, Any]]) -> Dict[str, Any]:
    self.update_state(state='PROGRESS', meta={'status': 'Processing savedata files...'})

    upload_results = {}
    upload_folder = get_savedata_folder()
    os.makedirs(upload_folder, exist_ok=True)

    try:
        for file_data in files:
            savedata_id = None
            savedata_path = None
            try:
                filename = file_data.get('filename', '')
                time = file_data.get('last_modified', datetime.now(timezone.utc))
                file_content = file_data.get('content', b'')
                if not file_content:
                    raise ValueError(f"Failed to read content of {filename}")

                savedata = create_savedata(resource_id, {'filename': filename, 'time': time})
                savedata_id = savedata.id
                savedata_path = os.path.join(upload_folder, f"{savedata_id}")

                with open(savedata_path, 'wb') as f:
                    f.write(file_content)

                upload_results[filename] = True
            except Exception as exc:
                if savedata_id is not None:
                    delete_savedata(resource_id, savedata_id)
                if savedata_path is not None and os.path.exists(savedata_path):
                    os.remove(savedata_path)
                upload_results[filename] = str(exc)

        return {"status": "SUCCESS", "result": upload_results}
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}