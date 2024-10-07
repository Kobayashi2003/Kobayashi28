from flask import Blueprint, render_template, abort
from vndb.db import connect_db

from vndb.utils import format_description, judge_sexual, judge_violence

vn_bp = Blueprint('vn', __name__, url_prefix='/vn', template_folder='templates')

@vn_bp.route('/')
def index():
    conn = connect_db()
    with conn.cursor() as curs:
        curs.execute("""
        SELECT 
            id, title,
            image->>'thumbnail' as thumbnail,
            image->>'sexual' as  image__sexual,
            image->>'violence' as image__violence
        FROM vn ORDER BY id DESC""")
        result = curs.fetchall()
    vns = []
    for row in result:
        vns.append({
        'id':               row[0],
        'title':            row[1],
        'thumbnail':        row[2],
        'image__sexual':    judge_sexual(float(row[3])),
        'image__violence':  judge_sexual(float(row[4]))
        })
    return render_template('vn/index.html', vns=vns)


@vn_bp.route('/<id>')
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


@vn_bp.route('/search')
def search():
    return render_template('vn/search.html')

@vn_bp.route('/config')
def config():
    return render_template('vn/config.html') 
