from typing import Dict

from flask import request, jsonify
from . import database_bp 
from api.tasks import backup_task

@database_bp.route('/backup', methods=['POST'])
def backup_database() -> Dict[str, str]:
    data = request.json
    filename = data.get('filename') 

    task = backup_task.delay(filename)
    return jsonify({"task_id": task.id}), 202