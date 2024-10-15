from flask import Blueprint, render_template 

from vndb.search import search_local, handle_for_index


index_bp = Blueprint('index', __name__, url_prefix='/')

@index_bp.route('/', methods=['GET'])
def index():
    vns = handle_for_index(search_local())
    return render_template('index/index.html', vns=vns)
