from typing import Dict 

from flask import request, jsonify, abort
from . import database_bp
from api.tasks import crud_task
from api.utils.check import infer_type_from_id

@database_bp.route('/crud/<string:model_type>/<string:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def crud_database(model_type: str, id: str) -> Dict[str, str]:
    if model_type not in ['vn', 'tag', 'producer', 'staff', 'character', 'trait']:
        abort(400, description="Invalid model type")
    if not infer_type_from_id(id) == model_type:
        abort(400, description="Invalid ID")

    params = request.get_json(force=True, silent=True)
    if params is None:
        params = request.form.to_dict()
    if not params:
        params = request.args.to_dict()
    if not params:
        params = {}

    if request.method == 'GET':
        task = crud_task.delay('read', model_type, id)
    elif request.method == 'POST':
        task = crud_task.delay('create', model_type, id, params)
    elif request.method == 'PUT':
        task = crud_task.delay('update', model_type, id, params)
    elif request.method == 'DELETE':
        task = crud_task.delay('delete', model_type, id)

    return jsonify({"task_id": task.id}), 202

