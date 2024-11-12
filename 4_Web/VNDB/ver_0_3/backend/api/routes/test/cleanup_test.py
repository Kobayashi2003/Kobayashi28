from flask import Blueprint, request, render_template
from .utils import make_api_request, get_task_status

cleanup_test_routes = Blueprint('cleanup_test', __name__)

@cleanup_test_routes.route('/cleanup', methods=['GET', 'POST'])
def test_cleanup():
    if request.method == 'POST':
        return make_api_request('POST', 'cleanup', request.json)
    return render_template('test_cleanup.html')

@cleanup_test_routes.route('/cleanup/status/<task_id>', methods=['GET'])
def get_cleanup_status(task_id):
    return get_task_status('cleanup', task_id)