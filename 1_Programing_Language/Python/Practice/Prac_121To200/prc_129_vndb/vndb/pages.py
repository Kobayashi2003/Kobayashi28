from flask import Blueprint, render_template, abort, request, redirect, url_for
from vndb.db import connect_db

from vndb.utils import format_description, judge_sexual, judge_violence
from vndb.search import generate_fields, generate_filters, search_vndb

vn_bp = Blueprint('vn', __name__, url_prefix='/vn', template_folder='templates')

@vn_bp.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST' and request.form['searchType'] == 'local':
        localTitle          = request.form['localTitle']
        localDevelopers     = request.form['localDevelopers']
        localCharacters     = request.form['localCharacters']
        localLength         = request.form.get('localLength')
        conn = connect_db()
        with conn.cursor() as curs:
            select_sentence = ""

            if localTitle:
                select_sentence += f"""(
                SELECT DISTINCT data->>'id' AS id
                FROM vn
                WHERE data ->> 'title' ILIKE '%{localTitle}%'
                UNION
                SELECT DISTINCT data->>'id' AS id
                FROM vn, jsonb_array_elements(data->'titles') AS data_title
                WHERE data_title->>'title' ILIKE '%{localTitle}%'
                UNION
                SELECT DISTINCT data->>'id' AS id
                FROM vn, jsonb_array_elements(data->'alias') AS data_alias
                WHERE data_alias->>'name' ILIKE '%{localTitle}%'
                )"""
            if localDevelopers:
                select_sentence += " INTERSECT " if select_sentence else ""
                select_sentence += f"""(
                SELECT DISTINCT
                    data ->> 'id' AS id
                FROM vn, jsonb_array_elements(data -> 'developers') AS data_developers
                WHERE
                    data_developers ->> 'name' ILIKE '%{localDevelopers}%'
                    OR data_developers ->> 'original' ILIKE '%{localDevelopers}%'
                )"""
            if localCharacters:
                select_sentence += " INTERSECT " if select_sentence else ""
                select_sentence += f"""(
                SELECT DISTINCT data->>'id' AS id
                FROM vn, jsonb_array_elements(data->'va') AS data_va
                WHERE
                    data_va->'character'->>'name' ILIKE '%{localCharacters}%'
                    OR data_va->'character'->>'original' ILIKE '%{localCharacters}%'
                )"""
            if localLength:
                select_sentence += " INTERSECT " if select_sentence else ""
                localLength = {'very-short': 1,'short': 2, 'average': 3, 'long': 4,'very-long': 5}[localLength]
                select_sentence += f"""(
                SELECT DISTINCT data->>'id' AS id
                FROM vn
                WHERE data->>'length' = '{localLength}'
                )"""
            curs.execute(f"""
            SELECT
                data ->> 'id' as id,
                data ->> 'title' as title,
                data -> 'image' ->> 'thumbnail' as thumbnail,
                data -> 'image' ->> 'sexual' as image__sexual,
                data -> 'image' ->> 'violence' as image__violence
            FROM vn
            WHERE data ->> 'id' IN (
                {select_sentence if select_sentence else "SELECT data->>'id' FROM vn"}
            ) ORDER BY data->>'id' DESC;
            """)
            result = curs.fetchall()

    if request.method == 'POST' and request.form['searchType'] == 'vndb':
        result = []

    if request.method == 'GET':
        conn = connect_db()
        with conn.cursor() as curs:
            curs.execute("""
            SELECT
                data ->> 'id' as id,
                data ->> 'title' as title,
                data -> 'image' ->> 'thumbnail' as thumbnail,
                data -> 'image' ->> 'sexual' as image__sexual,
                data -> 'image' ->> 'violence' as image__violence
            FROM vn ORDER BY data->>'id' DESC""")
            result = curs.fetchall()

    vns = [{
        'id':               row[0],
        'title':            row[1],
        'thumbnail':        row[2],
        'image__sexual':    judge_sexual(float(row[3])),
        'image__violence':  judge_sexual(float(row[4]))
    } for row in result]

    return render_template('vn/index.html', vns=vns)


@vn_bp.route('/<id>', methods=['GET'])
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



@vn_bp.route('/test', methods=('GET', 'POST'))
def test():

    if request.method == 'POST':
        return render_template('vn/test.html', test='success')

    return render_template('vn/test.html', test='test')

@vn_bp.route('/config')
def config():
    return render_template('vn/config.html')
