from typing import Dict

from flask import jsonify, abort
from . import image_bp
from api.tasks import delete_image_task
from api.tasks import delete_images_task 

@image_bp.route('/delete-image/<string:delete_type>/<string:id>', methods=['DELETE'])
def delete_image(delete_type: str, id: str) -> Dict[str, str]:
    if delete_type not in ['vn', 'character']:
        abort(400, description="Invalid delete type")

    task = delete_image_task.delay(delete_type, id)
    return jsonify({"task_id": task.id}), 202

@image_bp.route('/delete-images/<string:delete_type>/<string:id>', methods=['DELETE'])
def delete_images(delete_type: str, id: str) -> Dict[str, str]:
    if delete_type not in ['vn', 'character']:
        abort(400, description="Invalid delete type")

    task = delete_images_task.delay(delete_type, id)
    return jsonify({"task_id": task.id}), 202