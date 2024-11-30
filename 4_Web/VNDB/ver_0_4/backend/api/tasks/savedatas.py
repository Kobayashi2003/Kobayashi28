from typing import Dict, List, Any 

import os
from datetime import datetime, timezone

from api.database import (
    get_savedata, get_savedatas,
    delete_savedata, delete_savedatas, 
    create_savedata 
)
from api.utils import (
    get_savedata_folder
)
from .common import (
    task_with_memoize, task_with_cache_clear, format_results
)

@task_with_memoize(timeout=600)
def get_savedata_task(resource_id: str, savedata_id: str = None) -> Dict[str, Any]:
    savedata = get_savedata(resource_id, savedata_id)
    return format_results(savedata)

@task_with_memoize(timeout=600)
def get_savedatas_task(resource_id: str) -> Dict[str, Any]:
    savedatas = get_savedatas(resource_id) 
    return format_results(savedatas)

@task_with_cache_clear
def upload_savedatas_task(resource_id: str, files: List[Dict[str, Any]]) -> Dict[str, Any]:
    upload_results = {}

    for file in files:
        filename = file.get('filename', '')
        result = upload_savedata_task(resource_id, file)
        upload_results[filename] = True if result.get('status') == 'SUCCESS' else False

    return format_results(upload_results)

@task_with_cache_clear
def upload_savedata_task(resource_id: str, file: Dict[str, Any]) -> Dict[str, Any]:
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

    return format_results(savedata)

@task_with_cache_clear
def delete_savedata_task(resource_id: str, savedata_id: str = None) -> Dict[str, Any]:
    result = delete_savedata(resource_id, savedata_id)
    return format_results(result)

@task_with_cache_clear
def delete_savedatas_task(resource_id: str) -> Dict[str, Any]:
    deleted_count = delete_savedatas(resource_id)
    return format_results(deleted_count)