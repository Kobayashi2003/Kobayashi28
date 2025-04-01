from typing import Any

from vndb.search import (
    search_remote, search_local,
    convert_remote_to_local
)
from vndb.database import (
    get_all, create, update, updatable,
    delete, delete_all, exists
)
from .common import (
    task_with_memoize, task_with_cache_clear,
    format_results, NOT_FOUND
)

@task_with_memoize(timeout=600)
def get_resource_task(resource_type: str, resource_id: str, response_size: str = 'small') -> dict[str, Any]:
    results = search_local(resource_type, {'id': resource_id}, response_size)
    if not results or not isinstance(results, dict) or not results.get('results'):
        return NOT_FOUND

    results = format_results(results)
    results['source'] = 'local'
    return results

@task_with_memoize(timeout=600)
def get_resources_task(resource_type: str, args: dict[str, Any], response_size: str = 'small',
                       page: int = 1, limit: int = 20, sort: str = 'id', reverse: bool = False, count: bool = True) -> dict[str, Any]:
    results = search_local(resource_type, args, response_size, page, limit, sort, reverse, count)
    if not results or not isinstance(results, dict) or not results.get('results'):
        return NOT_FOUND

    results = format_results(results)
    results['source'] = 'local'
    return results

@task_with_memoize(timeout=600)
def search_resource_task(resource_type: str, resource_id: str, response_size: str = 'small') -> dict[str, Any]:
    results = search_remote(resource_type, {'id': resource_id}, response_size)
    if not results or not isinstance(results, dict) or not results.get('results'):
        return NOT_FOUND

    if response_size == 'large':
        synchronize_resources_task.delay(resource_type, results['results'])

    results = format_results(results)
    results['source'] = 'remote'
    return results

@task_with_memoize(timeout=600)
def search_resources_task(resource_type: str, params: dict[str, Any], response_size: str = 'small',
                           page: int = 1, limit: int = 20, sort: str = 'id', reverse: bool = False, count: bool = True) -> dict[str, Any]:
    results = search_remote(resource_type, params, response_size, page, limit, sort, reverse, count)
    if not results or not isinstance(results, dict) or not results.get('results'):
        return NOT_FOUND

    if response_size == 'large':
        synchronize_resources_task.delay(resource_type, results['results'])

    results = format_results(results)
    results['source'] = 'remote'
    return results
   
@task_with_cache_clear
def update_resource_task(resource_type: str, resource_id: str) -> dict[str, Any]:
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
def update_resources_task(resource_type: str) -> dict[str, Any]:
    update_results = {}

    resources = get_all(resource_type)
    for resource in resources:
        result = update_resource_task(resource_type, resource.id)
        update_results[resource.id] = True if result['status'] == 'SUCCESS' else False

    return format_results(update_results)

@task_with_cache_clear
def delete_resource_task(resource_type: str, resource_id: str) -> dict[str, Any]:
    result = delete(resource_type, resource_id)
    return format_results(result)

@task_with_cache_clear
def delete_resources_task(resource_type: str) -> dict[str, Any]:
    deleted_count = delete_all(resource_type)
    return format_results(deleted_count)

@task_with_cache_clear
def edit_resource_task(resource_type: str, resource_id: str, update_data: dict[str, Any]) -> dict[str, Any]:
    result = update(resource_type, resource_id, update_data)
    return format_results(result)

@task_with_cache_clear
def edit_resources_task(resouce_type: str, update_datas: list[dict[str, Any]]) -> dict[str, Any]:
    update_results = {}

    for update_data in update_datas:
        resource_id = update_datas.pop('id')
        result = edit_resource_task(resouce_type, resource_id, update_data)
        update_results[resource_id] = True if result['status'] == 'SUCCESS' else False

    return format_results(update_results)


@task_with_cache_clear
def synchronize_resources_task(resource_type: str, results: list[dict[str, Any]]) -> dict[str, dict[str, bool]]:
    created = {}
    updated = {}
    for result in results:
        id = result['id']
        if not exists(resource_type, id):
            created[id] = (create(resource_type, id, result) is not None)
        elif updatable(resource_type, id):
            updated[id] = (update(resource_type, id, result) is not None)
    return {'created': created, 'updated': updated}
