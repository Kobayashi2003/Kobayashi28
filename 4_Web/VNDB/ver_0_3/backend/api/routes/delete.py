from flask import Blueprint, request, jsonify, abort
from api import celery
from ..tasks import delete_data_task

delete_bp = Blueprint('delete', __name__)

@delete_bp.route('/api/delete/<string:delete_type>/<string:id>', methods=['DELETE'])
def delete_data(delete_type, id):
    if delete_type not in ['vn', 'character', 'tag', 'producer', 'staff', 'trait']:
        abort(400, description="Invalid delete type")
    
    task = delete_data_task.delay(delete_type, id)
    return jsonify({"task_id": task.id}), 202

@delete_bp.route('/api/delete/status/<task_id>')
def get_delete_status(task_id):
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

@delete_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@delete_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@delete_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500