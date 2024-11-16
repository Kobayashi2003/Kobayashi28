from typing import Dict

from flask import jsonify, abort
from . import savedata_bp
from api.tasks import delete_savedata_task
from api.tasks import delete_savedatas_task
from api.utils.check import is_valid_id

@savedata_bp.route('/delete/<string:id>', methods=['DELETE'])
def delete_savedata(id: str) -> Dict[str, str]:
    if not is_valid_id(id, 's'):
        abort(400, description="Invalid ID")
    task = delete_savedata_task.delay(id)
    return jsonify({"task_id": task.id}), 202

@savedata_bp.route('/delete/batch/<string:vnid>', methods=['DELETE'])
def delete_savedatas(vnid: str) -> Dict[str, str]:
    if not is_valid_id(vnid, 'v'):
        abort(400, description="Invalid ID")
    task = delete_savedatas_task.delay(vnid)
    return jsonify({"task_id": task.id}), 202