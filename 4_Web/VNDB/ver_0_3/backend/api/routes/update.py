from flask import Blueprint, request, jsonify, abort
from api import celery
from ..tasks import update_data_task

update_bp = Blueprint('update_db', __name__)

@update_bp.route('/api/update/<string:update_type>/<string:id>', methods=['POST'])
def update_data(update_type, id):
    if update_type not in ['vn', 'character', 'tag', 'producer', 'staff', 'trait']:
        abort(400, description="Invalid update type")
    
    task = update_data_task.delay(update_type, id)
    return jsonify({"task_id": task.id}), 202

@update_bp.route('/api/update/status/<task_id>')
def get_update_status(task_id):
    task = celery.AsyncResult(task_id)
    return jsonify({
        'state': task.state,
        'status': task.info.get('status', 'Task is in progress...') if task.state != 'FAILURE' else 'Task failed',
        'result': task.result if task.state == 'SUCCESS' else None,
        'error': str(task.result) if task.state == 'FAILURE' else None
    })

@update_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@update_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@update_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500