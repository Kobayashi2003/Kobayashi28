from flask import Blueprint, jsonify, abort, request

image_bp = Blueprint('image', __name__, url_prefix='/images')

@image_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@image_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@image_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500

from api import cache
from api.tasks import get_image_task
from api.tasks import get_images_task
from api.tasks import upload_images_task
from api.tasks import download_images_task
from api.tasks import update_images_task
from api.tasks import delete_image_task
from api.tasks import delete_images_task
from api.utils.check import is_valid_id, infer_type_from_id, is_valid_image_id

@image_bp.route('', methods=['GET'])
@cache.cached(timeout=60)
def list_images():
    image_type = request.args.get('type')
    id = request.args.get('id')

    if image_type not in ['vn', 'character']:
        abort(400, description="Invalid image type")
    if not is_valid_id(id, valid_letters=['v', 'c']):
        abort(400, description="Invalid ID")
    if not infer_type_from_id(id) == image_type:
        abort(400, description="Invalid ID for the given type")

    task = get_images_task.delay(image_type, id)
    return jsonify({"task_id": task.id}), 202

@image_bp.route('/<string:id>', methods=['GET'])
@cache.cached(timeout=60)
def get_image(id: str):
    if not is_valid_image_id(id, 'vn') and not is_valid_image_id(id, 'character'):
        abort(400, description="Invalid image ID")

    task = get_image_task.delay(id)
    return jsonify({"task_id": task.id}), 202

@image_bp.route('', methods=['POST'])
def upload_images():
    image_type = request.args.get('type')
    id = request.args.get('id')

    if image_type not in ['vn', 'character']:
        abort(400, description="Invalid image type")
    if not is_valid_id(id, valid_letters=['v', 'c']):
        abort(400, description="Invalid ID")
    if not infer_type_from_id(id) == image_type:
        abort(400, description="Invalid ID for the given type")

    if 'files[]' not in request.files:
        abort(400, description="No file part")
    
    files = request.files.getlist('files[]')

    if not files or all(file.filename == '' for file in files):
        abort(400, description="No selected file")

    serializable_files = [
        {
            'filename': file.filename,
            'content': file.read(),
            'content_type': file.content_type
        } for file in files
    ]

    task = upload_images_task.delay(image_type, id, serializable_files)
    return jsonify({"task_id": task.id}), 202

@image_bp.route('', methods=['PUT'])
def update_images():
    update_type = request.args.get('type')
    id = request.args.get('id')

    if update_type not in ['vn', 'character']:
        abort(400, description="Invalid update type")
    if not is_valid_id(id, valid_letters=['v', 'c']):
        abort(400, description="Invalid ID")
    if not infer_type_from_id(id) == update_type:
        abort(400, description="Invalid ID for the given type")

    task = update_images_task.delay(update_type, id)
    return jsonify({"task_id": task.id}), 202

@image_bp.route('/<string:id>', methods=['DELETE'])
def delete_image(id: str):
    if not is_valid_image_id(id, 'vn') and not is_valid_image_id(id, 'character'):
        abort(400, description="Invalid image ID")

    task = delete_image_task.delay(id)
    return jsonify({"task_id": task.id}), 202

@image_bp.route('', methods=['DELETE'])
def delete_all_images():
    image_type = request.args.get('type')
    id = request.args.get('id')

    if image_type not in ['vn', 'character']:
        abort(400, description="Invalid image type")
    if not is_valid_id(id, valid_letters=['v', 'c']):
        abort(400, description="Invalid ID")
    if not infer_type_from_id(id) == image_type:
        abort(400, description="Invalid ID for the given type")

    task = delete_images_task.delay(image_type, id)
    return jsonify({"task_id": task.id}), 202