from functools import wraps
from flask import abort, current_app
from app.services.user_services import get_user_by_id
from app.services.image_services import get_image_by_id
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

def entity_exists(entity_type, id_param, getter_function):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            entity_id = kwargs.get(id_param)
            if entity_id is None:
                abort(400, description=f"{entity_type.capitalize()} ID is required.")
            entity = getter_function(entity_id)
            if not entity:
                abort(404, description=f"{entity_type.capitalize()} not found.")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

user_exists = entity_exists('user', 'uid', get_user_by_id)
image_exists = entity_exists('image', 'id', get_image_by_id)