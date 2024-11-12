from flask import Blueprint, request, jsonify, abort
from api import celery
from ..tasks import cleanup_task

cleanup_bp = Blueprint('cleanup', __name__)

@cleanup_bp.route('/api/cleanup', methods=['POST'])
def cleanup_database():
    data = request.json
    type = data.get('type')
    
    if type and type not in ['vn', 'tag', 'producer', 'staff', 'character', 'trait']:
        return jsonify({"error": "Invalid type specified"}), 400

    task = cleanup_task.delay(type)
    return jsonify({"task_id": task.id}), 202

@cleanup_bp.route('/api/cleanup/status/<task_id>')
def get_cleanup_status(task_id):
    task = celery.AsyncResult(task_id)
    return jsonify({
        'state': task.state,
        'status': task.info.get('status', 'Task is in progress...') if task.state != 'FAILURE' else 'Task failed',
        'result': task.result if task.state == 'SUCCESS' else None,
        'error': str(task.result) if task.state == 'FAILURE' else None
    })

@cleanup_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@cleanup_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@cleanup_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500