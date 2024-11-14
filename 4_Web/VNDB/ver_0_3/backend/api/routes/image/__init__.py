from flask import Blueprint, request, jsonify, abort, send_file
from api.utils import convert_imgid_to_imgpath 

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

from .download import download_images
from .update import update_images
from .delete import delete_image, delete_images
from .get import get_image, get_images
from .serve import serve_image
