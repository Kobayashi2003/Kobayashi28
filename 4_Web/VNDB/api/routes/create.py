from flask import Blueprint, request, jsonify, abort
from api.celery_app import celery
from api.tasks import create_task
from api.utils.logger import db_logger

create_bp = Blueprint('create', __name__)

@create_bp.route('/api/create', methods=['POST'])
def create():
    vn_data = request.json
    
    if not vn_data or 'id' not in vn_data:
        abort(400, description="Invalid VN data")
    
    task = create_task.delay(vn_data)
    
    return jsonify({"task_id": task.id}), 202

@create_bp.route('/api/create/status/<task_id>', methods=['GET'])
def create_status(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Create operation is pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': 'Create operation is in progress...'
        }
        if task.info:
            response['result'] = task.info
    else:
        response = {
            'state': task.state,
            'status': 'Create operation failed',
            'error': str(task.info)
        }
    return jsonify(response)

@create_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@create_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@create_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500