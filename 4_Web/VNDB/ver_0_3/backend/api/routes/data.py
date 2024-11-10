from flask import Blueprint, request, jsonify, abort 

from api.celery_app import celery
from api.cache_app import cache
from api.tasks import get_data_task
from api.search.local.search import search as local_search
from api.search.remote.search import search as remote_search

data_bp = Blueprint('data', __name__)

@data_bp.route('/api/data/<string:data_type>/<string:id>', defaults={'data_size': 'small'}, methods=['GET'])
@data_bp.route('/api/data/<string:data_type>/<string:id>/<string:data_size>', methods=['GET'])
@cache.memoize(timeout=300)
def get_data(data_type, id, data_size):
    if data_type not in ['vn', 'character', 'tag', 'producer', 'staff', 'trait']:
        abort(400, description="Invalid data type")
    if data_size not in ['small', 'large']:
        abort(400, description="Invalid data size")

    task = get_data_task.delay(data_type, id, data_size)
    return jsonify({"task_id": task.id}), 202

@data_bp.route('/api/data/status/<task_id>')
def get_status(task_id):
    task_result = celery.AsyncResult(task_id)
    if task_result.state == 'PENDING':
        response = {
            'state': task_result.state,
            'status': 'Task is pending...'
        }
    elif task_result.state != 'FAILURE':
        response = {
            'state': task_result.state,
            'status': task_result.info.get('status', '')
        }
        if 'result' in task_result.info:
            response['result'] = task_result.info['result']
    else:
        response = {
            'state': task_result.state,
            'status': str(task_result.info)
        }
    return jsonify(response)

@data_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@data_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@data_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500