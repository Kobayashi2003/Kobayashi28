from typing import Dict, Optional

from flask import jsonify, abort
from . import database_bp
from api.tasks import read_data_task 
from api.utils import infer_type_from_id

@database_bp.route('/read/<string:read_type>', methods=['GET'])
@database_bp.route('/read/<string:read_type>/<string:id>', methods=['GET'])
def read_data(read_type: str, id: Optional[str] = None) -> Dict[str, str]:
    if read_type not in ['vn', 'tag', 'producer', 'staff', 'character', 'trait']:
        abort(400, description="Invalid read type")
    if id and not infer_type_from_id(id) == read_type:
        abort(400, description="Invalid ID")
    
    task = read_data_task.delay(read_type, id)
    return jsonify({"task_id": task.id}), 202