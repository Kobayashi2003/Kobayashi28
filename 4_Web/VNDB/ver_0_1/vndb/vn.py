from flask import Blueprint, render_template, abort, request, redirect, url_for, current_app
from vndb.db import connect_db

from vndb.utils import format_description, judge_sexual, judge_violence
from vndb.search import generate_fields, generate_filters, search_vndb, search_local
from vndb.search import fields_params, filters_params
from vndb.download import download_vn

vn_bp = Blueprint('vn', __name__, 
                  url_prefix='/vn', 
                  template_folder='templates',
                  static_folder='static')

@vn_bp.route('/<id>', methods=['GET'])
def show(id):

    result = search_local(id=id)
    if not result:
        result = search_vndb(filters=generate_filters(id=id), fields=generate_fields())['results']
    if not result:
        abort(404, "VN not found")

    result[0]['description'] = format_description(result[0]['description'])
    if result[0]['image'] is not None:
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
