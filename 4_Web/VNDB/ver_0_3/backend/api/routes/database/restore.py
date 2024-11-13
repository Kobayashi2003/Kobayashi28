from typing import Dict

from flask import request, jsonify
from . import database_bp
from api.tasks import restore_task

@database_bp.route('/restore', methods=['POST'])
def restore_database() -> Dict[str, str]:
    data = request.json
    filename = data.get('filename')

    task = restore_task.delay(filename)
    return jsonify({"task_id": task.id}), 202