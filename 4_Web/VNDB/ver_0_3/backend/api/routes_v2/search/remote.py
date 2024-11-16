from typing import Dict 

from flask import request, jsonify, abort
from . import search_bp
from api import cache
from api.tasks import search_task

@search_bp.route('/remote/<string:search_type>/<string:response_size>', methods=['POST'])
@cache.memoize(timeout=60)
def search_remote(search_type: str, response_size: str) -> Dict[str, str]:
    if search_type not in ['vn', 'character', 'tag', 'producer', 'staff', 'trait']:
        abort(400, description="Invalid search type")
    if response_size not in ['small', 'large']:
        abort(400, description="Invalid response size")

    params = request.get_json(force=True, silent=True)
    if params is None:
        params = request.form.to_dict()
    if not params:
        params = request.args.to_dict()
    if not params:
        params = {}

    task = search_task.delay(search_from='remote', search_type=search_type, response_size=response_size, params=params)
    return jsonify({"task_id": task.id}), 202