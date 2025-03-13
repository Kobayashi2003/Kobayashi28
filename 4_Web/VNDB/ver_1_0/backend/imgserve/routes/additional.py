import os
import random
from flask import Blueprint, send_file, current_app

additional_bp = Blueprint('additional', __name__, url_prefix='/')

@additional_bp.route('/bg', methods=['GET'])
def get_bg():
    BG_FOLDER = current_app.config['DATA_FOLDER'] + '/additional/bg'
    os.makedirs(BG_FOLDER, exist_ok=True)
    bg_files = os.listdir(BG_FOLDER)
    random_bg = random.choice(bg_files)
    return send_file(os.path.abspath(os.path.join(BG_FOLDER, random_bg)), mimetype='image/png')

@additional_bp.route('/img', methods=['GET'])
def get_img():
    IMG_FOLDER = current_app.config['DATA_FOLDER'] + '/additional/img'
    os.makedirs(IMG_FOLDER, exist_ok=True)
    img_files = os.listdir(IMG_FOLDER)
    random_img = random.choice(img_files)
    return send_file(os.path.abspath(os.path.join(IMG_FOLDER, random_img)), mimetype='image/png')
