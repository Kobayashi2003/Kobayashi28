from typing import Dict, Any 

from api.database import (
    count, get_inactive, 
    get_inactive_type, get_inactive_all,
    cleanup, cleanup_type, cleanup_all,
    recover, recover_type, recover_all
)
from .common import (
    task_with_memoize, task_with_cache_clear, 
    format_results, NOT_FOUND
)

@task_with_memoize(timeout=600)
def get_inactive_item_task(item_type: str, item_id: str) -> Dict[str, Any]:
    result = get_inactive(item_type, item_id)
    return format_results(result)

@task_with_memoize(timeout=600)
def get_inactive_type_task(item_type: str, page: int = None, limit: int = None, sort: str = 'id', reverse: bool = False) -> Dict[str, Any]:
    results = get_inactive_type(item_type, page, limit, sort, reverse)
    if not results:
        return NOT_FOUND
    total = count(item_type)
    more = (page * limit) < total if page and limit else False

    results = format_results(results)
    results['count'] = total
    results['more'] = more
    return results

@task_with_memoize(timeout=600)
def get_inactive_all_task() -> Dict[str, Any]:
    results = get_inactive_all()
    # TODO

@task_with_cache_clear
def recover_item_task(item_type: str, item_id: str) -> Dict[str, Any]:
    result = recover(item_type, item_id)
    return format_results(result)

@task_with_cache_clear
def recover_type_task(item_type: str) -> Dict[str, Any]:
    results = recover_type(item_type)
    return format_results(results)

@task_with_cache_clear
def recover_all_task() -> Dict[str, Any]:
    results = recover_all()
    return format_results(results)

@task_with_cache_clear
def cleanup_item_task(item_type: str, item_id: str) -> Dict[str, Any]:
    result = cleanup(item_type, item_id)
    return format_results(result)

@task_with_cache_clear
def cleanup_type_task(item_type: str) -> Dict[str, Any]:
    results = cleanup_type(item_type)
    return format_results(results)

@task_with_cache_clear
def cleanup_all_task() -> Dict[str, Any]:
    results = cleanup_all()
    return format_results(results)