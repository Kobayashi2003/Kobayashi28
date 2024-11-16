from datetime import datetime, timezone

from flask import request, jsonify, abort
from werkzeug.utils import secure_filename

from . import savedata_bp
from api.tasks import upload_savedatas_task
from api.utils.check import infer_type_from_id

@savedata_bp.route('/upload/<string:vnid>', methods=['POST'])
def upload_savedatas(vnid: str):
    if not infer_type_from_id(vnid) == 'vn':
        abort(400, description="Invalid ID")
    if 'files[]' not in request.files:
        abort(400, description="No file part")
    
    files = request.files.getlist('files[]')

    if not files or all(file.filename == '' for file in files):
        abort(400, description="No selected file")

    # Convert FileStorage objects to a format that can be serialized
    to_datetime = lambda ts: datetime.fromtimestamp(int(ts) / 1000.0, tz=timezone.utc) if ts else datetime.now(timezone.utc)

    serializable_files = [
        {
            # 'filename': secure_filename(file.filename),
            'filename': file.filename,
            'content': file.read(),
            'last_modified': to_datetime(request.form.get(f'last_modified_{file.filename}'))
        } for file in files
    ]

    task = upload_savedatas_task.delay(vnid, serializable_files)
    return jsonify({"task_id": task.id}), 202