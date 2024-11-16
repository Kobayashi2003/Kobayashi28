from flask import Blueprint, request, render_template
from .utils import make_api_request, get_task_status

delete_test_routes = Blueprint('delete_test', __name__)

@delete_test_routes.route('/delete', methods=['GET', 'POST'])
def test_delete():
    if request.method == 'POST':
        delete_type = request.form.get('deleteType')
        id = request.form.get('id')
        return make_api_request('DELETE', f'delete/{delete_type}/{id}')
    return render_template('test_delete.html')

@delete_test_routes.route('/delete/status/<task_id>', methods=['GET'])
def get_delete_status(task_id):
    return get_task_status('delete', task_id)