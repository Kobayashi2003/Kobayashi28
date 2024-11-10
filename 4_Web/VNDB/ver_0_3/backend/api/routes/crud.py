from flask import Blueprint, request, jsonify, abort
from api.celery_app import celery
from api.tasks import crud_task

crud_bp = Blueprint('crud', __name__)

@crud_bp.route('/api/create', methods=['POST'])
def create_operation():
    return handle_crud_operation('create')

@crud_bp.route('/api/read', methods=['GET'])
def read_operation():
    return handle_crud_operation('read')

@crud_bp.route('/api/update', methods=['PUT'])
def update_operation():
    return handle_crud_operation('update')

@crud_bp.route('/api/delete', methods=['DELETE'])
def delete_operation():
    return handle_crud_operation('delete')

def handle_crud_operation(operation):
    params = request.json if request.is_json else request.args.to_dict()
    model_type = params.get('modelType')
    id = params.get('id')
    data = params.get('data', {})

    if model_type not in ['vn', 'character', 'tag', 'producer', 'staff', 'trait']:
        abort(400, description="Invalid model type")

    task = crud_task.delay(
        operation=operation,
        model_type=model_type,
        id=id,
        data=data
    )

    return jsonify({"task_id": task.id}), 202

@crud_bp.route('/api/crud/status/<task_id>', methods=['GET'])
def crud_status(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'CRUD operation is pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': 'CRUD operation is in progress...'
        }
        if task.info:
            response['result'] = task.info
    else:
        response = {
            'state': task.state,
            'status': 'CRUD operation failed',
            'error': str(task.info)
        }
    return jsonify(response)

@crud_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@crud_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@crud_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500