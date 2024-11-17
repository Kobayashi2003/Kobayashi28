from flask import Blueprint, jsonify
from api import celery

api_bp = Blueprint('api_v4', __name__, url_prefix='/api/v4')

@api_bp.route('/tasks/<string:task_id>', methods=['GET'])
def task_status(task_id: str):
    task = celery.AsyncResult(task_id)
    return jsonify(task.result)

# Import and register other blueprints
from .hello import hello_bp
from .vns import vns_bp
from .characters import characters_bp
from .producers import producers_bp
from .staff import staff_bp
from .tags import tags_bp
from .traits import traits_bp

api_bp.register_blueprint(hello_bp)
api_bp.register_blueprint(vns_bp)
api_bp.register_blueprint(characters_bp)
api_bp.register_blueprint(producers_bp)
api_bp.register_blueprint(staff_bp)
api_bp.register_blueprint(tags_bp)
api_bp.register_blueprint(traits_bp)