from flask import Blueprint, request, render_template
from .utils import make_api_request, get_task_status

crud_test_routes = Blueprint('crud_test', __name__)

@crud_test_routes.route('/crud', methods=['GET', 'POST'])
def test_crud():
    if request.method == 'POST':
        data = request.json
        return make_api_request('POST', 'crud/' + data['operation'], data)
    return render_template('test_crud.html')

@crud_test_routes.route('/crud/status/<task_id>', methods=['GET'])
def get_crud_status(task_id):
    return get_task_status('crud', task_id)