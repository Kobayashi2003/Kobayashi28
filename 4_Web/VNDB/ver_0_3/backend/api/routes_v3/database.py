from typing import Optional, Dict

from flask import Blueprint, jsonify, abort, request

database_bp = Blueprint('database', __name__, url_prefix='/database')

@database_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@database_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@database_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500

from api.tasks import read_data_task
from api.tasks import create_data_task
from api.tasks import update_data_task
from api.tasks import delete_data_task
from api.tasks import backup_task
from api.tasks import restore_task
from api.tasks import cleanup_task
from api.utils import infer_type_from_id 

@database_bp.route('/<string:resource>', methods=['GET'])
@database_bp.route('/<string:resource>/<string:id>', methods=['GET'])
def read_data(resource: str, id: Optional[str]) -> Dict[str, str]:
    valid_resources = ['vns', 'characters', 'tags', 'producers', 'staff', 'traits']
    if resource not in valid_resources:
        abort(400, description=f"Invalid resource type. Must be one of: {', '.join(valid_resources)}")
    
    read_type = resource[:-1] if resource.endswith('s') else resource
    
    if id and not infer_type_from_id(id) == read_type:
        abort(400, description="Invalid ID")
    
    if not id:
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=20, type=int)
        sort = request.args.get('sort', default=None, type=str)
        order = request.args.get('order', default='asc', type=str)

        if page < 1:
            abort(400, description="Page must be a positive integer")
        if limit < 1 or limit > 100:
            abort(400, description="Limit must be between 1 and 100")
        if order not in ['asc', 'desc']:
            abort(400, description="Order must be either 'asc' or 'desc'")

        task = read_data_task.delay(read_type, page=page, limit=limit, sort=sort, order=order)
    else:
        task = read_data_task.delay(read_type, id)

    return jsonify({"task_id": task.id}), 202

@database_bp.route('/<string:resource>', methods=['POST'])
def create_data(resource: str) -> Dict[str, str]:
    valid_resources = ['vns', 'characters', 'tags', 'producers', 'staff', 'traits']
    if resource not in valid_resources:
        abort(400, description=f"Invalid resource type. Must be one of: {', '.join(valid_resources)}")
    
    create_type = resource[:-1] if resource.endswith('s') else resource

    data = request.json if request.is_json else request.form.to_dict()
    
    if not data:
        abort(400, description="No data provided")

    id = data.pop('id')
    if not infer_type_from_id(id) == create_type:
        abort(400, description=f"Invalid ID format for resource type: {create_type}")

    task = create_data_task.delay(create_type, id, data)
    return jsonify({"task_id": task.id}), 202

@database_bp.route('/<string:resource>/<string:id>', methods=['PUT'])
def update_data(resource: str, id: str) -> Dict[str, str]:
    valid_resources = ['vns', 'characters', 'tags', 'producers', 'staff', 'traits']
    if resource not in valid_resources:
        abort(400, description=f"Invalid resource type. Must be one of: {', '.join(valid_resources)}")
    
    update_type = resource[:-1] if resource.endswith('s') else resource
    
    if not infer_type_from_id(id) == update_type:
        abort(400, description="Invalid ID")
    
    task = update_data_task.delay(update_type, id)
    return jsonify({"task_id": task.id}), 202

@database_bp.route('/<string:resource>/<string:id>', methods=['DELETE'])
def delete_data(resource: str, id: str) -> Dict[str, str]:
    valid_resources = ['vns', 'characters', 'tags', 'producers', 'staff', 'traits']
    if resource not in valid_resources:
        abort(400, description=f"Invalid resource type. Must be one of: {', '.join(valid_resources)}")
    
    delete_type = resource[:-1] if resource.endswith('s') else resource
    
    if not infer_type_from_id(id) == delete_type:
        abort(400, description="Invalid ID")
    
    task = delete_data_task.delay(delete_type, id)
    return jsonify({"task_id": task.id}), 202

@database_bp.route('/backup', methods=['POST'])
def backup_database() -> Dict[str, str]:
    filename = request.args.get('filename')

    if not filename:
        data = request.json if request.is_json else request.form.to_dict()
        filename = data.get('filename')

    task = backup_task.delay(filename)
    return jsonify({"task_id": task.id}), 202

@database_bp.route('/restore', methods=['POST'])
def restore_database() -> Dict[str, str]:
    filename = request.args.get('filename')

    if not filename:
        data = request.json if request.is_json else request.form.to_dict()
        if not data or 'filename' not in data:
            abort(400, description="Filename must be provided")
        filename = data['filename']

    task = restore_task.delay(filename)
    return jsonify({"task_id": task.id}), 202

@database_bp.route('/cleanup', methods=['POST'])
def cleanup_database() -> Dict[str, str]:
    cleanup_type = request.args.get('type', default='all', type=str)
    valid_types = ['vn', 'tag', 'producer', 'staff', 'character', 'trait', 'all']

    if cleanup_type not in valid_types:
        abort(400, description=f"Invalid cleanup type. Must be one of: {', '.join(valid_types)}")
    
    task = cleanup_task.delay(cleanup_type)
    return jsonify({"task_id": task.id}), 202