from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.services import user_services
from flask_restx import abort

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        if not user_services.is_admin(current_user_id):
            abort(403, 'Admin privileges required')
        return fn(*args, **kwargs)
    return wrapper