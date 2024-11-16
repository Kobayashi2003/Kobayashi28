from typing import Dict

from flask import jsonify, abort
from . import image_bp
from api.tasks import download_images_task
from api.utils.check import is_valid_id, infer_type_from_id

@image_bp.route('/download/<string:download_type>/<string:id>', methods=['POST'])
def download_images(download_type: str, id: str) -> Dict[str, str]:
    if download_type not in ['vn', 'character']:
        abort(400, description="Invalid download type")
    if not is_valid_id(id, valid_letters=['v', 'c']):
        abort(400, description="Invalid ID")
    if not infer_type_from_id(id) == download_type:
        abort(400, description="Invalid ID")

    task = download_images_task.delay(download_type, id)
    return jsonify({"task_id": task.id}), 202