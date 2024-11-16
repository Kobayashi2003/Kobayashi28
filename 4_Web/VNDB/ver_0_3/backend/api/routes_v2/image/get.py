from typing import Dict

from flask import jsonify, abort
from . import image_bp
from api import cache
from api.tasks import get_image_task
from api.tasks import get_images_task
from api.utils.check import is_valid_image_id, is_valid_id, infer_type_from_id 

@image_bp.route('/get/<string:get_type>/<string:id>', methods=['GET'])
@cache.cached(timeout=60)
def get_image(get_type: str, id: str) -> Dict[str, str]:
    if get_type not in ['vn', 'character']:
        abort(400, description="Invalid get type")
    if not is_valid_image_id(id, get_type):
        abort(400, description="Invalid ID")

    task = get_image_task.delay(get_type, id)
    return jsonify({"task_id": task.id}), 202

@image_bp.route('/get/batch/<string:get_type>/<string:id>', methods=['GET'])
@cache.cached(timeout=60)
def get_images(get_type: str, id: str) -> Dict[str, str]:
    if get_type not in ['vn', 'character']:
        abort(400, description="Invalid get type")
    if not is_valid_id(id, valid_letters=['v', 'c']):
        abort(400, description="Invalid ID")
    if not infer_type_from_id(id) == get_type:
        abort(400, description="Invalid ID")

    task = get_images_task.delay(get_type, id)
    return jsonify({"task_id": task.id}), 202