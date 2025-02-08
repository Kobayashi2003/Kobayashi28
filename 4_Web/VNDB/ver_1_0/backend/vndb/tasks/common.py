from typing import Any, Dict

from functools import wraps

from vndb import celery, cache, db, scheduler
from vndb.database import convert_model_to_dict

NOT_FOUND = {'status': 'NOT_FOUND','result': None}

def format_results(results: Any) -> Dict[str, Any]:
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
            return {"status": "ERROR", "result": str(e)}
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

def task_with_memoize(timeout=600):
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

def daily_task(hour=0, minute=0):
    """
    Decorator for tasks that should run daily at a specific time.

    :param hour: Hour of the day (0-23)
    :param minute: Minute of the hour (0-59)
    """
    def decorator(func):
        @wraps(func)
        @scheduler.task(trigger='cron', id=f'daily_{func.__name__}', hour=hour, minute=minute)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def weekly_task(day_of_week=0, hour=0, minute=0):
    """
    Decorator for tasks that should run weekly on a specific day and time.

    :param day_of_week: Day of the week (0-6, where 0 is Monday)
    :param hour: Hour of the day (0-23)
    :param minute: Minute of the hour (0-59)
    """
    def decorator(func):
        @wraps(func)
        @scheduler.task(trigger='cron', id=f'weekly_{func.__name__}', day_of_week=day_of_week, hour=hour, minute=minute)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def monthly_task(day=1, hour=0, minute=0):
    """
    Decorator for tasks that should run monthly on a specific day and time.

    :param day: Day of the month (1-31)
    :param hour: Hour of the day (0-23)
    :param minute: Minute of the hour (0-59)
    """
    def decorator(func):
        @wraps(func)
        @scheduler.task(trigger='cron', id=f'monthly_{func.__name__}', day=day, hour=hour, minute=minute)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def hourly_task(minute=0):
    """
    Decorator for tasks that should run every hour at a specific minute.

    :param minute: Minute of the hour (0-59)
    """
    def decorator(func):
        @wraps(func)
        @scheduler.task(trigger='cron', id=f'hourly_{func.__name__}', minute=minute)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def custom_interval_task(minutes=0, hours=0, days=0):
    """
    Decorator for tasks that should run at custom intervals.

    :param minutes: Number of minutes between runs
    :param hours: Number of hours between runs
    :param days: Number of days between runs
    """
    def decorator(func):
        @wraps(func)
        @scheduler.task(trigger='interval', id=f'interval_{func.__name__}', minutes=minutes, hours=hours, days=days)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def workday_task(hour=9, minute=0):
    """
    Decorator for tasks that should run every workday (Monday to Friday) at a specific time.

    :param hour: Hour of the day (0-23)
    :param minute: Minute of the hour (0-59)
    """
    def decorator(func):
        @wraps(func)
        @scheduler.task(trigger='cron', id=f'workday_{func.__name__}', day_of_week='mon-fri', hour=hour, minute=minute)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def test_task(func):
    """
    Decorator for test tasks that should run every 10 seconds.
    """
    @wraps(func)
    @scheduler.task(trigger='interval', id=f'test_{func.__name__}', seconds=30)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper