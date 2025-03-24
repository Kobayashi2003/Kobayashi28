from typing import Callable
from functools import wraps
from imgserve import db
from .models import IMAGE_MODEL

def save_db_operation(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(type: str, *args, **kwargs):
        if type not in IMAGE_MODEL:
            return None
        try:
            return func(type, *args, **kwargs)
        except Exception as e:
            db.session.rollback()
            print(f"Error in {func.__name__}: {str(e)}")
            return None
    return wrapper