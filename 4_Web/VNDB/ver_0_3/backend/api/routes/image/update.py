from typing import Dict

from flask import jsonify, abort
from . import image_bp
from api.tasks import update_images_task

@image_bp.route('/update/<string:update_type>/<string:id>', methods=['POST'])
def update_images(update_type: str, id: str) -> Dict[str, str]:
    if update_type not in ['vn', 'character']:
        abort(400, description="Invalid update type")

    task = update_images_task.delay(update_type, id)
    return jsonify({"task_id": task.id}), 202