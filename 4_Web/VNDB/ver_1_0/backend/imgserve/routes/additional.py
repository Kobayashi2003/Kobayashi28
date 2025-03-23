import os
import re
import random
from flask import Blueprint, send_file, abort, current_app

from imgserve.database import exists, create
from imgserve.utils import get_image_path
from imgserve.tasks.images import create_image_task

additional_bp = Blueprint('additional', __name__, url_prefix='/')

@additional_bp.route('/bg', methods=['GET'])
def get_bg():
    BG_FOLDER = current_app.config['DATA_FOLDER'] + '/additional/bg'
    os.makedirs(BG_FOLDER, exist_ok=True)
    bg_files = os.listdir(BG_FOLDER)
    random_bg = random.choice(bg_files)
    return send_file(os.path.abspath(os.path.join(BG_FOLDER, random_bg)), mimetype='image/png')

@additional_bp.route('/random', methods=['GET'])
def get_random():
    IMG_FOLDER = current_app.config['DATA_FOLDER'] + '/additional/random'
    os.makedirs(IMG_FOLDER, exist_ok=True)
    img_files = os.listdir(IMG_FOLDER)
    random_img = random.choice(img_files)
    return send_file(os.path.abspath(os.path.join(IMG_FOLDER, random_img)), mimetype='image/png')

@additional_bp.route('/img/<string:type>/<int:_>/<int:id>', methods=['GET'])
@additional_bp.route('/img/<string:type>/<int:id>', methods=['GET'])
@additional_bp.route('/img/<string:type>', methods=['GET'])
def get_img(type, id, _=None):

    thumbnail_pattern = r"(?P<original_type>cv|sf)\.t"
    thumbnail_match = re.match(thumbnail_pattern, type)
    if thumbnail_match and not exists(thumbnail_match.group('original_type'), id):
        create_image_task.delay(thumbnail_match.group('original_type'), id)

    original_pattern = r"(?P<original_type>cv|sf)"
    original_match = re.match(original_pattern, type)
    if original_match and not exists(original_match.group('original_type'), id):
        create_image_task.delay(f"{original_match.group('original_type')}.t", id)

    if not exists(type, id):
        create(type, id)
    image_path = get_image_path(type, id)
    if not os.path.exists(image_path):
        abort(404)
    return send_file(image_path, mimetype='image/png')