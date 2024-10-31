from flask import Blueprint, request, jsonify, abort
from api.celery_app import celery
from api.tasks import update_task
from api.utils.logger import db_logger

update_bp = Blueprint('update', __name__)

@update_bp.route('/api/update', methods=['POST'])
def update():
    vn_id = request.json.get('id')
    vn_data = request.json.get('data')
    downloaded = request.json.get('downloaded')
    
    if not vn_id:
        abort(400, description="Missing VN ID")
    
    if vn_data is None and downloaded is None:
        abort(400, description="No update data provided")
    
    task = update_task.delay(vn_id, vn_data, downloaded)
    
    return jsonify({"task_id": task.id}), 202

@update_bp.route('/api/update/status/<task_id>', methods=['GET'])
def update_status(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Update operation is pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': 'Update operation is in progress...'
        }
        if task.info:
            response['result'] = task.info
    else:
        response = {
            'state': task.state,
            'status': 'Update operation failed',
            'error': str(task.info)
        }
    return jsonify(response)

@update_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@update_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@update_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500