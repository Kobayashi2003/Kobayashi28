from typing import Dict

from flask import jsonify, abort
from . import search_bp
from api import cache 
from api.tasks import get_data_task

@search_bp.route('/data/<string:data_type>/<string:data_size>/<string:id>', methods=['GET'])
@cache.memoize(timeout=60)
def get_data(data_type: str, data_size: str, id: str) -> Dict[str, str]:
    if data_type not in ['vn', 'character', 'tag', 'producer', 'staff', 'trait']:
        abort(400, description="Invalid data type")
    if data_size not in ['small', 'large']:
        abort(400, description="Invalid data size")

    task = get_data_task.delay(data_type, id, data_size)
    return jsonify({"task_id": task.id}), 202