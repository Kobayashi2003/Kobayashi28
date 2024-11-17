from typing import Dict

from flask import jsonify, abort, request
from . import database_bp
from api.tasks import create_data_task
from api.utils import infer_type_from_id

@database_bp.route('/create/<string:create_type>l', methods=['POST'])
def create_data(create_type: str, id: str) -> Dict[str, str]:
    if create_type not in ['vn', 'tag', 'producer', 'staff', 'character', 'trait']:
        abort(400, description="Invalid create type")
    if not infer_type_from_id(id) == create_type:
        abort(400, description="Invalid ID")

    data = request.json if request.is_json else request.form.to_dict()
    
    task = create_data_task.delay(create_type, id, data)
    return jsonify({"task_id": task.id}), 202