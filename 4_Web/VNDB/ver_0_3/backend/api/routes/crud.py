from flask import Blueprint, request, jsonify, abort
from api import celery
from ..tasks import crud_task

crud_bp = Blueprint('crud', __name__)

@crud_bp.route('/api/crud/<string:operation>', methods=['POST'])
def handle_crud_operation(operation):
    if operation not in ['create', 'read', 'update', 'delete']:
        abort(400, description="Invalid operation")

    params = request.json if request.is_json else request.args.to_dict()
    model_type = params.get('modelType')
    id = params.get('id')
    data = params.get('data', {})

    if model_type not in ['vn', 'character', 'tag', 'producer', 'staff', 'trait']:
        abort(400, description="Invalid model type")

    task = crud_task.delay(operation=operation, model_type=model_type, id=id, data=data)
    return jsonify({"task_id": task.id}), 202

@crud_bp.route('/api/crud/status/<task_id>', methods=['GET'])
def crud_status(task_id):
    task = celery.AsyncResult(task_id)
    return jsonify({
        'state': task.state,
        'status': task.info.get('status', 'Task is in progress...') if task.state != 'FAILURE' else 'Task failed',
        'result': task.result if task.state == 'SUCCESS' else None,
        'error': str(task.result) if task.state == 'FAILURE' else None
    })

@crud_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@crud_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@crud_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500