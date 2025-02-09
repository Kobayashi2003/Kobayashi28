from typing import Callable
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from imgserve import db
from .models import IMAGE_MODEL

def save_db_operation(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(type: str, *args, **kwargs):
        if type not in IMAGE_MODEL:
            return None
        try:
            return func(type, *args, **kwargs)
        except SQLAlchemyError:
            db.session.rollback()
            return None
    return wrapper