from typing import Dict

from flask import jsonify, abort
from . import database_bp
from api.tasks import cleanup_task
from api.utils.check import infer_type_from_id

@database_bp.route('/cleanup/<string:cleanup_type>', methods=['POST'])
def cleanup_database(cleanup_type: str) -> Dict[str, str]:
    if cleanup_type not in ['vn', 'tag', 'producer', 'staff', 'character', 'trait', 'all']:
        abort(400, description="Invalid cleanup type")
    if not infer_type_from_id(id) == cleanup_type:
        abort(400, description="Invalid ID")

    task = cleanup_task.delay(cleanup_type)
    return jsonify({"task_id": task.id}), 202
