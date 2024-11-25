from typing import Dict, Any

from api import celery
from api.search import (
    search_resources_by_vnid, 
    search_resources_by_charid
)
from api.database import (
    exists, create, update,
    get_all_related, delete_all_related, 
)
from api.utils import convert_remote_to_local
from .common import error_handler

@error_handler
def _get_related_resources_task(resource_type: str, resource_id: str, related_resource_type: str) -> Dict[str, Any]:
    result = get_all_related(resource_type, resource_id, related_resource_type)
    return {
        'status': 'SUCCESS' if result else 'NOT_FOUND',
        'result': result if result else None
    }

@error_handler
def _search_related_resources_task(resource_type: str, resource_id: str, related_resource_type: str, response_size: str = 'small') -> Dict[str, Any]:
    
    if resource_type == 'vn':
        search_results = search_resources_by_vnid(resource_id, related_resource_type, response_size)
    elif resource_type == 'character':
        search_results = search_resources_by_charid(resource_id, related_resource_type, response_size)
    else:
        raise ValueError(f"Invalid resource_type: {resource_type}. Only 'vn' and 'character' are supported.")
    
    if not search_results or not isinstance(search_results, dict) or not search_results.get('results'):
        raise ValueError(f"No related {related_resource_type} found for {resource_type} {resource_id}")

    return {
        'status': 'SUCCESS' if search_results else 'NOT_FOUND',
        'result': search_results
    }

@error_handler
def _update_related_resources_task(resource_type: str, resource_id: str, related_resource_type: str) -> Dict[str, Any]:
    if resource_type == 'vn':
        related_data = search_resources_by_vnid(resource_id, related_resource_type, 'large')
    elif resource_type == 'character':
        related_data = search_resources_by_charid(resource_id, related_resource_type, 'large')
    else:
        raise ValueError(f"Invalid resource_type: {resource_type}. Only 'vn' and 'character' are supported.")

    if not related_data or not isinstance(related_data, dict) or not related_data.get('results'):
        raise ValueError(f"No related {related_resource_type} found for {resource_type} {resource_id}")

    update_results = {}

    for item in related_data['results']:
        id = item['id']
        try:
            update_data = convert_remote_to_local(related_resource_type, item) 
            if exists(related_resource_type, id):
                data = update(related_resource_type, id, update_data)
            else:
                data = create(related_resource_type, id, update_data)
            if not data:
                update_results[id] = False
            else:
                update_results[id] = True
            
        except Exception as exc:
            update_results[id] = False

    return {
        'status': 'ALL SUCCESS' if all(update_results.values()) else 'SOME FAILURE',
        'result': update_results
    }

@error_handler
def _delete_related_resources_task(resource_type: str, resource_id: str, related_resource_type: str) -> Dict[str, Any]:
    deleted_count = delete_all_related(resource_type, resource_id, related_resource_type)
    return {
        'status': 'SUCCESS' if deleted_count else 'NOT_FOUND',
        'result': deleted_count
    }

@celery.task
def get_related_resources_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_related_resources_task(*args, **kwargs)

@celery.task
def search_related_resources_task(*args, **kwargs) -> Dict[str, Any]:
    return _search_related_resources_task(*args, **kwargs)

@celery.task
def update_related_resources_task(*args, **kwargs) -> Dict[str, Any]:
    return _update_related_resources_task(*args, **kwargs)

@celery.task
def delete_related_resources_task(*args, **kwargs) -> Dict[str, Any]:
    return _delete_related_resources_task(*args, **kwargs)