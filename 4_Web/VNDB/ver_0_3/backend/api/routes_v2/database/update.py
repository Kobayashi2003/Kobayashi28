from typing import Dict

from flask import jsonify, abort
from . import database_bp
from api.tasks import update_data_task
from api.utils.check import infer_type_from_id

@database_bp.route('/update/<string:update_type>/<string:id>', methods=['PUT'])
def update_data(update_type: str, id: str) -> Dict[str, str]:
    if update_type not in ['vn', 'tag', 'producer', 'staff', 'character', 'trait']:
        abort(400, description="Invalid update type")
    if not infer_type_from_id(id) == update_type:
        abort(400, description="Invalid ID")
    
    task = update_data_task.delay(update_type, id)
    return jsonify({"task_id": task.id}), 202