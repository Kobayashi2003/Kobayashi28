from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from api import db

def db_transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with db.session.begin_nested():
                result = func(*args, **kwargs)
            if result is None:
                return None
            db.session.commit()
            return result
        except (SQLAlchemyError, ValueError) as e:
            db.session.rollback()
            print(f"Error in {func.__name__}: {str(e)}")
            return None
    return wrapper