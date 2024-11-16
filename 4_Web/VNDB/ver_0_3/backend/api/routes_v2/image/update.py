from typing import Dict

from flask import jsonify, abort
from . import image_bp
from api.tasks import update_images_task
from api.utils.check import is_valid_id, infer_type_from_id

@image_bp.route('/update/<string:update_type>/<string:id>', methods=['POST'])
def update_images(update_type: str, id: str) -> Dict[str, str]:
    if update_type not in ['vn', 'character']:
        abort(400, description="Invalid update type")
    if not is_valid_id(id, valid_letters=['v', 'c']):
        abort(400, description="Invalid ID")
    if not infer_type_from_id(id) == update_type:
        abort(400, description="Invalid ID")

    task = update_images_task.delay(update_type, id)
    return jsonify({"task_id": task.id}), 202