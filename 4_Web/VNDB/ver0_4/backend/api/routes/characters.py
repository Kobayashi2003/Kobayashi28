from flask import Blueprint, jsonify, request

from api.tasks.resource import get_resources_task
from api.tasks.resource import search_resource_task 
from api.tasks.resource import search_resources_task 
from api.tasks.resource import update_resources_task 
from api.tasks.resource import delete_resources_task 

from api.tasks.image import get_images_task
from api.tasks.image import upload_images_task
from api.tasks.image import update_images_task
from api.tasks.image import delete_images_task

characters_bp = Blueprint('characters', __name__, url_prefix='/characters')

@characters_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@characters_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@characters_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500

@characters_bp.route('', methods=['GET'])
def get_characters():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)
    sort = request.args.get('sort', default='id', type=str)
    order = request.args.get('order', default='asc', type=str)
    
    task = get_resources_task.delay('character', None, page, limit, sort, order)
    return jsonify({"task_id": task.id}), 202

@characters_bp.route('/<string:id>', methods=['GET'])
def get_character(id):
    task = get_resources_task.delay('character', id)
    return jsonify({"task_id": task.id}), 202

@characters_bp.route('', methods=['POST'])
def search_characters():
    search_params = request.json
    search_from = search_params.pop('search_from', 'local')
    response_size = search_params.pop('response_size', 'small')
    page = search_params.pop('page', 1)
    limit = search_params.pop('limit', 20)
    sort = search_params.pop('sort', 'id')
    order = search_params.pop('order', 'asc')
    
    task = search_resources_task.delay('character', search_from, search_params, response_size, page, limit, sort, order)
    return jsonify({"task_id": task.id}), 202

@characters_bp.route('/<string:id>', methods=['POST'])
def search_character_by_id(id):
    task = search_resource_task.delay('character', id)
    return jsonify({"task_id": task.id}), 202

@characters_bp.route('', methods=['PUT'])
def update_characters():
    task = update_resources_task.delay('character')
    return jsonify({"task_id": task.id}), 202

@characters_bp.route('/<string:id>', methods=['PUT'])
def update_character(id):
    task = update_resources_task.delay('character', id)
    return jsonify({"task_id": task.id}), 202

@characters_bp.route('', methods=['DELETE'])
def delete_characters():
    task = delete_resources_task.delay('character')
    return jsonify({"task_id": task.id}), 202

@characters_bp.route('/<string:id>', methods=['DELETE'])
def delete_character(id):
    task = delete_resources_task.delay('character', id)
    return jsonify({"task_id": task.id}), 202

# Image-related routes
@characters_bp.route('/<string:charid>/images', methods=['GET'])
def get_character_images(charid):
    task = get_images_task.delay('character', charid)
    return jsonify({"task_id": task.id}), 202

@characters_bp.route('/<string:charid>/images/<string:id>', methods=['GET'])
def get_character_image(charid, id):
    task = get_images_task.delay('character', charid, id)
    return jsonify({"task_id": task.id}), 202

@characters_bp.route('/<string:charid>/images', methods=['POST'])
def upload_character_images(charid):
    if 'files' not in request.files:
        return jsonify({"error": "No file part"}), 400
    files = request.files.getlist('files')
    file_data = [{'filename': file.filename, 'content': file.read()} for file in files]
    task = upload_images_task.delay('character', charid, file_data)
    return jsonify({"task_id": task.id}), 202

@characters_bp.route('/<string:charid>/images', methods=['PUT'])
def update_character_images(charid):
    task = update_images_task.delay('character', charid)
    return jsonify({"task_id": task.id}), 202

@characters_bp.route('/<string:charid>/images/<string:id>', methods=['PUT'])
def update_character_image(charid, id):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    file_data = {'filename': file.filename, 'content': file.read()}
    task = update_images_task.delay('character', charid, id, file_data)
    return jsonify({"task_id": task.id}), 202

@characters_bp.route('/<string:charid>/images', methods=['DELETE'])
def delete_character_images(charid):
    task = delete_images_task.delay('character', charid)
    return jsonify({"task_id": task.id}), 202

@characters_bp.route('/<string:charid>/images/<string:id>', methods=['DELETE'])
def delete_character_image(charid, id):
    task = delete_images_task.delay('character', charid, id)
    return jsonify({"task_id": task.id}), 202