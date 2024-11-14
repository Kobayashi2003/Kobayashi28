from flask import Blueprint, request, render_template
from .utils import make_api_request, get_task_status

backup_restore_test_routes = Blueprint('backup_restore_test', __name__)

@backup_restore_test_routes.route('/backup', methods=['GET', 'POST'])
def test_backup():
    if request.method == 'POST':
        return make_api_request('POST', 'backup', request.json)
    return render_template('test_backup_restore.html', operation='backup')

@backup_restore_test_routes.route('/restore', methods=['GET', 'POST'])
def test_restore():
    if request.method == 'POST':
        return make_api_request('POST', 'restore', request.json)
    return render_template('test_backup_restore.html', operation='restore')

@backup_restore_test_routes.route('/backup/status/<task_id>', methods=['GET'])
@backup_restore_test_routes.route('/restore/status/<task_id>', methods=['GET'])
def get_backup_restore_status(task_id):
    return get_task_status('backup', task_id)