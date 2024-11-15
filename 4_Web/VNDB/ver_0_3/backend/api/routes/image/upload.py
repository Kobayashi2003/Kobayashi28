from typing import Dict

from flask import request, jsonify, abort
from . import image_bp
from api.tasks import upload_images_task

@image_bp.route('/upload/<string:upload_type>/<string:id>', methods=['POST'])
def upload_images(upload_type: str, id: str) -> Dict[str, str]:
    if upload_type not in ['vn', 'character']:
        abort(400, description="Invalid upload type")

    if 'files[]' not in request.files.getlist('files[]'):
        abort(400, description="No file part")
    
    files = request.files.getlist('files[]')

    if not files or files[0].filename == '':
        abort(400, description="No selected file")

    task = upload_images_task.delay(upload_type, id, files)
    return jsonify({"task_id": task.id}), 202
    
    


