from typing import Dict

from flask import jsonify, abort
from . import image_bp
from api.tasks import delete_image_task
from api.tasks import delete_images_task 
from api.utils.check import is_valid_image_id, is_valid_id, infer_type_from_id

@image_bp.route('/delete/<string:delete_type>/<string:id>', methods=['DELETE'])
def delete_image(delete_type: str, id: str) -> Dict[str, str]:
    if delete_type not in ['vn', 'character']:
        abort(400, description="Invalid delete type")
    if not is_valid_image_id(id, delete_type):
        abort(400, description="Invalid ID")

    task = delete_image_task.delay(delete_type, id)
    return jsonify({"task_id": task.id}), 202

@image_bp.route('/delete/batch/<string:delete_type>/<string:id>', methods=['DELETE'])
def delete_images(delete_type: str, id: str) -> Dict[str, str]:
    if delete_type not in ['vn', 'character']:
        abort(400, description="Invalid delete type")
    if not is_valid_id(id, valid_letters=['v', 'c']):
        abort(400, description="Invalid ID")
    if not infer_type_from_id(id) == delete_type:
        abort(400, description="Invalid ID") 

    task = delete_images_task.delay(delete_type, id)
    return jsonify({"task_id": task.id}), 202