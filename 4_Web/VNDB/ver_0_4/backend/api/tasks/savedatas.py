from typing import Dict, List, Any 

import os
from datetime import datetime, timezone

from api import celery
from api.database import (
    get_savedata, get_savedatas,
    delete_savedata, delete_savedatas, 
    create_savedata, convert_model_to_dict
)
from api.utils import get_savedata_folder
from .common import error_handler

@error_handler
def _delete_savedata_task(resource_id: str, savedata_id: str = None) -> Dict[str, Any]:
    result = delete_savedata(resource_id, savedata_id)
    return {
        'status': 'SUCCESS' if result else 'NOT_FOUND',
        'result': convert_model_to_dict(result) if result else None
    }

@error_handler
def _delete_savedatas_task(resource_id: str) -> Dict[str, Any]:
    deleted_count = delete_savedatas(resource_id)
    return {
        'status': 'SUCCESS' if deleted_count else 'NOT_FOUND',
        'result': deleted_count
    }

@error_handler
def _get_savedata_task(resource_id: str, savedata_id: str = None) -> Dict[str, Any]:
    savedata = get_savedata(resource_id, savedata_id)
    return {
        "status": "SUCCESS" if savedata else "NOT_FOUND",
        "result": convert_model_to_dict(savedata) if savedata else None
    }

@error_handler
def _get_savedatas_task(resource_id: str) -> Dict[str, Any]:
    savedatas = get_savedatas(resource_id) 
    return {
        "status": "SUCCESS" if savedatas else "NOT_FOUND",
        "result": [convert_model_to_dict(savedata) for savedata in savedatas if savedata is not None]
    }

@error_handler
def _upload_savedatas_task(resource_id: str, files: List[Dict[str, Any]]) -> Dict[str, Any]:
    upload_results = {}

    for file in files:
        filename = file.get('filename', '')
        result = _upload_savedata_task(resource_id, file)
        upload_results[filename] = True if result.get('status') == 'SUCCESS' else False

    return {
        'status': 'ALL SUCCESS' if all(upload_results.values()) else 'SOME FAILURE',
        'result': upload_results
    }

@error_handler
def _upload_savedata_task(resource_id: str, file: Dict[str, Any]) -> Dict[str, Any]:
    upload_folder = get_savedata_folder()
    os.makedirs(upload_folder, exist_ok=True)

    filename = file.get('filename', '')
    last_modified = file.get('last_modified', datetime.now(timezone.utc))
    file_content = file.get('content', b'')
    if not file_content:
        raise ValueError(f"Failed to read content of {filename}")

    savedata = create_savedata(resource_id, {'filename': filename, 'time': last_modified})
    if not savedata:
        raise ValueError(f"Failed to create savedata for {filename}")

    savedata_id = savedata.id
    savedata_path = os.path.join(upload_folder, f"{savedata_id}")

    with open(savedata_path, 'wb') as f:
        f.write(file_content)

    return {
        'status': 'SUCCESS',
        'result': convert_model_to_dict(savedata)
    }

@celery.task
def delete_savedata_task(*args, **kwargs) -> Dict[str, Any]:
    return _delete_savedata_task(*args, **kwargs)

@celery.task
def delete_savedatas_task(*args, **kwargs) -> Dict[str, Any]:
    return _delete_savedatas_task(*args, **kwargs)

@celery.task
def get_savedata_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_savedata_task(*args, **kwargs)

@celery.task
def get_savedatas_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_savedatas_task(*args, **kwargs)

@celery.task
def upload_savedatas_task(*args, **kwargs) -> Dict[str, Any]:
    return _upload_savedatas_task(*args, **kwargs)

@celery.task
def upload_savedata_task(*args, **kwargs) -> Dict[str, Any]:
    return _upload_savedata_task(*args, **kwargs)