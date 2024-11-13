from flask import Blueprint, jsonify

image_bp = Blueprint('image', __name__, url_prefix='/image')

@image_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@image_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@image_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500
