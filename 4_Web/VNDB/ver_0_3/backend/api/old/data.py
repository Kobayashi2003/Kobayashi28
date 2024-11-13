from flask import Blueprint, request, jsonify, abort 
from api import cache, celery
from ..tasks import get_data_task

data_bp = Blueprint('data', __name__)

@data_bp.route('/data/<string:data_type>/<string:id>', defaults={'data_size': 'small'}, methods=['GET'])
@data_bp.route('/data/<string:data_type>/<string:id>/<string:data_size>', methods=['GET'])
@cache.memoize(timeout=300)
def get_data(data_type, id, data_size):
    if data_type not in ['vn', 'character', 'tag', 'producer', 'staff', 'trait']:
        abort(400, description="Invalid data type")
    if data_size not in ['small', 'large']:
        abort(400, description="Invalid data size")

    task = get_data_task.delay(data_type, id, data_size)
    return jsonify({"task_id": task.id}), 202

@data_bp.route('/data/status/<task_id>')
def get_status(task_id):
    task = celery.AsyncResult(task_id)
    return jsonify({
        'state': task.state,
        'status': task.info.get('status', 'Task is in progress...') if task.state != 'FAILURE' else 'Task failed',
        'result': task.result if task.state == 'SUCCESS' else None,
        'error': str(task.result) if task.state == 'FAILURE' else None
    })

@data_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@data_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@data_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500