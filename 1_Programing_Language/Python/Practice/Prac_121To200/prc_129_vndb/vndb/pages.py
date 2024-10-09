from flask import Blueprint, render_template, abort, request, redirect, url_for
from vndb.db import connect_db

from vndb.utils import format_description, judge_sexual, judge_violence
from vndb.search import generate_fields, generate_filters, search_vndb

vn_bp = Blueprint('vn', __name__, url_prefix='/vn', template_folder='templates')

@vn_bp.route('/', methods=['GET'])
def index():

    conn = connect_db()
    with conn.cursor() as curs:
        curs.execute("""
        SELECT
            id,
            title,
            image->>'thumbnail' as thumbnail,
            image->>'sexual' as  image__sexual,
            image->>'violence' as image__violence,
            released, length, length_minutes
        FROM vn ORDER BY id DESC""")
        result = curs.fetchall()

    vns = [{
        'id':               row[0],
        'title':            row[1],
        'thumbnail':        row[2],
        'image__sexual':    judge_sexual(float(row[3])),
        'image__violence':  judge_sexual(float(row[4]))
    } for row in result]

    return render_template('vn/index.html', vns=vns)


@vn_bp.route('/<id>', methods=['POST'])
def show(id):
    conn = connect_db()
    with conn.cursor() as curs:
        curs.execute("SELECT data FROM vn WHERE id = %s", (id,))
        result = curs.fetchone()
        if result is None:
            abort(404, "VN not found")

    result[0]['description'] = format_description(result[0]['description'])
    result[0]['image']['sexual'] = judge_violence(float(result[0]['image']['sexual']))
    result[0]['image']['violence'] = judge_violence(float(result[0]['image']['violence']))

    for screenshot in result[0]['screenshots']:
        screenshot['sexual'] = judge_violence(float(screenshot['sexual']))
        screenshot['violence'] = judge_violence(float(screenshot['violence']))

    for va in result[0]['va']:
        va['character']['description'] = format_description(va['character']['description'])
        if va['character']['image'] is not None:
            va['character']['image']['sexual'] = judge_sexual(float(va['character']['image']['sexual']))
            va['character']['image']['violence'] = judge_violence(float(va['character']['image']['violence']))

    return render_template('vn/vn.html', vndata=result[0])


@vn_bp.route('/search_local', methods=['POST'])
def handle_search_local():
    localTitle          = request.form['localTitle']
    localDevelopers     = request.form['localDevelopers']
    localReleasedDate   = request.form['localReleasedDate']
    localCharacters     = request.form['localCharacters']
    localLength         = request.form['localLength']

@vn_bp.route('/search_vndb', methods=['POST'])
def handle_search_vndb():
    pass

@vn_bp.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == 'POST':
        query = request.form['query']
        vndata = search_vndb(fields=generate_fields(), filters=generate_filters(query=query))
        if vndata:
            # return render_template('vn/search.html', vndata=vndata)
            return render_template('vn/vn.html', vndata=vndata['results'][0])
        else:
            return render_template('vn/search.html', error="No results found for query: " + query)

    return render_template('vn/search.html')

@vn_bp.route('/config')
def config():
    return render_template('vn/config.html')
