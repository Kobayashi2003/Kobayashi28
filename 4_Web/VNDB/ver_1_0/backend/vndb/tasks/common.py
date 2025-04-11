from typing import Any

from functools import wraps

from vndb import celery, cache, db 
from vndb.database import convert_model_to_dict

NOT_FOUND = {'status': 'NOT_FOUND', 'result': None}

def format_results(results: Any) -> dict[str, Any]:
    if isinstance(results, db.Model):
        return {'status': 'SUCCESS','results': convert_model_to_dict(results)}
    elif isinstance(results, list) and all(isinstance(item, db.Model) for item in results):
        return {'status': 'SUCCESS', 'results': [convert_model_to_dict(item) for item in results]}
    elif isinstance(results, dict) and results.get('results'):
        results['status'] = 'SUCCESS'
        return results
    elif results:
        return {'status': 'SUCCESS','results': results}

    return NOT_FOUND

def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {"status": "ERROR", "results": str(e)}
    return wrapper

def clear_caches(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        cache.clear()
        return result
    return wrapper

def task_with_cache_clear(func):
    @celery.task
    @wraps(func)
    @error_handler
    @clear_caches
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def dont_cache(response):
    # Don't cache if the response is not a dict or if status is 'ERROR'
    return not isinstance(response, dict) or response.get('status') == 'ERROR'

def task_with_memoize(timeout=60*60*24):
    def decorator(func):
        @celery.task
        @wraps(func)
        @error_handler
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            result = cache.get(cache_key)
            if result is None:
                result = func(*args, **kwargs)
                if result['status'] == 'SUCCESS':
                    cache.set(cache_key, result, timeout=timeout)
            return result 
        return wrapper
    return decorator
