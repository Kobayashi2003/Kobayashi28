from typing import Dict

from flask import jsonify, abort
from . import savedata_bp
from api import cache
from api.tasks import get_savedata_task
from api.tasks import get_savedatas_task
from api.utils.check import is_valid_id

@savedata_bp.route('/get/<string:savedata_id>', methods=['GET'])
@cache.cached(timeout=60)
def get_savedata(savedata_id: str) -> Dict[str, str]:
    if not is_valid_id(savedata_id, 's'):
        abort(400, description="Invalid ID")
    task = get_savedata_task.delay(savedata_id)
    return jsonify({"task_id": task.id}), 202

@savedata_bp.route('/get/batch/<string:vn_id>', methods=['GET'])
@cache.cached(timeout=60)
def get_savedatas(vnid: str) -> Dict[str, str]:
    if not is_valid_id(vnid, 'v'):
        abort(400, description="Invalid ID")
    task = get_savedatas_task.delay(vnid)
    return jsonify({"task_id": task.id}), 202