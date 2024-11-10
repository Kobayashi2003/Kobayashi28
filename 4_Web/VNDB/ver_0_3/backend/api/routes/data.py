from flask import Blueprint, request, jsonify, abort 
from flask_caching import Cache

from api.search.local.search import search as local_search
from api.search.remote.search import search as remote_search

data_bp = Blueprint('data', __name__)
cache = Cache(config={'CACHE_TYPE': 'simple'})

@data_bp.route('/api/data/<string:data_type>/<string:id>', defaults={'data_size': 'small'}, methods=['GET'])
@data_bp.route('/api/data/<string:data_type>/<string:id>/<string:data_size>', methods=['GET'])
@cache.memoize(timeout=300)
def get_data(data_type, id, data_size):
    if data_type not in ['vn', 'character', 'tag', 'producer', 'staff', 'trait']:
        abort(400, description="Invalid data type")
    if data_size not in ['small', 'large']:
        abort(400, description="Invalid data size")

    task = data_