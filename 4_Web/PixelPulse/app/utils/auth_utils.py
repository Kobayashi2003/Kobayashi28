from functools import wraps
from flask import abort
from flask_jwt_extended import get_jwt_identity, jwt_required

def login_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_uid = get_jwt_identity()
        if 'uid' in kwargs and str(kwargs['uid']) != current_uid:
            abort(403, description="You don't have permission to perform this action.")
        return f(*args, **kwargs)
    return decorated_function
