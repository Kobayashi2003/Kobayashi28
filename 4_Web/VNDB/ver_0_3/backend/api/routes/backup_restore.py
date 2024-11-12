from flask import Blueprint, request, jsonify, abort
from api import celery
from ..tasks import backup_task, restore_task

backup_restore_bp = Blueprint('backup_restore', __name__)

@backup_restore_bp.route('/api/backup', methods=['POST'])
def backup_database():
    data = request.json
    filename = data.get('filename')
    
    task = backup_task.delay(filename)
    return jsonify({"task_id": task.id}), 202

@backup_restore_bp.route('/api/restore', methods=['POST'])
def restore_database():
    data = request.json
    filename = data.get('filename')
    
    if not filename:
        return jsonify({"error": "Filename is required"}), 400

    task = restore_task.delay(filename)
    return jsonify({"task_id": task.id}), 202

@backup_restore_bp.route('/api/backup/status/<task_id>')
@backup_restore_bp.route('/api/restore/status/<task_id>')
def get_task_status(task_id):
    task = celery.AsyncResult(task_id)
    return jsonify({
        'state': task.state,
        'status': task.info.get('status', 'Task is in progress...') if task.state != 'FAILURE' else 'Task failed',
        'result': task.result if task.state == 'SUCCESS' else None,
        'error': str(task.result) if task.state == 'FAILURE' else None
    })

@backup_restore_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@backup_restore_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@backup_restore_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500