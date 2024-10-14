from flask import current_app, render_template, request, abort, redirect, url_for, Blueprint

from vndb.db import connect_db
from vndb.utils import format_description, judge_violence, judge_sexual
from vndb.search import generate_fields, generate_filters, search_vndb, search_local
from vndb.search import filters_params, fields_params
from vndb.download import download_vn

index_bp = Blueprint('index', __name__, url_prefix='/')

@index_bp.route('/', methods=['GET'])
def index():

    conn = connect_db()
    with conn.cursor() as curs:
        curs.execute("""
        SELECT
            data ->> 'id' as id,
            data ->> 'title' as title,
            data -> 'image' ->> 'thumbnail' as thumbnail,
            data -> 'image' ->> 'sexual' as image__sexual,
            data -> 'image' ->> 'violence' as image__violence
        FROM vn ORDER BY data->>'title'""")
        result = curs.fetchall()

    vns = [{
        'id':               row[0],
        'title':            row[1],
        'thumbnail':        row[2],
        'image__sexual':    judge_sexual(float(row[3])),
        'image__violence':  judge_sexual(float(row[4]))
    } for row in result]

    return render_template('index/index.html', vns=vns)
