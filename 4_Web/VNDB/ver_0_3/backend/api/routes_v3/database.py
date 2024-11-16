from flask import Blueprint, jsonify

database_bp = Blueprint('database', __name__, url_prefix='/database')

@database_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@database_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@database_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500