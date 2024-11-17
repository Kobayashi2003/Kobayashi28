from flask import Blueprint, jsonify, request, abort, send_file

from api.database import get_image_path, get_savedata_path, get

from api.tasks.resource import get_resources_task
from api.tasks.resource import search_resource_task 
from api.tasks.resource import search_resources_task 
from api.tasks.resource import update_resources_task 
from api.tasks.resource import delete_resources_task 
from api.tasks.resource import delete_vns_task

from api.tasks.image import get_images_task
from api.tasks.image import upload_images_task
from api.tasks.image import update_images_task
from api.tasks.image import delete_images_task

from api.tasks.savedata import get_savedatas_task
from api.tasks.savedata import upload_savedatas_task
from api.tasks.savedata import delete_savedatas_task

vns_bp = Blueprint('vns', __name__, url_prefix='/vns')

@vns_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@vns_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@vns_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500


@vns_bp.route('', methods=['GET'])
def get_vns():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=20, type=int)
    sort = request.args.get('sort', default='id', type=str)
    order = request.args.get('order', default='asc', type=str)
    
    task = get_resources_task.delay('vn', None, page, limit, sort, order)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:id>', methods=['GET'])
def get_vn(id):
    task = get_resources_task.delay('vn', id)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('', methods=['POST'])
def search_vns():
    search_params = request.json
    search_from = search_params.pop('search_from', 'local')
    response_size = search_params.pop('response_size', 'small')
    page = search_params.pop('page', 1)
    limit = search_params.pop('limit', 20)
    sort = search_params.pop('sort', 'id')
    order = search_params.pop('order', 'asc')
    
    task = search_resources_task.delay('vn', search_from, search_params, response_size, page, limit, sort, order)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:id>', methods=['POST'])
def search_vn_by_id(id):
    task = search_resource_task.delay('vn', id)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('', methods=['PUT'])
def update_vns():
    task = update_resources_task.delay('vn')
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:id>', methods=['PUT'])
def update_vn(id):
    task = update_resources_task.delay('vn', id)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('', methods=['DELETE'])
def delete_vns():
    task = delete_vns_task.delay()
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:id>', methods=['DELETE'])
def delete_vn(id):
    task = delete_vns_task.delay(id)
    return jsonify({"task_id": task.id}), 202


@vns_bp.route('/<string:vnid>/images', methods=['GET'])
def get_vn_images(vnid):
    task = get_images_task.delay('vn', vnid)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:vnid>/images/<string:id>', methods=['GET'])
def get_vn_image(vnid, id):
    format = request.args.get('format', 'file')
    if format == 'file':
        image_path = get_image_path('vn', vnid, id)
        if not image_path:
            abort(400, 'Invaild image URL')
        return send_file(image_path, mimetype='image/jpeg')
    task = get_images_task.delay('vn', vnid, id)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:vnid>/images', methods=['POST'])
def upload_vn_images(vnid):
    if 'files' not in request.files:
        return jsonify({"error": "No file part"}), 400
    files = request.files.getlist('files')
    file_data = [{'filename': file.filename, 'content': file.read()} for file in files]
    task = upload_images_task.delay('vn', vnid, file_data)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:vnid>/images', methods=['PUT'])
def update_vn_images(vnid):
    task = update_images_task.delay('vn', vnid)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:vnid>/images/<string:id>', methods=['PUT'])
def update_vn_image(vnid, id):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    file_data = {'filename': file.filename, 'content': file.read()}
    task = update_images_task.delay('vn', vnid, id, file_data)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:vnid>/images', methods=['DELETE'])
def delete_vn_images(vnid):
    task = delete_images_task.delay('vn', vnid)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:vnid>/images/<string:id>', methods=['DELETE'])
def delete_vn_image(vnid, id):
    task = delete_images_task.delay('vn', vnid, id)
    return jsonify({"task_id": task.id}), 202


@vns_bp.route('/<string:vnid>/savedatas', methods=['GET'])
def get_vn_savedatas(vnid):
    format = request.args.get('format', 'file')
    if format == 'file':
        ...
    task = get_savedatas_task.delay('vn', vnid)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:vnid>/savedatas/<string:id>', methods=['GET'])
def get_vn_savedata(vnid, id):
    format = request.args.get('format', 'file')
    if format == 'file':
        savedata = get('savedata', id)
        savedata_path = get_savedata_path(vnid, id)
        if not savedata or not savedata_path:
            abort(400, 'Invaild file url')
        return send_file(savedata_path, as_attachment=True, download_name=savedata.filename)
    task = get_savedatas_task.delay('vn', vnid, id)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:vnid>/savedatas', methods=['POST'])
def upload_vn_savedatas(vnid):
    if 'files' not in request.files and 'files[]' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    files = request.files.getlist('files') or request.files.getlist('files[]')
    file_data = []
    for file in files:
        file_data.append({
            'filename': file.filename,
            'content': file.read(),
            'last_modified': file.headers.get('Last-Modified')
        })
    
    task = upload_savedatas_task.delay('vn', vnid, file_data)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:vnid>/savedatas', methods=['DELETE'])
def delete_vn_savedatas(vnid):
    task = delete_savedatas_task.delay('vn', vnid)
    return jsonify({"task_id": task.id}), 202

@vns_bp.route('/<string:vnid>/savedatas/<string:id>', methods=['DELETE'])
def delete_vn_savedata(vnid, id):
    task = delete_savedatas_task.delay('vn', vnid, id)
    return jsonify({"task_id": task.id}), 202