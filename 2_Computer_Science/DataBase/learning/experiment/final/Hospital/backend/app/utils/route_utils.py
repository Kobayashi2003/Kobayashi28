from functools import wraps
from flask import abort, current_app
from app.logger import logger

def error_handler(status_code, message):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as exc:
                if current_app.debug:
                    logger.exception(f'{message}:{str(exc)}')
                    abort(status_code, description=message)
                else:
                    logger.error(f'{message}:{str(exc)}')
                    abort(status_code, description='An error occurred. Please try again later.')
        return decorated_function
    return decorator