import os
from flask import Blueprint, jsonify, send_file, abort 
from imgserve.database import exists, create
from imgserve.tasks import (
    create_image_task, update_image_task, delete_image_task
)
from imgserve.utils import get_image_path

image_bp = Blueprint('images', __name__, url_prefix='/')

@image_bp.route('/<string:type>/<int:id>', methods=['GET'])
def get_image(type, id):
    if not exists(type, id):
        create(type, id)
    image_path = get_image_path(type, id)
    if not os.path.exists(image_path):
        abort(404)
    return send_file(image_path, mimetype='image/jpeg')

@image_bp.route('/<string:type>/<int:id>', methods=['POST'])
def create_image(type, id):
    task = create_image_task.delay(type, id)
    return jsonify({"task_id": task.id}), 202

@image_bp.route('/<string:type>/<int:id>', methods=['PUT'])
def update_image(type, id):
    task = update_image_task.delay(type, id)
    return jsonify({"task_id": task.id}), 202

@image_bp.route('/<string:type>/<int:id>', methods=['DELETE'])
def delete_image(type, id):
    task = delete_image_task.delay(type, id)
    return jsonify({"task_id": task.id}), 202