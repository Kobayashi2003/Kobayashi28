from flask import Blueprint, jsonify

savedata_bp = Blueprint('savedata', __name__, url_prefix='/savedata')

@savedata_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

@savedata_bp.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@savedata_bp.errorhandler(500)
def server_error(e):
    return jsonify(error="An unexpected error occurred"), 500

from .get import get_savedata, get_savedatas
from .delete import delete_savedata, delete_savedatas
from .upload import upload_savedatas
from .serve import serve_savedata
