from typing import List, Dict 

import io
import os
from datetime import datetime, timezone
from flask import current_app
from api import celery
from api.database import exists, create, next_savedata_id

@celery.task(bind=True)
def upload_savedatas_task(self, resource_type: str, resource_id: str, files: List[Dict]):
    self.update_state(state='PROGRESS', meta={'status': 'Checking resource existence...'})
    if not exists(resource_type, resource_id):
        return {"status": "NOT_FOUND", "result": None}

    self.update_state(state='PROGRESS', meta={'status': 'Processing savedata files...'})

    upload_results = {}
    upload_folder = current_app.config['SAVEDATA_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    for file_data in files:
        savedata_id = next_savedata_id()
        filename = file_data.get('filename', savedata_id)
        file_time = file_data.get('last_modified', datetime.now(timezone.utc))
        file_content = io.BytesIO(file_data['content'])
        savedata_data = {
            'vnid': resource_id,
            'time': file_time,
            'filename': filename
        }
        try:
            create('savedata', savedata_id, savedata_data)

            savedata_path = os.path.join(upload_folder, f"{savedata_id}")
            with open(savedata_path, 'wb') as f:
                f.write(file_content)

            upload_results[filename] = True

        except Exception as exc:
            upload_results[filename] = False
            if 'savedata_path' in locals() and os.path.exists(savedata_path):
                os.remove(savedata_path)

    return {"status": "SUCCESS", "result": upload_results}