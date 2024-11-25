from typing import Dict, List, Any

from api import celery
from api.search import (
    search_remote, search_local
)
from api.database import (
    get, get_all, create, update,
    delete, delete_all, exists, 
    convert_model_to_dict
)
from api.utils import convert_remote_to_local
from .common import error_handler

@error_handler
def _get_resource_task(resource_type: str, resource_id: str) -> Dict[str, Any]:
    result = get(resource_type, resource_id)
    return {
        'status': 'SUCCESS' if result else 'NOT_FOUND',
        'result': convert_model_to_dict(result) if result else None
    }

@error_handler
def _get_resources_task(resource_type: str, page: int = None, limit: int = None, sort: str = 'id', order: str = 'asc') -> Dict[str, Any]:
    result = get_all(resource_type, page=page, limit=limit, sort=sort, order=order)
    return {
        'status': 'SUCCESS' if result else None,
        'result': [convert_model_to_dict(item) for item in result] if result else []
    }

@error_handler
def _search_resource_task(resource_type: str, resource_id: str, response_size: str = 'small') -> Dict[str, Any]:
    search_results = search_local(resource_type, {'id': resource_id}, response_size)
    if search_results and isinstance(search_results, dict) and search_results.get('results'):
        search_results['status'] = 'SUCCESS'
        search_results['source'] = 'local'
        return search_results

    search_results = search_remote(resource_type, {'id': resource_id}, response_size)
    if search_results and isinstance(search_results, dict) and search_results.get('results'):
        search_results['status'] = 'SUCCESS'
        search_results['source'] = 'remote'
        return search_results

    return {'status': 'NOT_FOUND', 'result': None}

@error_handler
def _search_resources_task(resource_type: str, search_from: str, params: Dict[str, Any], response_size: str = 'small',
                           page: int = None, limit: int = None, sort: str = 'id', order: str = 'asc') -> Dict[str, Any]:
    if search_from == 'local':
        search_results = search_local(resource_type, params, response_size, page, limit, sort, order)
    elif search_from == 'remote':
        search_results = search_remote(resource_type, params, response_size, page, limit, sort, order)
    else:
        raise ValueError(f"Invalid search_from value: {search_from}. Only 'local' and 'remote' are supported.")
    
    if not search_results or not isinstance(search_results, dict) or not search_results.get('results'):
        return {'status': 'NOT_FOUND', 'result': None}

    search_results['status'] = 'SUCCESS'
    search_results['source'] = 'remote'
    return search_results
   
@error_handler
def _update_resource_task(resource_type: str, resource_id: str) -> Dict[str, Any]:
    remote_result = search_remote(resource_type, {'id':resource_id}, 'large')

    if not remote_result or not remote_result.get('results'):
        return {'status': 'NOT_FOUND', 'result': None}
    
    update_data = convert_remote_to_local(resource_type, remote_result['results'][0])

    if exists(resource_type, resource_id):
        data = update(resource_type, resource_id, update_data)
    else:
        data = create(resource_type, resource_id, update_data)
    
    return {
        'status': 'SUCCESS' if data else 'NOT_FOUND',
        'result': convert_model_to_dict(data) if data else None
    }

@error_handler
def _update_resources_task(resource_type: str) -> Dict[str, Any]:
    update_results = {}

    resources = get_all(resource_type)
    for resource in resources:
        result = _update_resource_task(resource_type, resource.id)
        update_results[resource.id] = True if result['status'] == 'SUCCESS' else False

    return {
        'status': 'ALL SUCCESS' if all(update_results.values()) else 'SOME FAILURE',
        'result': update_results
    }

@error_handler
def _delete_resource_task(resource_type: str, resource_id: str) -> Dict[str, Any]:
    result = delete(resource_type, resource_id)
    return {
        'status': 'SUCCESS' if result else 'NOT_FOUND',
        'result': convert_model_to_dict(result) if result else None
    }

@error_handler
def _delete_resources_task(resource_type: str) -> Dict[str, Any]:
    deleted_count = delete_all(resource_type)
    return {
        'status': 'SUCCESS' if deleted_count else 'NOT_FOUND',
        'result': deleted_count
    }

@error_handler
def _edit_resource_task(resource_type: str, resource_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    result = update(resource_type, resource_id, update_data)
    return {
        'status': 'SUCCESS' if result else 'NOT_FOUND',
        'result': convert_model_to_dict(result) if result else None
    }

@error_handler
def _edit_resources_task(resouce_type: str, update_datas: List[Dict[str, Any]]) -> Dict[str, Any]:
    update_results = {}

    for update_data in update_datas:
        resource_id = update_datas.pop('id')
        result = _edit_resource_task(resouce_type, resource_id, update_data)
        update_results[resource_id] = True if result['status'] == 'SUCCESS' else False

    return {
        'status': 'ALL SUCCESS' if all(update_results.values()) else 'SOME FAILURE',
        'result': update_results
    }

@celery.task
def get_resource_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_resource_task(*args, **kwargs)

@celery.task
def get_resources_task(*args, **kwargs) -> Dict[str, Any]:
    return _get_resources_task(*args, **kwargs)

@celery.task
def search_resource_task(*args, **kwargs) -> Dict[str, Any]:
    return _search_resource_task(*args, **kwargs)

@celery.task
def search_resources_task(*args, **kwargs) -> Dict[str, Any]:
    return _search_resources_task(*args, **kwargs)

@celery.task
def update_resource_task(*args, **kwargs) -> Dict[str, Any]:
    return _update_resource_task(*args, **kwargs)

@celery.task
def update_resources_task(*args, **kwargs) -> Dict[str, Any]:
    return _update_resources_task(*args, **kwargs)

@celery.task
def delete_resource_task(*args, **kwargs) -> Dict[str, Any]:
    return _delete_resource_task(*args, **kwargs)

@celery.task
def delete_resources_task(*args, **kwargs) -> Dict[str, Any]:
    return _delete_resources_task(*args, **kwargs)

@celery.task
def edit_resource_task(*args, **kwargs) -> Dict[str, Any]:
    return _edit_resource_task(*args, **kwargs)

@celery.task
def edit_resources_task(*args, **kwargs) -> Dict[str, Any]:
    return _edit_resources_task(*args, **kwargs)