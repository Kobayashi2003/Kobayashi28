from typing import Any 

from vndb.database import (
    get_inactive, get_inactive_all,
    cleanup, cleanup_all,
    recover, recover_all,
    count_all 
)
from .common import (
    task_with_memoize, task_with_cache_clear, 
    format_results, NOT_FOUND
)

@task_with_memoize(timeout=600)
def get_inactive_resource_task(item_type: str, item_id: str) -> dict[str, Any]:
    result = get_inactive(item_type, item_id)
    return format_results(result)

@task_with_memoize(timeout=600)
def get_inactive_resources_task(item_type: str, page: int = None, limit: int = None, sort: str = 'id', reverse: bool = False, count: bool = True) -> dict[str, Any]:
    results = get_inactive_all(item_type, page, limit, sort, reverse)
    if not results:
        return NOT_FOUND
    total = count_all(item_type)
    more = (page * limit) < total if page and limit else False

    results = format_results(results)
    if count:
        results['count'] = total
    results['more'] = more
    return results

@task_with_cache_clear
def recover_resource_task(item_type: str, item_id: str) -> dict[str, Any]:
    result = recover(item_type, item_id)
    return format_results(result)

@task_with_cache_clear
def recover_resources_task(item_type: str) -> dict[str, Any]:
    results = recover_all(item_type)
    return format_results(results)

@task_with_cache_clear
def cleanup_resource_task(item_type: str, item_id: str) -> dict[str, Any]:
    result = cleanup(item_type, item_id)
    return format_results(result)

@task_with_cache_clear
def cleanup_resources_task(item_type: str) -> dict[str, Any]:
    results = cleanup_all(item_type)
    return format_results(results)