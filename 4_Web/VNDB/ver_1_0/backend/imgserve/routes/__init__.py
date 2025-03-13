from flask import Blueprint, jsonify 

api_bp = Blueprint('api', __name__, url_prefix='/')

@api_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@api_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@api_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500

@api_bp.route('', methods=['GET', 'TRACE'])
def hello_world():
    return jsonify({"message": "IMGSERVE"})

from .images import image_bp
from .tasks import task_bp
from .additional import additional_bp

api_bp.register_blueprint(image_bp)
api_bp.register_blueprint(task_bp)
api_bp.register_blueprint(additional_bp)