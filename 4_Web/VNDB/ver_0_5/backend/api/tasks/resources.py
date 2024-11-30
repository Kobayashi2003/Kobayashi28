from typing import Dict, List, Any

from api.search import (
    search_remote, search_local,
    convert_remote_to_local 
)
from api.database import (
    get, get_all, create, update,
    delete, delete_all, exists, count 
)
from .common import (
    task_with_memoize, task_with_cache_clear,
    format_results, NOT_FOUND
)

@task_with_memoize(timeout=600)
def get_resource_task(resource_type: str, resource_id: str) -> Dict[str, Any]:
    result = get(resource_type, resource_id)
    return format_results(result)

@task_with_memoize(timeout=600)
def get_resources_task(resource_type: str, page: int = None, limit: int = None, sort: str = 'id', reverse: bool = False) -> Dict[str, Any]:
    results = get_all(resource_type, page, limit, sort, reverse)
    if not results:
        return NOT_FOUND
    total = count(resource_type)
    more = (page * limit) < total if page and limit else False

    results = format_results(results)
    results['count'] = total
    results['more'] = more
    return results

@task_with_memoize(timeout=600)
def search_resource_task(resource_type: str, resource_id: str, response_size: str = 'small') -> Dict[str, Any]:

    results = search_local(resource_type, {'id': resource_id}, response_size)
    if results and isinstance(results, dict) and results.get('results'):
        results = format_results(results)
        results['source'] = 'local'
        return results

    results = search_remote(resource_type, {'id': resource_id}, response_size)
    if results and isinstance(results, dict) and results.get('results'):
        results = format_results(results)
        results['source'] = 'remote'
        return results

    return NOT_FOUND

@task_with_memoize(timeout=600)
def search_resources_task(resource_type: str, search_from: str, params: Dict[str, Any], response_size: str = 'small',
                           page: int = None, limit: int = None, sort: str = 'id', reverse: bool = False, count: bool = True) -> Dict[str, Any]:
    if search_from == 'local':
        results = search_local(resource_type, params, response_size, page, limit, sort, reverse, count)
    elif search_from == 'remote':
        results = search_remote(resource_type, params, response_size, page, limit, sort, reverse, count)
    else:
        raise ValueError(f"Invalid search_from value: {search_from}. Only 'local' and 'remote' are supported.")
    
    if not results or not isinstance(results, dict) or not results.get('results'):
        return NOT_FOUND

    results = format_results(results)
    results['source'] = search_from
    return results
   
@task_with_cache_clear
def update_resource_task(resource_type: str, resource_id: str) -> Dict[str, Any]:
    remote_result = search_remote(resource_type, {'id':resource_id}, 'large')
    if not remote_result or not remote_result.get('results'):
        return NOT_FOUND
    
    update_data = convert_remote_to_local(resource_type, remote_result['results'][0])

    if exists(resource_type, resource_id):
        data = update(resource_type, resource_id, update_data)
    else:
        data = create(resource_type, resource_id, update_data)
    
    return format_results(data)

@task_with_cache_clear
def update_resources_task(resource_type: str) -> Dict[str, Any]:
    update_results = {}

    resources = get_all(resource_type)
    for resource in resources:
        result = update_resource_task(resource_type, resource.id)
        update_results[resource.id] = True if result['status'] == 'SUCCESS' else False

    return format_results(update_results)

@task_with_cache_clear
def delete_resource_task(resource_type: str, resource_id: str) -> Dict[str, Any]:
    result = delete(resource_type, resource_id)
    return format_results(result)

@task_with_cache_clear
def delete_resources_task(resource_type: str) -> Dict[str, Any]:
    deleted_count = delete_all(resource_type)
    return format_results(deleted_count)

@task_with_cache_clear
def edit_resource_task(resource_type: str, resource_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    result = update(resource_type, resource_id, update_data)
    return format_results(result)

@task_with_cache_clear
def edit_resources_task(resouce_type: str, update_datas: List[Dict[str, Any]]) -> Dict[str, Any]:
    update_results = {}

    for update_data in update_datas:
        resource_id = update_datas.pop('id')
        result = edit_resource_task(resouce_type, resource_id, update_data)
        update_results[resource_id] = True if result['status'] == 'SUCCESS' else False

    return format_results(update_results)