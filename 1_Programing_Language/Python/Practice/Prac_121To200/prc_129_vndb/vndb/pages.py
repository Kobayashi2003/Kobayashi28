from flask import Blueprint, render_template, abort, request, redirect, url_for
from vndb.db import connect_db

from vndb.utils import format_description, judge_sexual, judge_violence
from vndb.search import generate_fields, generate_filters, search_vndb, search_local
from vndb.search import VN_Operactor_And, VN_Operactor_Or
from vndb.search import VN_Filter_ID, VN_Filter_Developer, VN_Filter_Staff, VN_Filter_Character, VN_Filter_Tag 

vn_bp = Blueprint('vn', __name__, url_prefix='/vn', template_folder='templates')

def handle_form(form = None) -> dict:
    return {
        'searchType':         form.get('searchType')        if form.get('searchType')       != None else 'local',
        'localTitle':         form.get('localTitle')        if form.get('localTitle')       != None else '',
        'localDevelopers':    form.get('localDevelopers')   if form.get('localDevelopers')  != None else '',
        'localCharacters':    form.get('localCharacters')   if form.get('localCharacters')  != None else '',
        'localTags':          form.get('localTags')         if form.get('localTags')        != None else '',
        'localLength':        form.get('localLength')       if form.get('localLength')      != None else '',
        'vndbQuery':          form.get('vndbQuery')         if form.get('vndbQuery')        != None else '',
        'vndbDevelopers':     form.get('vndbDevelopers')    if form.get('vndbDevelopers')   != None else '',
        'vndbStaffs':         form.get('vndbStaffs')        if form.get('vndbStaffs')       != None else '',
        'vndbCharacters':     form.get('vndbCharacters')    if form.get('vndbCharacters')   != None else '',
        'vndbTags':           form.get('vndbTags')          if form.get('vndbTags')         != None else '',
        'sortSelect':         form.get('sortSelect')        if form.get('sortSelect')       != None else 'title',
        'sortOrder':          form.get('sortOrder')         if form.get('sortOrder')        != None else 'asc'
    } if form else {
        'searchType':         'local',
        'localTitle':         '',
        'localDevelopers':    '',
        'localCharacters':    '',
        'localTags':          '',
        'localLength':        '',
        'vndbQuery':          '',
        'vndbDevelopers':     '',
        'vndbStaffs':         '',
        'vndbCharacters':     '',
        'vndbTags':           '',
        'sortSelect':         'title',
        'sortOrder':          'asc'
    } 

@vn_bp.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST' and ('searchType' not in request.form or not request.form['searchType']):
        return render_template('test.html', test='TEST FROM INDEX')

    if request.method == 'POST' and request.form['searchType'] == 'local':

        form = handle_form(request.form)

        result = search_local(title=form['localTitle'], developers=form['localDevelopers'], characters=form['localCharacters'], 
                              tags=form['localTags'], length=form['localLength'], sort_by=form['sortSelect'], 
                              sort_order=(form['sortOrder'] == 'desc'))
        result = result if result else []


    if request.method == 'POST' and request.form['searchType'] == 'vndb':

        form = handle_form(request.form)

        and_container = VN_Operactor_And()

        if form['vndbDevelopers']:
            or_container = VN_Operactor_Or()
            for developer in form['vndbDevelopers'].split(','):
                or_container += VN_Filter_Developer(developer.strip())
            and_container += or_container

        if form['vndbStaffs']:
            or_container = VN_Operactor_Or()
            for staff in form['vndbStaffs'].split(','):
                or_container += VN_Filter_Staff(staff.strip())
            and_container += or_container

        if form['vndbCharacters']:
            or_container = VN_Operactor_Or()
            for character in form['vndbCharacters'].split(','):
                or_container += VN_Filter_Character(character.strip())
            and_container += or_container

        if form['vndbTags']:
            or_container = VN_Operactor_Or()
            for tag in form['vndbTags'].split(','):
                or_container += VN_Filter_Tag(tag.strip())
            and_container += or_container

        filters = and_container.get_filters()
        # return render_template('test.html', test=filters)
        filters = filters if len(filters) > 1 else []

        fields = generate_fields("""id, title, image.thumbnail, image.sexual, image.violence""")
        filters = generate_filters(query=form['vndbQuery'], filters=filters)

        result = search_vndb(filters=filters, fields=fields, sort=form['sortSelect'], reverse=(form['sortOrder'] == 'desc'))
        result = result['results'] if result else []
        result = [[row['id'], row['title'], row['image']['thumbnail'], row['image']['sexual'], 
                   row['image']['violence']] for row in result] if result else []

    if request.method == 'GET':

        form = handle_form()

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

    return render_template('vn/index.html', vns=vns, form=form)


@vn_bp.route('/<id>', methods=['GET'])
def show(id):

    conn = connect_db()
    with conn.cursor() as curs:
        curs.execute("SELECT data FROM vn WHERE id = %s", (id,))
        result = curs.fetchone()
        if not result:
            fields = generate_fields()
            filter = generate_filters(filters=(VN_Operactor_And() + VN_Filter_ID(id)).get_filters())
            result = search_vndb(filters=filter, fields=fields)
            result = result['results'] if result else []
        if not result:
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


@vn_bp.route('/config')
def config():
    return render_template('vn/config.html')
