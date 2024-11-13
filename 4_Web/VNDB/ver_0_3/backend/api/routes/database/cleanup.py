from typing import Dict

from flask import jsonify, abort
from . import database_bp
from api.tasks import cleanup_task

@database_bp.route('/cleanup/<string:cleanup_type>', methods=['POST'])
def cleanup_database(cleanup_type: str) -> Dict[str, str]:
    if cleanup_type not in ['vn', 'tag', 'producer', 'staff', 'character', 'trait', 'all']:
        abort(400, description="Invalid cleanup type")

    task = cleanup_task.delay(cleanup_type)
    return jsonify({"task_id": task.id}), 202
