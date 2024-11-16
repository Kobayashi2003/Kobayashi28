from typing import Dict

from flask import request, jsonify, abort
from . import image_bp
from api.tasks import upload_images_task
from api.utils.check import is_valid_id, infer_type_from_id

@image_bp.route('/upload/<string:upload_type>/<string:id>', methods=['POST'])
def upload_images(upload_type: str, id: str) -> Dict[str, str]:
    if upload_type not in ['vn', 'character']:
        abort(400, description="Invalid upload type")
    if not is_valid_id(id, valid_letters=['v', 'c']):
        abort(400, description="Invalid ID")
    if not infer_type_from_id(id) == upload_type:
        abort(400, description="Invalid ID")

    if 'files[]' not in request.files:
        abort(400, description="No file part")
    
    files = request.files.getlist('files[]')

    if not files or all(file.filename == '' for file in files):
        abort(400, description="No selected file")

    # Convert FileStorage objects to a format that can be serialized
    serializable_files = [
        {
            'filename': file.filename,
            'content': file.read(),
            'content_type': file.content_type
        } for file in files
    ]

    task = upload_images_task.delay(upload_type, id, serializable_files)
    return jsonify({"task_id": task.id}), 202
 