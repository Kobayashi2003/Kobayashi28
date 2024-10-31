from flask import Blueprint, request, jsonify, abort
from api.celery_app import celery
from api.tasks import delete_task
from api.utils.logger import db_logger

delete_bp = Blueprint('delete', __name__)

@delete_bp.route('/api/delete', methods=['POST'])
def delete():
    vn_id = request.json.get('id')
    
    if not vn_id:
        abort(400, description="Missing VN ID")
    
    task = delete_task.delay(vn_id)
    
    return jsonify({"task_id": task.id}), 202

@delete_bp.route('/api/delete/status/<task_id>', methods=['GET'])
def delete_status(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Delete operation is pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': 'Delete operation is in progress...'
        }
        if task.info:
            response['result'] = task.info
    else:
        response = {
            'state': task.state,
            'status': 'Delete operation failed',
            'error': str(task.info)
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