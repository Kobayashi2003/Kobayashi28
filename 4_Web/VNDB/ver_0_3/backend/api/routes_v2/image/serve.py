from flask import request, abort, send_file

from . import image_bp
from api import cache
from api.utils import convert_imgid_to_imgpath
from api.utils import convert_imgurl_to_imgid
from api.utils.check import is_valid_image_id

@image_bp.route('/v/<id>', methods=['GET'])
@image_bp.route('/c/<id>', methods=['GET'])
def serve_image(id):
    image_url = request.url
    type = 'vn' if '/v/' in image_url else 'character'

    # Convert the URL to a file path
    image_id = get_image_id(image_url)
    if not is_valid_image_id(image_id, type):
        abort(400, description="Invalid Image ID")

    image_path = get_image_path(type, image_id)

    if image_path is None:
        abort(400, description="Invalid image URL")

    return send_file(image_path, mimetype='image/jpeg')

@cache.memoize(timeout=60)
def get_image_id(url):
    return convert_imgurl_to_imgid(url)

@cache.memoize(timeout=60)
def get_image_path(type, id):
    return convert_imgid_to_imgpath(type, id)