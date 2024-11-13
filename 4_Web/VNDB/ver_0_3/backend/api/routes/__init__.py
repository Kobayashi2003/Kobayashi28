from typing import Dict, Any

from flask import Blueprint, jsonify
from api import celery

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/status/<string:task_id>', methods=['GET'])
def task_status(task_id: str) -> Dict[str, Any]:
    task = celery.AsyncResult(task_id)
    return jsonify({
        'state': task.state,
        'status': task.info.get('status', 'Task is in progress...') if task.state != 'FAILURE' else 'Task failed',
        'result': task.result if task.state == 'SUCCESS' else None,
        'error': str(task.result) if task.state == 'FAILURE' else None
    })

from .hello import hello_bp
from .search import search_bp
from .database import database_bp
from .image import image_bp

api_bp.register_blueprint(hello_bp)
api_bp.register_blueprint(search_bp)
api_bp.register_blueprint(database_bp)
api_bp.register_blueprint(image_bp)
