from flask import Blueprint, jsonify, request

from api.tasks.resource import get_resources_task
from api.tasks.resource import search_resource_task 
from api.tasks.resource import search_resources_task 
from api.tasks.resource import update_resources_task 
from api.tasks.resource import delete_resources_task 

producers_bp = Blueprint('producers', __name__, url_prefix='/producers')

@producers_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@producers_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@producers_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500

@producers_bp.route('', methods=['GET'])
def get_producers():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)
    sort = request.args.get('sort', default='id', type=str)
    order = request.args.get('order', default='asc', type=str)
    
    task = get_resources_task.delay('producer', None, page, limit, sort, order)
    return jsonify({"task_id": task.id}), 202

@producers_bp.route('/<string:id>', methods=['GET'])
def get_producer(id):
    task = get_resources_task.delay('producer', id)
    return jsonify({"task_id": task.id}), 202

@producers_bp.route('', methods=['POST'])
def search_producers():
    search_params = request.json
    search_from = search_params.pop('search_from', 'local')
    response_size = search_params.pop('response_size', 'small')
    page = search_params.pop('page', 1)
    limit = search_params.pop('limit', 20)
    sort = search_params.pop('sort', 'id')
    order = search_params.pop('order', 'asc')
    
    task = search_resources_task.delay('producer', search_from, search_params, response_size, page, limit, sort, order)
    return jsonify({"task_id": task.id}), 202

@producers_bp.route('/<string:id>', methods=['POST'])
def search_producer_by_id(id):
    task = search_resource_task.delay('producer', id)
    return jsonify({"task_id": task.id}), 202

@producers_bp.route('', methods=['PUT'])
def update_producers():
    task = update_resources_task.delay('producer')
    return jsonify({"task_id": task.id}), 202

@producers_bp.route('/<string:id>', methods=['PUT'])
def update_producer(id):
    task = update_resources_task.delay('producer', id)
    return jsonify({"task_id": task.id}), 202

@producers_bp.route('', methods=['DELETE'])
def delete_producers():
    task = delete_resources_task.delay('producer')
    return jsonify({"task_id": task.id}), 202

@producers_bp.route('/<string:id>', methods=['DELETE'])
def delete_producer(id):
    task = delete_resources_task.delay('producer', id)
    return jsonify({"task_id": task.id}), 202