from flask import Blueprint, jsonify, abort, request

savedata_bp = Blueprint('savedata', __name__, url_prefix='/savedatas')

@savedata_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@savedata_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@savedata_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500

from api import cache
from api.tasks import get_savedata_task
from api.tasks import get_savedatas_task
from api.tasks import upload_savedatas_task
from api.tasks import delete_savedata_task
from api.tasks import delete_savedatas_task
from api.utils.check import is_valid_id

@savedata_bp.route('', methods=['GET'])
@cache.cached(timeout=60)
def list_savedata():
    vn_id = request.args.get('vn_id')
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)

    if not is_valid_id(vn_id, 'v'):
        abort(400, description="Invalid VN ID")
    if limit > 100:
        abort(400, description="Limit cannot exceed 100")

    task = get_savedatas_task.delay(vn_id, page, limit)
    return jsonify({"task_id": task.id}), 202

@savedata_bp.route('/<string:id>', methods=['GET'])
@cache.cached(timeout=60)
def get_savedata(id):
    if not is_valid_id(id, 's'):
        abort(400, description="Invalid savedata ID")

    task = get_savedata_task.delay(id)
    return jsonify({"task_id": task.id}), 202

@savedata_bp.route('', methods=['POST'])
def upload_savedata():
    vn_id = request.args.get('vn_id')

    if not is_valid_id(vn_id, 'v'):
        abort(400, description="Invalid VN ID")

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

    task = upload_savedatas_task.delay(vn_id, serializable_files)
    return jsonify({"task_id": task.id}), 202

@savedata_bp.route('/<string:id>', methods=['DELETE'])
def delete_savedata(id):
    if not is_valid_id(id, 's'):
        abort(400, description="Invalid savedata ID")

    task = delete_savedata_task.delay(id)
    return jsonify({"task_id": task.id}), 202

@savedata_bp.route('', methods=['DELETE'])
def delete_all_savedata():
    vn_id = request.args.get('vn_id')

    if not is_valid_id(vn_id, 'v'):
        abort(400, description="Invalid VN ID")

    task = delete_savedatas_task.delay(vn_id)
    return jsonify({"task_id": task.id}), 202

@savedata_bp.route('/download/<string:id>', methods=['GET'])
def download_savedata(id):
    if is_valid_id(id, 's'):
        task = get_savedata_task.delay(id)
        return jsonify({"task_id": task.id}), 202
    elif is_valid_id(id, 'v'):
        task = get_savedatas_task.delay(id)
        return jsonify({"task_id": task.id}), 202
    else:
        abort(400, description="Invalid ID")