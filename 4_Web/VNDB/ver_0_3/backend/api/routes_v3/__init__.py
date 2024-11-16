from flask import Blueprint, jsonify
from api import celery

api_bp = Blueprint('api_v3', __name__, url_prefix='/api/v3')

@api_bp.route('/tasks/<string:task_id>', methods=['GET'])
def task_status(task_id: str):
    task = celery.AsyncResult(task_id)
    return jsonify({
        'state': task.state,
        'status': task.info.get('status', 'Task is in progress...') if task.state != 'FAILURE' else 'Task failed',
        'result': task.result if task.state == 'SUCCESS' else None,
        'error': str(task.result) if task.state == 'FAILURE' else None
    })

# Import and register other blueprints
from .hello import hello_bp
from .database import database_bp
from .search import search_bp
from .image import image_bp
from .savedata import savedata_bp

api_bp.register_blueprint(hello_bp)
api_bp.register_blueprint(database_bp)
api_bp.register_blueprint(search_bp)
api_bp.register_blueprint(image_bp)
api_bp.register_blueprint(savedata_bp)