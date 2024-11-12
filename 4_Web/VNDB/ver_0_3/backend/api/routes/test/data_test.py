from flask import Blueprint, request, render_template
from .utils import make_api_request, get_task_status

data_test_routes = Blueprint('data_test', __name__)

@data_test_routes.route('/data', methods=['GET', 'POST'])
def test_data():
    if request.method == 'POST':
        data_type = request.form.get('dataType')
        id = request.form.get('id')
        data_size = request.form.get('dataSize', 'small')
        return make_api_request('GET', f'data/{data_type}/{id}/{data_size}')
    return render_template('test_data.html')

@data_test_routes.route('/data/status/<task_id>', methods=['GET'])
def get_data_status(task_id):
    return get_task_status('data', task_id)