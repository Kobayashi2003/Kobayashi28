from functools import wraps 
from flask import abort, request
from flask_jwt_extended import get_jwt_identity, jwt_required

def login_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_uid = get_jwt_identity()
        request_uid = None

        if 'uid' in kwargs:
            request_uid = kwargs['uid']
        elif request.is_json:
            request_uid = request.json.get('uid')
        elif request.form:
            request_uid = request.form.get('uid')
        elif request.args:
            request_uid = request.args.get('uid')

        if request_uid and str(request_uid) != current_uid:
            abort(403, description="You don't have permission to perform this action.")

        return f(*args, **kwargs)

    return decorated_function
