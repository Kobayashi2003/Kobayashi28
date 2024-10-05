from flask import Blueprint, render_template
from vndb.db import connect_db

from vndb.utils import format_description

vn_bp = Blueprint('vn', __name__, url_prefix='/vn', template_folder='templates')

@vn_bp.route('/<id>')
def show(id):
    conn = connect_db()
    with conn.cursor() as curs:
        curs.execute("SELECT data FROM vn WHERE id = %s", (id,))
        result = curs.fetchone()
        if result is None:
            return 'VN not found'
    result[0]['description'] = format_description(result[0]['description'])
    for va in result[0]['va']:
        va['character']['description'] = format_description(va['character']['description'])
    return render_template('vn/vn.html', vndata=result[0])