from typing import Dict

from flask import jsonify, abort
from . import database_bp
from api.tasks import delete_data_task
from api.utils import infer_type_from_id

@database_bp.route('/delete/<string:delete_type>/<string:id>', methods=['DELETE'])
def delete_data(delete_type: str, id: str) -> Dict[str, str]:
    if delete_type not in ['vn', 'tag', 'producer', 'staff', 'character', 'trait']:
        abort(400, description="Invalid delete type")
    if not infer_type_from_id(id) == delete_type:
        abort(400, description="Invalid ID")
    
    task = delete_data_task.delay(delete_type, id)
    return jsonify({"task_id": task.id}), 202