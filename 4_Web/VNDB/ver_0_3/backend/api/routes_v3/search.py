from typing import Dict

from flask import Blueprint, jsonify, abort, request

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@search_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@search_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500

from api import cache
from api.tasks import search_task
from api.tasks import get_data_task
from api.utils.check import infer_type_from_id

@search_bp.route('', methods=['GET'])
@cache.memoize(timeout=60)
def search() -> Dict[str, str]:
    search_type = request.args.get('type')
    if search_type not in ['vn', 'character', 'tag', 'producer', 'staff', 'trait']:
        abort(400, description="Invalid search type")

    query = request.args.get('query')
    fields = request.args.get('fields')
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)
    sort = request.args.get('sort', default='id')
    order = request.args.get('order', default='asc')

    if limit > 100:
        abort(400, description="Limit cannot exceed 100")

    if order not in ['asc', 'desc']:
        abort(400, description="Order must be either 'asc' or 'desc'")

    params = {
        'query': query,
        'fields': fields
    }

    task = search_task.delay(search_from='local', search_type=search_type, 
                             response_size='small', params=params,
                             page=page, limit=limit, sort=sort, order=order)
    return jsonify({"task_id": task.id}), 202
    
@search_bp.route('/<string:resource>/<string:id>', methods=['GET'])
@cache.memoize(timeout=60)
def get_data(resource: str, id: str):
    valid_resources = ['vns', 'characters', 'tags', 'producers', 'staff', 'traits']
    if resource not in valid_resources:
        abort(400, description=f"Invalid resource type. Must be one of: {', '.join(valid_resources)}")
    
    # Convert plural resource name to singular for internal processing
    data_type = resource[:-1] if resource.endswith('s') else resource

    # Validate ID format
    if not infer_type_from_id(id) == data_type:
        abort(400, description="Invalid ID format for the given resource type")

    # Get data size from query parameters, default to 'small'
    data_size = request.args.get('size', default='small')
    if data_size not in ['small', 'large']:
        abort(400, description="Invalid data size. Must be 'small' or 'large'")

    # Start the asynchronous task
    task = get_data_task.delay(data_type, id, data_size)

    # Return the task ID
    return jsonify({"task_id": task.id}), 202