from imgserve import scheduler
from functools import wraps

def test_task(func):
    @wraps(func)
    @scheduler.task(trigger='interval', id=f'test_{func.__name__}', seconds=10)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def hourly_task(minute=0):
    def decorator(func):
        @wraps(func)
        @scheduler.task(trigger='cron', id=f'hourly_{func.__name__}', minute=minute)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def daily_task(hour=0, minute=0):
    def decorator(func):
        @wraps(func)
        @scheduler.task(trigger='cron', id=f'daily_{func.__name__}', hour=hour, minute=minute)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def weekly_task(day_of_week=0, hour=0, minute=0):
    def decorator(func):
        @wraps(func)
        @scheduler.task(trigger='cron', id=f'weekly_{func.__name__}', day_of_week=day_of_week, hour=hour, minute=minute)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator