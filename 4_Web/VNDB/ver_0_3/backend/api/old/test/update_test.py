from flask import Blueprint, request, render_template
from .utils import make_api_request, get_task_status

update_test_routes = Blueprint('update_test', __name__)

@update_test_routes.route('/update', methods=['GET', 'POST'])
def test_update():
    if request.method == 'POST':
        update_type = request.form.get('updateType')
        id = request.form.get('id')
        return make_api_request('POST', f'update/{update_type}/{id}')
    return render_template('test_update.html')

@update_test_routes.route('/update/status/<task_id>', methods=['GET'])
def get_update_status(task_id):
    return get_task_status('update', task_id)